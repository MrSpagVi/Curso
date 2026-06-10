with open("docs/etapas/etapa-33-schmitt-concepto-politico.md", "r", encoding="utf-8") as f:
    content = f.read()

for idx, line in enumerate(content.splitlines(), 1):
    if "Etapa" in line or "etapa" in line:
        print(f"Line {idx}: {line}")
