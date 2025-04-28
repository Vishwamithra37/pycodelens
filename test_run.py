#!/usr/bin/env python3
"""
Test script to run PyCodeLens on sample.py
"""

from pycodelens.analyzer import analyze_file
import json

# Analyze the sample file
results = analyze_file('sample.py')

# Print summary information
print("File Summary:")
print(f"  Functions: {results['summary']['num_functions']}")
print(f"  Decorators: {results['summary']['num_decorators']}")
print(f"  Classes: {results['summary']['num_classes']}")
print(f"  Print statements: {results['summary']['num_print_statements']}")

# Print function details
print("\nFUNCTIONS:")
for func in results['raw_results']['functions']:
    print(f"  {func['name']} (lines {func['line_start']}-{func['line_end']})")
    if func['decorators']:
        print(f"    Decorators: {', '.join('@' + d['name'] for d in func['decorators'])}")

# Print decorator details
print("\nDECORATORS:")
decorator_names = {}
for dec in results['raw_results']['decorators']:
    decorator_names.setdefault(dec['name'], []).append(dec['line'])
    
for name, lines in decorator_names.items():
    print(f"  @{name}: {len(lines)} occurrences (lines: {', '.join(map(str, lines))})")

# Print JSON data
print("\nFull JSON data:")
print(json.dumps(results['summary'], indent=2))
