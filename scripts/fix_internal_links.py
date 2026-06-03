import os
import re
import pathlib

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

# We want to replace links like etapa-XX- with etapa-YY-
# Let's find all md files in docs/
docs_root = pathlib.Path(r"c:\Users\vicen\Documents\Libros Politica - Copy\docs")
md_files = list(docs_root.glob("**/*.md"))

print(f"Found {len(md_files)} markdown files to scan and fix.")

# Regex to match etapa-XX- or etapa-X- in links or text
# e.g., (etapa-27-foucault.md) -> (etapa-31-foucault.md)
link_pattern = re.compile(r'etapa-(\d{1,2})-')

total_replacements = 0

for file_path in md_files:
    content = file_path.read_text(encoding="utf-8")
    
    # We want to be careful and find all occurrences of 'etapa-XX-'
    # If the file name itself is etapa-YY-..., we don't want to break it, but replacing it is fine since it's already renamed.
    # Actually, replacing all occurrences of etapa-XX- with the new stage number is correct because if a file was renamed, its internal references should also point to the new numbers.
    
    new_content = content
    matches = sorted(list(set(link_pattern.findall(content))), key=lambda x: len(x), reverse=True)
    
    file_replacements = 0
    
    # We will replace in reverse order of old numbers to avoid partial replacement collision (e.g. 8 replacing in 87 if we are not careful, but the regex match of digits solves this).
    # To be extremely precise, we can find all matches of the pattern, check if the number is in shift_map, and replace "etapa-XX-" with "etapa-YY-".
    
    def replace_match(match):
        old_num = int(match.group(1))
        if old_num in shift_map:
            new_num = shift_map[old_num]
            return f"etapa-{new_num:02d}-"
        return match.group(0)
        
    new_content, count = link_pattern.subn(replace_match, content)
    
    if count > 0:
        file_path.write_text(new_content, encoding="utf-8")
        print(f"Fixed {count} link references in: {file_path.name}")
        total_replacements += count

print(f"Link fix complete. Total references updated: {total_replacements}")
