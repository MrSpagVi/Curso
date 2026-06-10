with open("mkdocs.yml", "r", encoding="utf-8") as f:
    content = f.read()

for idx, line in enumerate(content.splitlines(), 1):
    if "schmitt" in line.lower() or "etapa-33" in line.lower() or "etapa-41" in line.lower():
        print(f"Line {idx}: {line.strip()}")
