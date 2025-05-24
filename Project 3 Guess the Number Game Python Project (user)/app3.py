"""
Guess the Number (User) with OOP:
1. Composition
2. Strategy Pattern
3. Error Handling
"""
import random

class GuessStrategy:  # Strategy Pattern
    def next_guess(self, low, high):
        raise NotImplementedError

class RandomGuess(GuessStrategy):
    def next_guess(self, low, high):
        return random.randint(low, high)

class BinarySearchGuess(GuessStrategy):
    def next_guess(self, low, high):
        return (low + high) // 2

class UserNumberGame:
    def __init__(self, strategy=RandomGuess()):  # Composition
        self.strategy = strategy
        self.low = 1
        self.high = 100
        self.attempts = 0

    def play(self):
        print("Think of a number 1-100")
        while True:
            guess = self.strategy.next_guess(self.low, self.high)
            print(f"My guess: {guess}")
            response = input("[H]igher, [L]ower, [C]orrect? ").upper()
            
            try:
                if response == "H":
                    self.low = guess + 1
                elif response == "L":
                    self.high = guess - 1
                elif response == "C":
                    print(f"I won in {self.attempts} attempts!")
                    break
                self.attempts += 1
            except ValueError:
                print("Invalid input!")

# Usage
game = UserNumberGame(strategy=BinarySearchGuess())
game.play()