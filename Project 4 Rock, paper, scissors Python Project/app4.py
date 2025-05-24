"""
Rock, Paper, Scissors with OOP:
1. Factory Pattern
2. Enums
3. Polymorphism
"""
from enum import Enum
import random

class Move(Enum):  # Enum for state management
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class MoveFactory:  # Factory Pattern
    @staticmethod
    def create_move(move_type):
        if move_type == "R":
            return Move.ROCK
        elif move_type == "P":
            return Move.PAPER
        elif move_type == "S":
            return Move.SCISSORS
        raise ValueError("Invalid move")

class GameEvaluator:
    @staticmethod
    def evaluate(user, computer):
        """Polymorphic behavior through method logic"""
        if user == computer:
            return "Tie"
        if (user == Move.ROCK and computer == Move.SCISSORS) or \
           (user == Move.PAPER and computer == Move.ROCK) or \
           (user == Move.SCISSORS and computer == Move.PAPER):
            return "You Win"
        return "Computer Wins"

# Usage
user_input = input("Choose [R]ock, [P]aper, [S]cissors: ").upper()
user_move = MoveFactory.create_move(user_input)
computer_move = random.choice(list(Move))

print(f"\nYou: {user_move.name} | Computer: {computer_move.name}")
print(GameEvaluator.evaluate(user_move, computer_move))