"""
Countdown Timer with OOP:
1. Decorators
2. Context Managers
3. Threading
"""
import time
from threading import Thread
from functools import wraps

def log_time(func):  # Decorator Pattern
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time: {time.time() - start:.2f}s")
        return result
    return wrapper

class Timer:
    def __init__(self, seconds):
        self.duration = seconds
    
    def __enter__(self):  # Context Manager
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Timer completed!")

    @log_time
    def countdown(self):
        """Threaded countdown with decorator"""
        def run():
            for remaining in range(self.duration, 0, -1):
                print(f"{remaining // 60:02d}:{remaining % 60:02d}", end="\r")
                time.sleep(1)
        
        t = Thread(target=run)
        t.start()
        t.join()

# Usage
with Timer(10) as timer:  # Context Manager
    timer.countdown()