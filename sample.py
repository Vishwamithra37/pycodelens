#!/usr/bin/env python3
"""
Sample Python file for testing PyCodeLens.
"""

import os
import sys
from functools import wraps

def decorator_one(func):
    """A sample decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("Before function")
        result = func(*args, **kwargs)
        print("After function")
        return result
    return wrapper

def decorator_two(message):
    """A sample decorator with arguments."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(message)
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@decorator_one
def sample_function():
    """A sample function with a decorator."""
    print("This is a sample function")
    return True

@decorator_two("Starting process")
def process_data(data):
    """A sample function with a decorator that has arguments."""
    print(f"Processing {len(data)} items")
    return data

class SampleClass:
    """A sample class."""
    
    def __init__(self, name):
        """Initialize the class."""
        self.name = name
        print(f"Created SampleClass with name: {name}")
    
    @staticmethod
    def static_method():
        """A static method."""
        print("This is a static method")
        return "static"
    
    @classmethod
    def class_method(cls):
        """A class method."""
        print("This is a class method")
        return cls.__name__
    
    def regular_method(self, value):
        """A regular method."""
        print(f"Regular method with value: {value}")
        return value

def main():
    """Main function."""
    print("Starting main function")
    sample_function()
    process_data([1, 2, 3])
    
    sample = SampleClass("test")
    sample.static_method()
    sample.class_method()
    sample.regular_method(42)
    
    print("Finished")

if __name__ == "__main__":
    main()
