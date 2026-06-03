import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]
files.sort()

pattern_header = re.compile(r'^##\s+(Justificación.*)', re.IGNORECASE | re.MULTILINE)
output_path = r"c:\Users\vicen\Documents\Libros Politica - Copy\scratch\view_tasks_output.txt"

with open(output_path, "w", encoding="utf-8") as out:
    for file in files:
        path = os.path.join(etapas_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check if has justification
        if pattern_header.search(content):
            continue
            
        tareas_match = re.search(r'## Tareas(.*?)(##|$)', content, re.DOTALL)
        if tareas_match:
            tareas_text = tareas_match.group(1).strip()
            low = tareas_text.lower()
            # if contains any keywords indicating it's a selective reading
            if any(k in low for k in ["selección", "cap.", "caps", "capítulo", "sección", "omitir", "leer de la"]):
                out.write("="*60 + "\n")
                out.write(f"File: {file}\n")
                out.write(tareas_text + "\n")
                out.write("="*60 + "\n\n")

print("Done writing report to scratch/view_tasks_output.txt")
