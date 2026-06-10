with open("scratch/build_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

lines = content.splitlines()
# Let's search for "for" loops that iterate over doc/etapas or listdir
for idx, line in enumerate(lines):
    if "listdir" in line or "os.walk" in line or "etapas_dir" in line:
        print(f"=== Match at Line {idx+1} ===")
        for j in range(max(0, idx-5), min(len(lines), idx+30)):
            print(f"{j+1}: {lines[j]}")
