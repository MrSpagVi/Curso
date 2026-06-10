with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines, 1):
    if "F5-T24" in line or "F5-T25" in line or "F4-T22" in line or "F4-T23" in line:
        print(f"Match at Line {idx}: {line.strip()}")
        for j in range(idx - 1, min(len(lines), idx + 25)):
            print(f"{j+1}: {lines[j]}")
        print("=" * 60)
