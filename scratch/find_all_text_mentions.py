import os
import re
import pathlib

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

docs_root = pathlib.Path(r"c:\Users\vicen\Documents\Libros Politica - Copy\docs")
md_files = list(docs_root.glob("**/*.md"))

pattern = re.compile(r'\b(Etapa\s+|etapa\s+)(\d{1,2})\b')

total_updates = 0

for file_path in md_files:
    if file_path.name == "mejoras_academicas.md":
        # Already updated
        continue
        
    content = file_path.read_text(encoding="utf-8")
    
    def replace_text_match(match):
        prefix = match.group(1)
        num_str = match.group(2)
        num = int(num_str)
        if num in shift_map:
            new_num = shift_map[num]
            if new_num != num:
                return f"{prefix}{new_num}"
        return match.group(0)
        
    new_content, count = pattern.subn(replace_text_match, content)
    
    if count > 0:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Updated {count} text stage mentions in {file_path.name}")
        total_updates += count

print(f"Total text stage mentions updated in other files: {total_updates}")
