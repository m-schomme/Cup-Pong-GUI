import random
import time

class CupPongSimulator:
    def __init__(self, num_cups=6):
        self.num_cups = num_cups
        self.player_cups = [True] * num_cups  # True = cup active
        self.robot_cups = [True] * num_cups

    def simulate_player_shot(self):
        # Simulate a random shot result
        remaining = [i for i, active in enumerate(self.player_cups) if active]
        if not remaining:
            return None  # Game over
        hit = random.choice(remaining)
        self.player_cups[hit] = False
        return hit

    def simulate_robot_shot(self):
        # Simulate a random shot result
        remaining = [i for i, active in enumerate(self.robot_cups) if active]
        if not remaining:
            return None
        hit = random.choice(remaining)
        self.robot_cups[hit] = False
        return hit
    
    def get_game_state(self):
        return self.player_cups + self.robot_cups
