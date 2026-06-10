import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = os.listdir(etapas_dir)
stages = []
for f in files:
    m = re.search(r'etapa-(\d+)-', f)
    if m:
        stages.append(int(m.group(1)))

stages.sort()
print(f"Total stage files found: {len(stages)}")
missing = [i for i in range(1, 104) if i not in stages]
if missing:
    print(f"Missing stages: {missing}")
else:
    print("All 103 stages are fully populated and exist on disk!")
