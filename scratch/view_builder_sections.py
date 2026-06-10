with open("scratch/build_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines, 1):
    if "debates-contrasts-section" in line or "debatesHtml" in line or "growthHtml" in line:
        print(f"Match in build_dashboard.py at Line {idx}: {line.strip()}")
