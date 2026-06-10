with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines, 1):
    if "CF-1" in line:
        s = f"Match at Line {idx}: {repr(line.strip())}"
        print(s.encode('ascii', 'backslashreplace').decode('ascii'))
        for j in range(idx - 1, min(len(lines), idx + 50)):
            sj = f"{j+1}: {repr(lines[j])}"
            print(sj.encode('ascii', 'backslashreplace').decode('ascii'))
        print("=" * 60)
