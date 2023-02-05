# Static Code Analyzer: Stage 1/5
# https://hyperskill.org/projects/112/stages/609/implement

with open(input(), "r", encoding="utf-8") as file:
    for n, line in enumerate(file, start=1):
        if len(line) > 79:
            print(f'Line {n}: S001 Too long')
