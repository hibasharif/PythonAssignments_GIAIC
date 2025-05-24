"""
Password Generator with OOP:
1. Builder Pattern
2. Property Decorators
3. Class Methods
"""
import random
import string

class PasswordBuilder:  # Builder Pattern
    def __init__(self):
        self.length = 12
        self._complexity = "medium"
    
    @property
    def complexity(self):
        return self._complexity
    
    @complexity.setter
    def complexity(self, value):
        if value in ["low", "medium", "high"]:
            self._complexity = value
        else:
            raise ValueError("Invalid complexity level")

    @classmethod
    def strong_password(cls):
        """Alternative constructor"""
        builder = cls()
        builder.length = 16
        builder.complexity = "high"
        return builder

    def generate(self):
        chars = string.ascii_letters
        if self.complexity == "medium":
            chars += string.digits
        elif self.complexity == "high":
            chars += string.digits + "!@#$%^&*"
        
        return ''.join(random.choice(chars) for _ in range(self.length))

# Usage
builder = PasswordBuilder.strong_password()  # Class Method
builder.complexity = "high"  # Property Setter
print("Your password:", builder.generate())