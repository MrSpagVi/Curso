with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines):
    if "REQ1-T26" in line:
        print(f"=== Match at Line {idx+1} ===")
        for j in range(max(0, idx-5), min(len(lines), idx+30)):
            print(f"{j+1}: {lines[j]}")
