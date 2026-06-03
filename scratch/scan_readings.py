import os
import re

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]
files.sort()

print(f"Total files found: {len(files)}")

pattern_meta = re.compile(r'<span>:material-book-[^>]*>([^<]+)</span>')
pattern_header = re.compile(r'^##\s+(Justificación.*)', re.IGNORECASE | re.MULTILINE)

report = []

for file in files:
    path = os.path.join(etapas_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Get title
    title_match = re.search(r'^title:\s*"(.*?)"', content, re.MULTILINE)
    title = title_match.group(1) if title_match else file
    
    # Get meta type
    meta_matches = pattern_meta.findall(content)
    meta_type = meta_matches[-1] if meta_matches else "Unknown"
    if "Libro" in content and "selección" in content.lower() or "caps." in content.lower() or "cap." in content.lower():
        is_selection = True
    elif "Selección" in content or "selección" in content:
        is_selection = True
    else:
        is_selection = False
        
    has_justification = bool(pattern_header.search(content))
    
    report.append({
        "file": file,
        "title": title,
        "meta_type": meta_type,
        "is_selection": is_selection,
        "has_justification": has_justification,
        "content_length": len(content)
    })

# Print overview
print(f"{'File':<45} | {'Meta Type':<25} | {'Selection?':<10} | {'Justification?':<15}")
print("-" * 105)
for r in report:
    if r["is_selection"] or r["has_justification"]:
        print(f"{r['file']:<45} | {r['meta_type']:<25} | {str(r['is_selection']):<10} | {str(r['has_justification']):<15}")
