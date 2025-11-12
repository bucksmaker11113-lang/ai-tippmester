"""
Logger – Tippmester 5.2
Színes naplózás a futás közbeni eseményekhez.
"""

from datetime import datetime

class Logger:
    COLORS = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "ENDC": "\033[0m",
    }

    def log(self, level, message):
        color = self.COLORS.get(level, "")
        endc = self.COLORS["ENDC"]
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{color}[{timestamp}] {level}: {message}{endc}")

    def info(self, msg): self.log("INFO", msg)
    def success(self, msg): self.log("SUCCESS", msg)
    def warning(self, msg): self.log("WARNING", msg)
    def error(self, msg): self.log("ERROR", msg)
