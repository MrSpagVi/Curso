import os
import re

targets = {
    "etapa-18-constant-libertad.md": "Etapa 18",
    "etapa-19-tocqueville-democracia-en-america.md": "Etapa 19",
    "etapa-40-gramsci-cuadernos.md": "Etapa 40",
    "etapa-68-agamben.md": "Etapa 68",
    "etapa-69-fanon-condenados-tierra.md": "Etapa 69",
    "etapa-72-chibber-teoria-poscolonial.md": "Etapa 72",
    "etapa-73-mbembe-necropolitica.md": "Etapa 73"
}

etapas_dir = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas"
all_passed = True

for filename, expected_title in targets.items():
    path = os.path.join(etapas_dir, filename)
    if not os.path.exists(path):
        print(f"FAIL: {filename} does not exist!")
        all_passed = False
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check both the frontmatter/first header and the text content
    if expected_title not in content:
        print(f"FAIL: {filename} does not contain '{expected_title}' in its content!")
        all_passed = False
    else:
        # Check if the wrong title numbers are still there
        wrong_titles = ["Etapa 19" if expected_title == "Etapa 18" else "",
                        "Etapa 20" if expected_title == "Etapa 19" else "",
                        "Etapa 52" if expected_title == "Etapa 40" else "",
                        "Etapa 83" if expected_title == "Etapa 68" else "",
                        "Etapa 84" if expected_title == "Etapa 69" else "",
                        "Etapa 87" if expected_title == "Etapa 72" else "",
                        "Etapa 88" if expected_title == "Etapa 73" else ""]
        wrong_titles = [w for w in wrong_titles if w]
        found_wrong = False
        for w in wrong_titles:
            # Look for exact pattern "title: "Etapa XX"" or "# Etapa XX"
            if re.search(rf'title:\s*"{w}"|#\s*{w}', content):
                print(f"FAIL: {filename} still contains wrong title reference: '{w}'")
                all_passed = False
                found_wrong = True
        if not found_wrong:
            print(f"PASS: {filename} has correct internal title '{expected_title}'")

if all_passed:
    print("ALL corrected stages are perfectly aligned internally!")
else:
    print("SOME stage title alignments failed verification.")
