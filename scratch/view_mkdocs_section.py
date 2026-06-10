with open("mkdocs.yml", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for i in range(100, min(160, len(lines))):
    print(f"{i+1}: {lines[i]}")
