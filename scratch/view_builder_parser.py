with open("scratch/build_dashboard.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
funcs = re.findall(r'def \w+\(.*?\):', content)
for f in funcs:
    print(f)
