import os
import re

# Reconstruct shift_map from expand_syllabus.py
shift_map = {}
for i in range(1, 18):
    shift_map[i] = i
shift_map[18] = 19
shift_map[19] = 20
shift_map[20] = 22
shift_map[21] = 23
shift_map[22] = 25
shift_map[23] = 26
shift_map[24] = 27
shift_map[25] = 29
shift_map[26] = 30
shift_map[27] = 31
shift_map[28] = 34
shift_map[29] = 35
shift_map[30] = 37
shift_map[31] = 39
shift_map[32] = 40
shift_map[33] = 41
shift_map[34] = 43
shift_map[35] = 44
for i in range(36, 50):
    shift_map[i] = i + 12
for i in range(50, 53):
    shift_map[i] = i + 13
for i in range(53, 58):
    shift_map[i] = i + 13
for i in range(58, 75):
    shift_map[i] = i + 15
for i in range(75, 88):
    shift_map[i] = i + 16

path_mejoras = r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\mejoras_academicas.md"
with open(path_mejoras, "r", encoding="utf-8") as f:
    content = f.read()

# Replace references like **Etapa XX** or Etapa XX
# We'll use a regex that matches "Etapa XX" case-insensitively and updates the number
def replace_text_match(match):
    prefix = match.group(1) # e.g. "Etapa "
    num_str = match.group(2) # e.g. "21"
    num = int(num_str)
    if num in shift_map:
        new_num = shift_map[num]
        return f"{prefix}{new_num}"
    return match.group(0)

# Matches "Etapa 21", "etapa 21", "Etapa 23", etc.
pattern = re.compile(r'\b(Etapa\s+|etapa\s+)(\d{1,2})\b')

new_content, count = pattern.subn(replace_text_match, content)

# Write back
if count > 0:
    with open(path_mejoras, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {count} text stage mentions in {os.path.basename(path_mejoras)}")
else:
    print("No matches found in mejoras_academicas.md")
