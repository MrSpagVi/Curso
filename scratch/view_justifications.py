import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]
files.sort()

output_path = r"c:\Users\vicen\Documents\Libros Politica - Copy\scratch\current_justifications.txt"

with open(output_path, "w", encoding="utf-8") as out:
    for file in files:
        path = os.path.join(etapas_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        just_match = re.search(r'## Justificación(.*?)(## Tareas|## Tareas|## Tareas|$)', content, re.DOTALL | re.IGNORECASE)
        if just_match:
            out.write("="*60 + "\n")
            out.write(f"File: {file}\n")
            out.write("## Justificación" + just_match.group(1).strip() + "\n")
            out.write("="*60 + "\n\n")

print("Done writing current justifications to scratch/current_justifications.txt")
