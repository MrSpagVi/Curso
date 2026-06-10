import io, sys
from pypdf import PdfReader

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import sys as _s
path = _s.argv[1] if len(_s.argv) > 1 else r"C:\Users\vicen\.claude\projects\c--Users-vicen-Documents-Libros-Politica---Copy\e1e242dc-a222-4ee4-9912-209f9c65131f\tool-results\webfetch-1781037191957-rf5x7a.pdf"
r = PdfReader(path)
print("pages:", len(r.pages))
for i, p in enumerate(r.pages):
    print(f"--- PAGE {i+1} ---")
    print(p.extract_text())
