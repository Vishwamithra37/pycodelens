"""
Core analysis functionality for PyCodeLens.
"""

import sys
import os
import astroid
import re
from collections import defaultdict

class BaseCodeParser:
    """Base class for language-specific code parsers."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.code = f.read()
        self.lines = self.code.splitlines()
    
    def extract_elements(self):
        """Extract code elements. Must be implemented by subclasses."""
        raise NotImplementedError
        
    def get_source_by_name(self, results, name, element_type='function'):
        """Get source code by element name."""
        if element_type == 'function':
            for func in results['functions']:
                if func['name'] == name:
                    return func['source_code']
            # Check class methods
            for cls in results['classes']:
                for method in cls['methods']:
                    if method['name'] == name:
                        return method['source_code']
        elif element_type == 'class':
            for cls in results['classes']:
                if cls['name'] == name:
                    return cls['source_code']
                    
        return None
        
    def get_source_by_lines(self, start_line, end_line):
        """Get source code by line numbers."""
        end_idx = min(end_line, len(self.lines))
        return '\n'.join(self.lines[start_line-1:end_idx])


class PythonParser(BaseCodeParser):
    """Parser for Python code using astroid."""
    
    def extract_elements(self):
        """Extract code elements from Python file."""
        # Parse the file using astroid
        module = astroid.parse(self.code, self.file_path)
        
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
                'decorators': [],
                'source_code': '\n'.join(self.lines[node.lineno-1:node.end_lineno])
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
                'methods': [],
                'source_code': '\n'.join(self.lines[node.lineno-1:node.end_lineno])
            }
            
            # Extract methods within the class
            for method_node in node.nodes_of_class(astroid.FunctionDef):
                method_info = {
                    'name': method_node.name,
                    'line_start': method_node.lineno,
                    'line_end': method_node.end_lineno,
                    'source_code': '\n'.join(self.lines[method_node.lineno-1:method_node.end_lineno])
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
            'print_calls': print_calls,
        }


class JavaScriptParser(BaseCodeParser):
    """Basic parser for JavaScript code."""
    
    def extract_elements(self):
        """Extract code elements from JavaScript file."""
        # This is a simplified implementation
        # A real implementation would use a proper JavaScript parser
        
        functions = []
        classes = []
        
        # Basic regex-based parsing for demonstration
        
        # Find function declarations
        func_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*\{'
        function_matches = re.finditer(func_pattern, self.code)
        
        for match in function_matches:
            func_name = match.group(1)
            line_number = self.code[:match.start()].count('\n') + 1
            
            # Find the end of the function (simplification)
            end_line = line_number
            brace_count = 1
            for i, line in enumerate(self.lines[line_number:], line_number+1):
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0:
                        end_line = i
                        break
            
            functions.append({
                'name': func_name,
                'line_start': line_number,
                'line_end': end_line,
                'source_code': '\n'.join(self.lines[line_number-1:end_line])
            })
        
        # Find class declarations (ES6)
        class_pattern = r'class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{'
        class_matches = re.finditer(class_pattern, self.code)
        
        for match in class_matches:
            class_name = match.group(1)
            line_number = self.code[:match.start()].count('\n') + 1
            
            # Find the end of the class
            end_line = line_number
            brace_count = 1
            for i, line in enumerate(self.lines[line_number:], line_number+1):
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0:
                        end_line = i
                        break
            
            classes.append({
                'name': class_name,
                'line_start': line_number,
                'line_end': end_line,
                'methods': [],  # Simplified
                'source_code': '\n'.join(self.lines[line_number-1:end_line])
            })
        
        return {
            'functions': functions,
            'classes': classes,
            'decorators': [],  # JavaScript doesn't have Python-style decorators
            'print_calls': [],  # Not tracking console.log statements
        }


def get_parser_for_file(file_path):
    """Factory function to get the appropriate parser for a file."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.py':
        return PythonParser(file_path)
    elif file_ext in ['.js', '.jsx']:
        return JavaScriptParser(file_path)
    elif file_ext in ['.ts', '.tsx']:
        return TypeScriptParser(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

def extract_code_elements(file_path):
    """
    Extract code elements from a file using the appropriate parser.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        Dictionary containing lists of code elements
    """
    parser = get_parser_for_file(file_path)
    results = parser.extract_elements()
    # Store the parser for later use
    results['_parser'] = parser
    return results


def get_source_by_name(results, name, element_type='function'):
    """
    Get source code of an element by name.
    
    Args:
        results: Results from extract_code_elements
        name: Name of the element
        element_type: Type of element ('function' or 'class')
        
    Returns:
        Source code as string or None if not found
    """
    if '_parser' in results:
        return results['_parser'].get_source_by_name(results, name, element_type)
    return None


def get_source_by_lines(results, start_line, end_line):
    """
    Get source code by line numbers.
    
    Args:
        results: Results from extract_code_elements
        start_line: Starting line number (1-based)
        end_line: Ending line number (1-based)
        
    Returns:
        Source code as string
    """
    if '_parser' in results:
        return results['_parser'].get_source_by_lines(start_line, end_line)
    return None


def analyze_file(file_path):
    """
    Analyze a file and return formatted results.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        Dictionary with analysis results and formatted output
    """
    results = extract_code_elements(file_path)
    
    # Generate summary
    summary = {
        'file': file_path,
        'num_functions': len(results['functions']),
        'num_decorators': len(results.get('decorators', [])),
        'num_classes': len(results['classes']),
        'num_print_statements': len(results.get('print_calls', [])),
        'function_names': [f['name'] for f in results['functions']],
        'decorator_names': sorted(set(d['name'] for d in results.get('decorators', []))),
        'class_names': [c['name'] for c in results['classes']]
    }
    
    # Group decorators by name
    decorator_counts = defaultdict(int)
    decorator_lines = defaultdict(list)
    
    for dec in results.get('decorators', []):
        decorator_counts[dec['name']] += 1
        decorator_lines[dec['name']].append(dec['line'])
    
    summary['decorator_counts'] = dict(decorator_counts)
    summary['decorator_lines'] = dict(decorator_lines)
    
    return {
        'raw_results': results,
        'summary': summary
    }

class TypeScriptParser(BaseCodeParser):
    """Parser for TypeScript code."""
    
    def extract_elements(self):
        """Extract code elements from TypeScript file."""
        functions = []
        classes = []
        interfaces = []
        
        # Parse functions
        func_pattern = r'function\s+(\w+)\s*\([^)]*\)\s*(?::\s*\w+(?:\[\]|\<.*\>)?)?\s*\{'
        function_matches = re.finditer(func_pattern, self.code)
        
        for match in function_matches:
            func_name = match.group(1)
            line_number = self.code[:match.start()].count('\n') + 1
            
            # Find the end of the function
            end_line = line_number
            brace_count = 1
            for i, line in enumerate(self.lines[line_number:], line_number+1):
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0:
                        end_line = i
                        break
            
            functions.append({
                'name': func_name,
                'line_start': line_number,
                'line_end': end_line,
                'source_code': '\n'.join(self.lines[line_number-1:end_line])
            })
        
        # Parse classes
        class_pattern = r'class\s+(\w+)(?:\s+(?:extends|implements)\s+\w+)?\s*\{'
        class_matches = re.finditer(class_pattern, self.code)
        
        for match in class_matches:
            class_name = match.group(1)
            line_number = self.code[:match.start()].count('\n') + 1
            
            # Find the end of the class
            end_line = line_number
            brace_count = 1
            for i, line in enumerate(self.lines[line_number:], line_number+1):
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0:
                        end_line = i
                        break
            
            classes.append({
                'name': class_name,
                'line_start': line_number,
                'line_end': end_line,
                'methods': [],  # Methods would need detailed parsing
                'source_code': '\n'.join(self.lines[line_number-1:end_line])
            })
        
        # Parse interfaces
        interface_pattern = r'interface\s+(\w+)(?:\s+extends\s+\w+)?\s*\{'
        interface_matches = re.finditer(interface_pattern, self.code)
        
        for match in interface_matches:
            interface_name = match.group(1)
            line_number = self.code[:match.start()].count('\n') + 1
            
            # Find the end of the interface
            end_line = line_number
            brace_count = 1
            for i, line in enumerate(self.lines[line_number:], line_number+1):
                if '{' in line:
                    brace_count += line.count('{')
                if '}' in line:
                    brace_count -= line.count('}')
                    if brace_count == 0:
                        end_line = i
                        break
            
            interfaces.append({
                'name': interface_name,
                'line_start': line_number,
                'line_end': end_line,
                'source_code': '\n'.join(self.lines[line_number-1:end_line])
            })
        
        return {
            'functions': functions,
            'classes': classes,
            'interfaces': interfaces,
            'decorators': [],
            'print_calls': [],
        }

def replace_element(target_file, element_type, element_name, replacement_file=None, replacement_content=None):
    """
    Replace a code element (function, class) or line range in the target file.
    
    Args:
        target_file: Path to the file where replacement will occur
        element_type: Type of element to replace ('function', 'class', or 'lines')
        element_name: Name of the element, or line range as 'start-end'
        replacement_file: Path to the file containing replacement content (optional)
        replacement_content: Direct replacement content as string (optional)
        
    Returns:
        Tuple of (success, message)
    """
    if not replacement_file and not replacement_content:
        return False, "Either replacement_file or replacement_content must be provided"
    
    try:
        # Read target file
        with open(target_file, 'r', encoding='utf-8') as f:
            target_lines = f.readlines()
        
        # Read replacement content
        if replacement_file:
            with open(replacement_file, 'r', encoding='utf-8') as f:
                replacement_content = f.read()
        
        # Get element to replace
        start_line = None
        end_line = None
        
        if element_type == 'lines':
            try:
                parts = element_name.split('-')
                start_line = int(parts[0])
                end_line = int(parts[1]) if len(parts) > 1 else start_line
            except ValueError:
                return False, f"Invalid line range format: {element_name}. Use 'start-end'."
        else:
            # Analyze the file to find the element
            results = analyze_file(target_file)['raw_results']
            
            if element_type == 'function':
                element_list = results['functions']
                # Also check class methods
                if not any(f['name'] == element_name for f in element_list):
                    for cls in results['classes']:
                        for method in cls.get('methods', []):
                            if method['name'] == element_name:
                                start_line = method['line_start']
                                end_line = method['line_end']
                                break
                        if start_line:
                            break
            elif element_type == 'class':
                element_list = results['classes']
            else:
                return False, f"Unsupported element type: {element_type}"
                
            # If we haven't found a method, look for the main element
            if not start_line:
                for element in element_list:
                    if element['name'] == element_name:
                        start_line = element['line_start']
                        end_line = element['line_end']
                        break
                        
            if not start_line:
                return False, f"{element_type.capitalize()} '{element_name}' not found in {target_file}"
        
        # Calculate indentation of the first line
        original_indent = ""
        if start_line and start_line <= len(target_lines):
            line = target_lines[start_line - 1]
            original_indent = line[:len(line) - len(line.lstrip())]
        
        # Process the replacement content to match indentation
        replacement_lines = replacement_content.splitlines()
        if replacement_lines:
            # Identify the base indentation of the replacement content
            # by finding the non-empty line with the least indentation
            replace_indent = None
            for line in replacement_lines:
                if line.strip():  # Skip empty lines
                    current_indent = len(line) - len(line.lstrip())
                    if replace_indent is None or current_indent < replace_indent:
                        replace_indent = current_indent
            
            # If no indent was found, default to 0
            if replace_indent is None:
                replace_indent = 0
                
            # Apply the target indentation to all lines
            adjusted_lines = []
            for line in replacement_lines:
                if line.strip():  # If not an empty line
                    # Remove the original indent and add the new one
                    if len(line) > replace_indent:
                        line_content = line[replace_indent:]
                        adjusted_lines.append(f"{original_indent}{line_content}")
                    else:
                        adjusted_lines.append(f"{original_indent}{line.lstrip()}")
                else:
                    # For empty lines, just add the original indent if there was one
                    if original_indent:
                        adjusted_lines.append(original_indent)
                    else:
                        adjusted_lines.append("")
                        
            replacement_content = "\n".join(adjusted_lines)
        
        # Perform the replacement
        new_content = []
        i = 0
        while i < len(target_lines):
            line_num = i + 1
            if line_num < start_line or line_num > end_line:
                new_content.append(target_lines[i])
                i += 1
            elif line_num == start_line:
                # Add the replacement content
                new_content.append(replacement_content)
                if not replacement_content.endswith('\n'):
                    new_content.append('\n')
                # Skip all lines of the original element
                i = end_line
            else:
                i += 1
        
        # Write the modified content back to the file
        with open(target_file, 'w', encoding='utf-8') as f:
            for line in new_content:
                f.write(line if isinstance(line, str) else '')
        
        return True, f"Successfully replaced {element_type} '{element_name}' in {target_file}"
        
    except Exception as e:
        return False, f"Error replacing {element_type}: {str(e)}"