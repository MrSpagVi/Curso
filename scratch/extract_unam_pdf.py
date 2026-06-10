from pypdf import PdfReader

src = r"C:\Users\vicen\.claude\projects\c--Users-vicen-Documents-Libros-Politica---Copy\e1e242dc-a222-4ee4-9912-209f9c65131f\tool-results\webfetch-1781037254656-hqin8y.pdf"
out = r"C:\Users\vicen\Documents\Libros Politica - Copy\scratch\unam_pslp.txt"

r = PdfReader(src)
print("pages:", len(r.pages))
text = "\n".join(p.extract_text() or "" for p in r.pages)
with open(out, "w", encoding="utf-8") as f:
    f.write(text)
print("chars:", len(text))
