# Static Code Analyzer: Stage 2/5
# https://hyperskill.org/projects/112/stages/610/implement
# import re


def check_001(string):
    return len(string) > 79


def check_002(string):
    return (len(string) - len(string.lstrip(' '))) % 4
    # return re.search('^(?!^( {4})*[^ ])', string)  # Negative lookahead


def check_003(string):
    return string.split('#')[0].strip().endswith(';')
    # return re.search(r'^[^#]*;(?!\S)', string)  # Negative lookahead


def check_004(string):
    return not string.startswith('#') and '#' in string and '  #' not in string
    # return re.search('^[^#]*[^ ] ?#', string)


def check_005(string):
    return '#' in string and string.find('#') < string.lower().find('todo')
    # return re.search('(?i)# *TODO', string)  # (?i) ignores case in lookahead


def check_006(string):
    global empty_lines
    if string == '\n':
        empty_lines += 1
    elif empty_lines > 2:
        empty_lines = 0
        return True


empty_lines = 0
error_list = {
    'S001': (check_001, 'Too long'),
    'S002': (check_002, 'Indentation is not a multiple of four'),
    'S003': (check_003, 'Unnecessary semicolon'),
    'S004': (check_004, 'At least two spaces required before inline'),
    'S005': (check_005, 'TODO found'),
    'S006': (check_006, 'More than two blank lines preceding a code line')}


with open(input(), "r", encoding="utf-8") as file:
    for line_num, line in enumerate(file, start=1):
        for error_num in error_list:
            if error_list[error_num][0](line):
                print(f'Line {line_num}: {error_num} {error_list[error_num][1]}')

