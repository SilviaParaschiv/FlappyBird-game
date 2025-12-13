from __future__ import annotations

class ScoreManager:
    def __init__(self, filename: str = "highscore.txt"):
        self.filename = filename
        self.high_score = self.load_high_score()

    def load_high_score(self) -> int:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return int(file.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
        
    def try_update_high_score(self, score: int) -> bool:
        if score > self.high_score:
            self.high_score = score
            with open(self.filename, "w", encoding="utf-8") as file:
                file.write(str(self.high_score))
            return True
        return False