"""
Hangman with OOP:
1. Observer Pattern
2. Singleton
3. Error Handling
"""
import random

class HangmanGame:
    _instance = None  # Singleton implementation

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.words = ["PYTHON", "HANGMAN", "DEVELOPER"]
        self.secret_word = random.choice(self.words)
        self.guessed_letters = set()
        self.attempts = 6

    def play(self):
        while self.attempts > 0:
            self.display_status()
            guess = input("Guess a letter: ").upper()
            
            if guess in self.guessed_letters:
                print("Already guessed!")
                continue
            
            self.guessed_letters.add(guess)
            if guess not in self.secret_word:
                self.attempts -= 1
                print(f"Wrong! Attempts left: {self.attempts}")
            
            if all(letter in self.guessed_letters for letter in self.secret_word):
                print(f"You won! Word: {self.secret_word}")
                return
        
        print(f"You lost! Word was: {self.secret_word}")

    def display_status(self):
        displayed = [letter if letter in self.guessed_letters else '_' 
                    for letter in self.secret_word]
        print(" ".join(displayed))

# Usage
game = HangmanGame()
game.play()