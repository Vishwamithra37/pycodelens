```markdown
# PyCodeLens

A Python code analysis tool to extract and manipulate code elements like functions, decorators, classes, and print statements. It supports Python, JavaScript, and TypeScript files.

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

5. **Code Replacement**
   - Replace a function with new code
   - Replace a class with new code
   - Replace specific lines with new code
   - Automatic indentation handling

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

# Print source code for a specific function
pycodelens path/to/your_file.py --function-name my_function

# Print source code for a specific class
pycodelens path/to/your_file.py --class-name MyClass

# Print specific lines from the file
pycodelens path/to/your_file.py --lines 10-20
```

### Code Replacement

```bash
# Replace a function with code from a file
pycodelens path/to/your_file.py --replace-function my_function --replacement-file new_function.py

# Replace a class with inline content
pycodelens path/to/your_file.py --replace-class MyClass --replacement-content "class MyClass:\n    def new_method(self):\n        pass"

# Replace specific lines
pycodelens path/to/your_file.py --replace-lines 10-20 --replacement-file new_code.py
```

### Python API

```python
from pycodelens import analyze_file, replace_element

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

# Replace a function
success, message = replace_element(
    'path/to/your_file.py',
    'function',
    'my_function',
    replacement_file='new_function.py'
)
print(message)
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

## Supported Languages

- **Python** - Full support with detailed analysis
- **JavaScript** - Basic support for functions and classes
- **TypeScript** - Basic support with interface detection

## Requirements

- Python 3.7+
- astroid library

## License

MIT
```