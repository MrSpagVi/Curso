with open("dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

for idx, line in enumerate(content.splitlines(), 1):
    if "localStorage" in line:
        print(f"Line {idx}: {line.strip()}")
