import os

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]

found_any = False
for file in files:
    path = os.path.join(etapas_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if "Debates" in content or "Crecimiento" in content or "Contrastes" in content:
        print(f"Match in {file}")
        found_any = True

if not found_any:
    print("No markdown stage files contain Debates, Crecimiento, or Contrastes keywords.")
