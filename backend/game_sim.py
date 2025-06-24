import random
import time

class CupPongSimulator:
    def __init__(self, num_cups=10):
        self.num_cups = num_cups
        self.cups = [True] * num_cups  # True = cup active

    def simulate_shot(self):
        # Simulate a random shot result
        remaining = [i for i, active in enumerate(self.cups) if active]
        if not remaining:
            return None  # Game over
        hit = random.choice(remaining)
        self.cups[hit] = False
        return hit

    def get_game_state(self):
        return self.cups
