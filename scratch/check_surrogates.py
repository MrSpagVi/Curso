import re

path = r"c:\Users\vicen\Documents\Libros Politica - Copy\scratch\build_dashboard.py"
with open(path, "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

surrogate_re = re.compile(r'[\ud800-\udfff]')
for m in surrogate_re.finditer(content):
    print(f"File has surrogate at {m.start()}: {repr(content[max(0, m.start()-50):m.end()+50])}")

