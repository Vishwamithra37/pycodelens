"""
Core analysis functionality for PyCodeLens.
"""

import sys
import os
import astroid
from collections import defaultdict

def extract_code_elements(file_path):
    """
    Extract code elements (functions, decorators, classes, print statements) from a Python file.
    
    Args:
        file_path: Path to the Python file to analyze
        
    Returns:
        Dictionary containing lists of functions, decorators, classes, and print calls
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Parse the file using astroid
    module = astroid.parse(code, file_path)
    
    functions = []
    decorators = []
    classes = []
    print_calls = []
    
    # Extract functions and their details
    for node in module.nodes_of_class(astroid.FunctionDef):
        func_info = {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'decorators': []
        }
        
        # Extract decorators for this function
        if node.decorators:
            for decorator in node.decorators.nodes:
                decorator_name = ""
                if isinstance(decorator, astroid.Name):
                    decorator_name = decorator.name
                elif isinstance(decorator, astroid.Call) and isinstance(decorator.func, astroid.Name):
                    decorator_name = decorator.func.name
                    
                if decorator_name:
                    func_info['decorators'].append({
                        'name': decorator_name,
                        'line': decorator.lineno
                    })
                    decorators.append({
                        'name': decorator_name,
                        'line': decorator.lineno,
                        'parent': node.name
                    })
        
        functions.append(func_info)
    
    # Extract classes
    for node in module.nodes_of_class(astroid.ClassDef):
        class_info = {
            'name': node.name,
            'line_start': node.lineno,
            'line_end': node.end_lineno,
            'methods': []
        }
        
        # Extract methods within the class
        for method_node in node.nodes_of_class(astroid.FunctionDef):
            method_info = {
                'name': method_node.name,
                'line_start': method_node.lineno,
                'line_end': method_node.end_lineno
            }
            class_info['methods'].append(method_info)
            
        classes.append(class_info)
    
    # Extract print statements
    for node in module.nodes_of_class(astroid.Call):
        if isinstance(node.func, astroid.Name) and node.func.name == 'print':
            print_calls.append({
                'line': node.lineno,
                'args': len(node.args)
            })
    
    return {
        'functions': functions,
        'decorators': decorators,
        'classes': classes,
        'print_calls': print_calls
    }

def analyze_file(file_path):
    """
    Analyze a Python file and return formatted results.
    
    Args:
        file_path: Path to the Python file to analyze
        
    Returns:
        Dictionary with analysis results and formatted output
    """
    results = extract_code_elements(file_path)
    
    # Generate summary
    summary = {
        'file': file_path,
        'num_functions': len(results['functions']),
        'num_decorators': len(results['decorators']),
        'num_classes': len(results['classes']),
        'num_print_statements': len(results['print_calls']),
        'function_names': [f['name'] for f in results['functions']],
        'decorator_names': sorted(set(d['name'] for d in results['decorators'])),
        'class_names': [c['name'] for c in results['classes']]
    }
    
    # Group decorators by name
    decorator_counts = defaultdict(int)
    decorator_lines = defaultdict(list)
    
    for dec in results['decorators']:
        decorator_counts[dec['name']] += 1
        decorator_lines[dec['name']].append(dec['line'])
    
    summary['decorator_counts'] = dict(decorator_counts)
    summary['decorator_lines'] = dict(decorator_lines)
    
    return {
        'raw_results': results,
        'summary': summary
    }
