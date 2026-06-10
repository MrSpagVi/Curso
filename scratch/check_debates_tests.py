with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines, 1):
    if "REQ2-T27" in line or "Debates Section" in line:
        print(f"Match at Line {idx}: {line.strip()}")
        for j in range(idx - 1, min(len(lines), idx + 25)):
            print(f"{j+1}: {lines[j]}")
        print("=" * 60)
