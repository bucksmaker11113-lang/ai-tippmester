# ==========================================================
#  REINFORCEMENT LEARNING ENGINE – Quantum Engine 7.0
# ==========================================================
#  Az AI képes tanulni:
#   - bankroll változásból
#   - odds movementből
#   - value model hibáiból
#   - variance büntetésből
#   - reward = profit - risk - market_resistance
#
#  Az RL agent dönt:
#   - 0 → SKIP
#   - 1 → SINGLE
#   - 2 → KOMBI
#   - 3 → LIVE
#
#  Ez a modul a backbone, amire a multi-agent rendszer épül.
# ==========================================================

import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from database.db import SessionLocal
from database.models import BankrollLog, OddsHistory, TipSingle, TipLive


# ----------------------------------------------------------
# 1) Állapot (state) generáló
# ----------------------------------------------------------

def build_state():
    """
    RL state:
      - bankroll change
      - recent profit/loss
      - variance
      - odds volatility
      - recent value performance
      - recent live performance
    """

    db = SessionLocal()

    # BANKROLL
    br = db.query(BankrollLog).order_by(BankrollLog.id.desc()).limit(20).all()
    bankroll_vals = [b.balance for b in br][::-1]
    if len(bankroll_vals) < 5:
        bankroll_vals = bankroll_vals + [bankroll_vals[-1]] * (5 - len(bankroll_vals))

    bankroll_change = bankroll_vals[-1] - bankroll_vals[0]
    variance = float(np.var(bankroll_vals))

    # ODDS VOLATILITY
    oh = db.query(OddsHistory).order_by(OddsHistory.id.desc()).limit(30).all()
    odds_vals = [o.odds for o in oh][-10:]
    if len(odds_vals) < 3:
        odds_vals = odds_vals + [odds_vals[-1]] * (3 - len(odds_vals))
    volatility = float(np.std(odds_vals))

    # RECENT PERFORMANCE (PREMATCH)
    ts = db.query(TipSingle).order_by(TipSingle.id.desc()).limit(20).all()
    recent_single_strength = np.mean([t.strength for t in ts]) if ts else 0.5

    # RECENT PERFORMANCE (LIVE)
    tlv = db.query(TipLive).order_by(TipLive.id.desc()).limit(20).all()
    recent_live_strength = np.mean([t.live_strength for t in tlv]) if tlv else 0.5

    state = np.array([
        bankroll_change,
        variance,
        volatility,
        recent_single_strength,
        recent_live_strength
    ], dtype=np.float32)

    return state


# ----------------------------------------------------------
# 2) RL Neural Network
# ----------------------------------------------------------

class RLNet(nn.Module):
    def __init__(self, input_dim=5, output_dim=4):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, output_dim)
        )

    def forward(self, x):
        return self.layers(x)


# ----------------------------------------------------------
# 3) Deep Q-Learning Agent
# ----------------------------------------------------------

class RLEngine:
    def __init__(self):
        self.state_size = 5
        self.action_size = 4
        self.gamma = 0.92
        self.epsilon = 0.15
        self.lr = 0.0008
        self.memory = []

        self.model = RLNet()
        self.optimizer = optim.Adam(self.model.parameters(), lr=self.lr)
        self.loss_fn = nn.MSELoss()

    # Memory Replay Buffer
    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))
        if len(self.memory) > 5000:
            self.memory.pop(0)

    # Choose Action
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, self.action_size - 1)
        with torch.no_grad():
            q = self.model(torch.tensor(state).float().unsqueeze(0))
        return torch.argmax(q).item()

    # Reward Function
    def reward_function(self, action):
        db = SessionLocal()
        br = db.query(BankrollLog).order_by(BankrollLog.id.desc()).limit(2).all()

        if len(br) < 2:
            return 0

        profit = br[-1].balance - br[-2].balance
        variance_penalty = -abs(profit) * 0.2

        # Action-specific reward shaping
        if action == 1:     # SINGLE
            action_bonus = 0.1
        elif action == 2:   # KOMBI
            action_bonus = 0.05
        elif action == 3:   # LIVE
            action_bonus = 0.15
        else:               # SKIP
            action_bonus = -0.05

        return profit + variance_penalty + action_bonus

    # Training Cycle
    def train(self, batch=32):
        if len(self.memory) < batch:
            return

        minibatch = random.sample(self.memory, batch)

        for state, action, reward, next_state in minibatch:
            state_t = torch.tensor(state).float()
            next_state_t = torch.tensor(next_state).float()

            target = reward + self.gamma * torch.max(self.model(next_state_t))
            current = self.model(state_t)[action]

            loss = self.loss_fn(current, target.detach())

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

    # Save model
    def save(self, path="rl_model.pth"):
        torch.save(self.model.state_dict(), path)

    # Load model
    def load(self, path="rl_model.pth"):
        if os.path.exists(path):
            self.model.load_state_dict(torch.load(path))


# ----------------------------------------------------------
# GLOBAL RL ENGINE INSTANCE
# ----------------------------------------------------------

rl_agent = RLEngine()


# ----------------------------------------------------------
# 4) Pipeline hook: RL decision
# ----------------------------------------------------------

def rl_decide_action():
    state = build_state()
    action = rl_agent.choose_action(state)
    return action


def rl_learn(action):
    state = build_state()
    reward = rl_agent.reward_function(action)
    next_state = build_state()

    rl_agent.remember(state, action, reward, next_state)
    rl_agent.train()
    rl_agent.save()
