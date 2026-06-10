with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

for idx, line in enumerate(content.splitlines(), 1):
    if "foucault" in line.lower():
        print(f"Line {idx}: {line.strip()}")
