"""
Guess the Number (Computer) with OOP:
1. Inheritance
2. Static Methods
3. Magic Methods
"""
import random

class NumberGame:
    def __init__(self, min_num=1, max_num=100):
        self.min = min_num
        self.max = max_num
        self.target = self._generate_number()
        self.attempts = 0

    @staticmethod
    def _generate_number():
        """Static method: Doesn't need instance access"""
        return random.randint(1, 100)

    def __str__(self):
        """Magic Method: String representation"""
        return f"Guess between {self.min}-{self.max}"

class GuessTheNumber(NumberGame):  # Inheritance
    def play(self):
        print(self)  # Uses __str__
        while True:
            guess = int(input("Your guess: "))
            self.attempts += 1
            
            if guess < self.target:
                print("Too low!")
            elif guess > self.target:
                print("Too high!")
            else:
                print(f"Correct! Attempts: {self.attempts}")
                break

# Usage
game = GuessTheNumber()
game.play()