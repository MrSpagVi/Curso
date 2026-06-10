with open("docs/etapas/etapa-33-schmitt-concepto-politico.md", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
for idx, line in enumerate(lines):
    if any(q in line.lower() for q in ["foucault", "etapa 31", "etapa-31"]):
        print(f"Line {idx+1}: {line}")
