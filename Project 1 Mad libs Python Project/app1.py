"""
Mad Libs Generator with OOP Concepts:
1. Class and Object
2. Encapsulation
3. Method Abstraction
"""
class MadLibs:
    def __init__(self):
        self._template = "Once upon a time, there was a {adjective} {noun} who loved to {verb} in {place}."
        self._inputs = {}  # Encapsulated data

    def get_user_inputs(self):
        """Abstraction: Hide input collection logic"""
        self._inputs['noun'] = input("Enter a noun: ")
        self._inputs['verb'] = input("Enter a verb: ")
        self._inputs['adjective'] = input("Enter an adjective: ")
        self._inputs['place'] = input("Enter a place: ")

    def generate_story(self):
        """Polymorphism: Can be overridden by child classes"""
        return self._template.format(**self._inputs)

# Usage
game = MadLibs()  # Object instantiation
game.get_user_inputs()
print("\nYour Story:", game.generate_story())