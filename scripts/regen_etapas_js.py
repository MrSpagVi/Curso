import os
import re
import pathlib

EXTRA_JS = pathlib.Path("docs/assets/javascripts/extra.js")
docs_dir = pathlib.Path("docs/etapas")

stage_files = sorted([f for f in os.listdir(docs_dir) if f.startswith("etapa-") and f.endswith(".md")])

def get_phase(num):
    if 1 <= num <= 6:
        return 0 # Fase 0
    elif 7 <= num <= 19:
        return 1 # Fase 1
    elif 20 <= num <= 25:
        return 2 # Fase 2
    elif 26 <= num <= 35:
        return 3 # Fase 3
    elif 36 <= num <= 52:
        return 4 # Fase 4
    elif 53 <= num <= 69:
        return 5 # Fase 5
    elif 70 <= num <= 74:
        return 6 # M5
    elif 75 <= num <= 81:
        return 7 # M6
    elif 82 <= num <= 87:
        return 8 # Cierre
    return -1

new_rows = []
for filename in stage_files:
    slug = filename[:-3]
    path = docs_dir / filename
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    num_match = re.match(r"^etapa-(\d+)-", filename)
    num = int(num_match.group(1)) if num_match else -1
    
    # Extract title
    title = ""
    fm_match = re.search(r"^---\s*\ntitle:\s*[\"'](.*?)[\"']\s*\n---", content, re.MULTILINE)
    if fm_match:
        title = fm_match.group(1)
    else:
        h1_match = re.search(r"^#\s+(.*)$", content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1)
            
    title_clean = re.sub(r"^(Etapa\s+\d+\s*[-—–:]\s*|\d+\s*·\s*)", "", title).strip()
    title_clean = title_clean.replace("'", "\\'") # escape single quotes for js string
    
    # Count checklists in ## Tareas
    tareas_match = re.search(r"## Tareas\n(.*?)(?=\n## |\Z)", content, re.DOTALL | re.IGNORECASE)
    cbs = 0
    if tareas_match:
        cbs = len(re.findall(r"-\s*\[\s*\]", tareas_match.group(1)))
        
    new_rows.append({
        "slug": slug,
        "total": cbs,
        "title": title_clean,
        "phase": get_phase(num)
    })

lines = ["  const ETAPAS = ["]
for r in new_rows:
    lines.append(f"    {{ slug: '{r['slug']}', total: {r['total']}, title: '{r['title']}', phase: {r['phase']} }},")
lines.append("  ];")
block = "\n".join(lines)

js = EXTRA_JS.read_text(encoding="utf-8")
new_js, n = re.subn(r"  const ETAPAS = \[.*?\];", lambda m: block, js, count=1, flags=re.DOTALL)
assert n == 1, f"expected to replace 1 array block, replaced {n}"
EXTRA_JS.write_text(new_js, encoding="utf-8")
print(f"ETAPAS[] regenerated successfully: {len(new_rows)} stages.")
