# backend/core/bayesian_updater.py

class BayesianUpdater:
    def __init__(self, prior_probabilities):
        self.prior_probabilities = prior_probabilities  # Kezdeti valószínűségek

    def update(self, new_data, likelihood):
        """Bayesian frissítés: új adat + valószínűségi frissítés"""
        # A Bayes-tétel alkalmazása
        posterior = (likelihood * self.prior_probabilities) / sum(likelihood * self.prior_probabilities)
        self.prior_probabilities = posterior  # Az új valószínűségek
        return posterior
