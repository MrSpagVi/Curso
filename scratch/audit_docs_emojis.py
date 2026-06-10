import os
import re
import unicodedata

emoji_pattern = re.compile(
    r"[\u2700-\u27BF]|"
    r"[\uE000-\uF8FF]|"
    r"\uD83C[\uDC00-\uDFFF]|"
    r"\uD83D[\uDC00-\uDFFF]|"
    r"[\u2600-\u26FF]|"
    r"\uD83E[\uDD10-\uDDFF]|"
    r"[\U00010000-\U0010ffff]",
    flags=re.UNICODE
)

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
files = [f for f in os.listdir(etapas_dir) if f.endswith(".md")]

emojis_found = []
for file in files:
    path = os.path.join(etapas_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    for idx, line in enumerate(content.splitlines(), 1):
        matches = emoji_pattern.findall(line)
        if matches:
            emojis_found.append((file, idx, line, matches))

if emojis_found:
    print(f"FOUND {len(emojis_found)} LINES WITH EMOJIS IN SOURCE DOCS:")
    for file, idx, line, matches in emojis_found[:20]:
        print(f"{file} Line {idx}: {matches} -> {line.strip()[:100]}")
else:
    print("NO EMOJIS FOUND IN SOURCE DOCS.")
