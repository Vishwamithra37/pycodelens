# PyCodeLens

A Python code analysis tool to extract code elements like functions, decorators, classes, and print statements.

## Installation

```bash
pip install pycodelens
```

## Features

PyCodeLens allows you to extract and analyze:

1. **Functions**
   - Count of functions in a file
   - Function names
   - Line numbers (start and end)
   - Associated decorators

2. **Decorators**
   - Count of decorators in a file
   - Decorator names
   - Line numbers where they appear

3. **Classes**
   - Count of classes in a file
   - Class names
   - Line numbers (start and end)
   - Methods within each class

4. **Print Statements**
   - Count of print statements
   - Line numbers
   - Number of arguments

## Usage

### Command Line

```bash
# Basic usage (shows count of all elements)
pycodelens path/to/your_file.py

# Show detailed information about functions
pycodelens path/to/your_file.py --functions

# Show only decorators
pycodelens path/to/your_file.py --decorators

# Show information about all elements
pycodelens path/to/your_file.py --all

# Show only counts
pycodelens path/to/your_file.py --counts

# Output in JSON format
pycodelens path/to/your_file.py --json

# Show verbose information
pycodelens path/to/your_file.py --all --verbose
```

### Python API

```python
from pycodelens import analyze_file

# Analyze a file
analysis = analyze_file('path/to/your_file.py')

# Access the summary
summary = analysis['summary']
print(f"Number of functions: {summary['num_functions']}")
print(f"Function names: {summary['function_names']}")

# Access raw results
raw_results = analysis['raw_results']
for func in raw_results['functions']:
    print(f"Function {func['name']} on lines {func['line_start']}-{func['line_end']}")
    if func['decorators']:
        print(f"  Has decorators: {', '.join('@' + d['name'] for d in func['decorators'])}")
```

## Example Output

```
File: example.py
  Functions: 5
  Decorators: 3
  Classes: 2
  Print statements: 7

FUNCTIONS:
  main (lines 10-20)
    Decorators: @app.route, @login_required
  process_data (lines 22-30)
  helper_function (lines 32-35)
    Decorators: @staticmethod
  ...

DECORATORS:
  @app.route: 2 occurrences (lines: 10, 45)
  @login_required: 1 occurrences (lines: 11)
  @staticmethod: 2 occurrences (lines: 32, 50)
  ...
```

## Requirements

- Python 3.7+
- astroid library

## License

MIT
