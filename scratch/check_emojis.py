import re
import sys

# Define standard emoji pattern
emoji_pattern = re.compile(
    r"[\u2700-\u27BF]|"
    r"[\uE000-\uF8FF]|"
    r"\uD83C[\uDC00-\uDFFF]|"
    r"\uD83D[\uDC00-\uDFFF]|"
    r"[\u2600-\u26FF]|"
    r"\uD83E[\uDD10-\uDDFF]|"
    # Additional common emojis
    r"[\U00010000-\U0010ffff]",
    flags=re.UNICODE
)

with open('dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

emojis_found = []
for idx, line in enumerate(content.splitlines(), 1):
    matches = emoji_pattern.findall(line)
    if matches:
        emojis_found.append((idx, line, matches))

if emojis_found:
    print(f"FOUND {len(emojis_found)} LINES WITH EMOJIS:")
    for idx, line, matches in emojis_found[:20]:
        print(f"Line {idx}: {matches} -> {line.strip()[:100]}")
    sys.exit(1)
else:
    print("NO EMOJIS FOUND IN DASHBOARD.HTML")
    sys.exit(0)
