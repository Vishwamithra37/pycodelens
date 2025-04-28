#!/usr/bin/env python3
"""
Test script to run PyCodeLens on sample files of different languages
"""

import sys
import os
from pycodelens.analyzer import analyze_file, get_source_by_name, get_source_by_lines
import json

def analyze_and_print_results(file_path):
    """Analyze a file and print the results."""
    print(f"\n{'=' * 60}")
    print(f"Analyzing: {file_path}")
    print(f"{'=' * 60}")
    
    # Determine file type
    _, ext = os.path.splitext(file_path)
    file_type = ext[1:].upper()  # Remove the dot and convert to uppercase
    
    try:
        results = analyze_file(file_path)
        
        # Print summary information
        print(f"\n{file_type} File Summary:")
        print(f"  Functions: {results['summary']['num_functions']}")
        print(f"  Classes: {results['summary']['num_classes']}")
        
        # Python-specific items
        if ext.lower() == '.py':
            print(f"  Decorators: {results['summary']['num_decorators']}")
            print(f"  Print statements: {results['summary']['num_print_statements']}")
        
        # TypeScript-specific items
        if ext.lower() == '.ts':
            interfaces = results['raw_results'].get('interfaces', [])
            print(f"  Interfaces: {len(interfaces)}")
            
            if interfaces:
                print("\nINTERFACES:")
                for interface in interfaces:
                    print(f"  {interface['name']} (lines {interface['line_start']}-{interface['line_end']})")
        
        # Print function details
        print(f"\n{file_type} FUNCTIONS:")
        for func in results['raw_results']['functions']:
            print(f"  {func['name']} (lines {func['line_start']}-{func['line_end']})")
            
            # Print decorators for Python
            if ext.lower() == '.py' and func.get('decorators'):
                print(f"    Decorators: {', '.join('@' + d['name'] for d in func['decorators'])}")
        
        # Print class details
        print(f"\n{file_type} CLASSES:")
        for cls in results['raw_results']['classes']:
            print(f"  {cls['name']} (lines {cls['line_start']}-{cls['line_end']})")
            if 'methods' in cls and cls['methods']:
                print(f"    Methods:")
                for method in cls['methods']:
                    print(f"      {method['name']} (lines {method['line_start']}-{method['line_end']})")
        
        # Demo getting source code by name
        if len(results['raw_results']['functions']) > 0:
            func_name = results['raw_results']['functions'][0]['name']
            print(f"\nSource code for function '{func_name}':")
            source = get_source_by_name(results['raw_results'], func_name, 'function')
            print("-" * 40)
            print(source)
            print("-" * 40)
        
        # Demo getting source code by lines
        if len(results['raw_results']['functions']) > 0:
            func = results['raw_results']['functions'][0]
            start_line = func['line_start']
            end_line = func['line_end']
            print(f"\nSource code for lines {start_line}-{end_line}:")
            source = get_source_by_lines(results['raw_results'], start_line, end_line)
            print("-" * 40)
            print(source)
            print("-" * 40)
            
        # Demo JSON output
        print("\nSummary JSON data:")
        print(json.dumps(results['summary'], indent=2))
            
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Main function to run the test script."""
    # Define sample files
    sample_files = [
        'sample.py',
        'sample.js',
        'sample.ts',
    ]
    
    # Check if files exist
    for file_path in sample_files[:]:
        if not os.path.exists(file_path):
            print(f"Warning: File '{file_path}' not found. Skipping.")
            sample_files.remove(file_path)
    
    # Analyze each file
    for file_path in sample_files:
        analyze_and_print_results(file_path)
    
    # Demonstrate CLI usage examples
    print("\n" + "=" * 60)
    print("CLI USAGE EXAMPLES:")
    print("=" * 60)
    print("\nTo list functions in a file:")
    print("  python -m pycodelens.cli sample.py --functions")
    print("\nTo print a specific function's source code:")
    print("  python -m pycodelens.cli sample.py --function-name greet")
    print("\nTo print a specific class's source code:")
    print("  python -m pycodelens.cli sample.js --class-name User")
    print("\nTo print a specific range of lines:")
    print("  python -m pycodelens.cli sample.ts --lines 10-20")
    print("\nTo analyze a JavaScript file:")
    print("  python -m pycodelens.cli sample.js --all")
    print("\nTo output analysis in JSON format:")
    print("  python -m pycodelens.cli sample.py --json")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())