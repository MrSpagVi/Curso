with open("scratch/build_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

# Search for how debates and growth sections are defined or if they are parsed/generated
for idx, line in enumerate(content.splitlines(), 1):
    if any(author in line for author in ["Gramsci", "Althusser", "Agamben", "Butler", "Fanon", "Mbembe"]):
        print(f"Line {idx}: {line.strip()}")
