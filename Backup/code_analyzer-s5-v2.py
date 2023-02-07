# Static Code Analyzer: Stage 5/5
# https://hyperskill.org/projects/112/stages/613/implement
import os
import sys
import re
import ast


def check_001(string, line):
    if len(string) > 79:
        errors.setdefault(line, []).append('S001 Too long')


def check_002(string, line):
    # if re.search('^(?!^( {4})*[^ ])', string)  # Negative lookahead
    if (len(string) - len(string.lstrip(' '))) % 4:
        errors.setdefault(line, []).append('S002 Indentation is not a multiple of four')


def check_003(string, line):
    # if re.search(r'^[^#]*;(?!\S)', string)  # Negative lookahead
    if string.split('#')[0].strip().endswith(';'):
        errors.setdefault(line, []).append('S003 Unnecessary semicolon')


def check_004(string, line):
    # return re.search('^[^#]*[^ ] ?#', string)
    if not string.startswith('#') and '#' in string and '  #' not in string:
	msg = 'S004 At least two spaces required before inline comments'
        errors.setdefault(line, []).append(msg)


def check_005(string, line):
    # return re.search('(?i)# *TODO', string)  # (?i) ignores case in lookahead
    if '#' in string and string.find('#') < string.lower().find('todo'):
        errors.setdefault(line, []).append('S005 TODO found')


def check_006(string, line):
    global empty_lines
    if string == '\n':
        empty_lines += 1
    elif empty_lines > 2:
        empty_lines = 0
        msg = 'S006 More than two blank lines used before this line'
        errors.setdefault(line, []).append(msg)
    else:
        empty_lines = 0


def check_007(string, line):
    match = re.search('(class|def)(?=  +)', string)
    if match:
        msg = f'S007 Too many spaces after \'{match.group(1)}\''
        errors.setdefault(line, []).append(msg)


def check_008(string, line):
    match = re.search('(?<=class )(.*_+.*|[a-z]+)', string)
    if match:
        msg = f'S008 Class name \'{match.group(1)}\' should use CamelCase'
        errors.setdefault(line, []).append(msg)


def check_009(string, line):
    match = re.search(r'(?<=def )(\w*[A-Z]\w*)(?=\()', string)
    if match:
        msg = f'S009 Function name \'{match.group(1)}\' should use snake_case'
        errors.setdefault(line, []).append(msg)


def check_010(tree_obj):
    for node in ast.walk(tree_obj):
        if isinstance(node, ast.FunctionDef):  # Check every function
            for item in node.args.args:  # Check every argument
                if not item.arg.islower():
                    msg = f'S010 Argument name \'{item.arg}\' should be snake_case'
                    errors.setdefault(node.lineno, []).append(msg)


def check_011(tree_obj):
    for node in ast.walk(tree_obj):
        if isinstance(node, ast.FunctionDef):  # Check every function
            for item in node.body:
                if isinstance(item, ast.Assign):  # Check every variable assignment
                    if isinstance(item.targets[0], ast.Name):  # Normal variables
                        variable = item.targets[0].id
                    else:  # Class instance variables, i.e. self.x
                        variable = item.targets[0].attr
                    if not variable.islower():
                        msg = f'S011 Variable \'{variable}\' in function should be snake_case'
                        errors.setdefault(item.lineno, []).append(msg)


def check_012(tree_obj):
    for node in ast.walk(tree_obj):
        if isinstance(node, ast.FunctionDef):  # Check every function
            for arg_type in node.args.defaults:  # Check every argument type
                if isinstance(arg_type, (ast.List, ast.Set, ast.Dict)):
                    msg = 'S012 Default argument value is mutable'
                    errors.setdefault(node.lineno, []).append(msg)
                    break


def check_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        global errors, empty_lines
        errors, empty_lines = {}, 0
        for line_num, line_text in enumerate(file, start=1):  # Check every line for errors 1-9
            for func in error_functions:
                eval(func)(line_text, line_num)
        file.seek(0)
        tree = ast.parse(file.read())
        # print(ast.dump(tree, indent=3))
        for func in error_functions_ast:  # Check for errors 10-12
            eval(func)(tree)
        for n in sorted(errors):  # Sort error messages by line number
            for msg in sorted(errors[n]):  # Sort error messages by error number
                print(f'{file_path}: Line {n}: {msg}')


errors, empty_lines = {}, 0
error_functions = set(map(lambda x: 'check_00' + str(x), range(1,10)))
error_functions_ast = set(map(lambda x: 'check_0' + str(x), range(10,13)))

path = sys.argv[1]
if os.path.isfile(path):
    check_file(path)
elif os.path.isdir(path):
    for file_name in sorted(os.listdir(path)):
        if file_name.endswith('.py') and file_name != 'tests.py':
            check_file(os.path.join(path, file_name))
else:
    print('Unknown file or directory path.')

