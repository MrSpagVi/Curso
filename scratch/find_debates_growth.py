with open("dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines, 1):
    if "debates-contrasts-section" in line or "growth-application-section" in line:
        print(f"Match at Line {idx}: {line.strip()}")
        # Print subsequent 30 lines
        for j in range(idx - 2, min(len(lines), idx + 35)):
            print(f"{j+1}: {lines[j]}")
        print("=" * 60)
