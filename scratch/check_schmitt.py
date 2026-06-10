with open("docs/etapas/etapa-33-schmitt-concepto-politico.md", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Let's find occurrences of Foucault, Agamben, and Mbembe in this file and print the lines
lines = content.splitlines()
for idx, line in enumerate(lines):
    if any(name in line for name in ["Foucault", "Agamben", "Mbembe"]):
        print(f"Line {idx+1}: {line}")
