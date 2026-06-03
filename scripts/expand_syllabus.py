import re
import os
import pathlib

DOCS_DIR = pathlib.Path(r"c:\Users\vicen\Documents\Libros Politica - Copy\docs\etapas")

# Mapping of original stage number to new stage number
shift_map = {}
# Fill in the mapping
# 1 to 17 remain 1 to 17
for i in range(1, 18):
    shift_map[i] = i

# 18-19 shift +1
shift_map[18] = 19
shift_map[19] = 20

# 20-21 shift +2
shift_map[20] = 22
shift_map[21] = 23

# 22-24 shift +3
shift_map[22] = 25
shift_map[23] = 26
shift_map[24] = 27

# 25-27 shift +4
shift_map[25] = 29
shift_map[26] = 30
shift_map[27] = 31

# 28-29 shift +6
shift_map[28] = 34
shift_map[29] = 35

# 30 shift +7
shift_map[30] = 37

# 31-33 shift +8
shift_map[31] = 39
shift_map[32] = 40
shift_map[33] = 41

# 34-35 shift +9
shift_map[34] = 43
shift_map[35] = 44

# 36-49 shift +12
for i in range(36, 50):
    shift_map[i] = i + 12

# 50-52 shift +13
for i in range(50, 53):
    shift_map[i] = i + 13

# 53-57 shift +13
for i in range(53, 58):
    shift_map[i] = i + 13

# 58-74 shift +15
for i in range(58, 75):
    shift_map[i] = i + 15

# 75-87 shift +16
for i in range(75, 88):
    shift_map[i] = i + 16

# Verify mapping is complete and has no collisions
assert len(shift_map) == 87
assert len(set(shift_map.values())) == 87

print("Syllabus Shifting Script Loaded.")

# Rename existing files in reverse order to avoid collisions
for old_num in sorted(shift_map.keys(), reverse=True):
    new_num = shift_map[old_num]
    if old_num == new_num:
        continue
        
    pattern = f"etapa-{old_num:02d}-*.md"
    matches = list(DOCS_DIR.glob(pattern))
    if not matches:
        print(f"[WARN] No file found for stage {old_num}")
        continue
    old_file = matches[0]
    
    old_name = old_file.name
    new_name = old_name.replace(f"etapa-{old_num:02d}-", f"etapa-{new_num:02d}-")
    new_file = old_file.parent / new_name
    
    content = old_file.read_text(encoding="utf-8")
    
    # Internal updates
    # Update title
    content = content.replace(f"Etapa {old_num} —", f"Etapa {new_num} —")
    content = content.replace(f"Etapa {old_num:02d} —", f"Etapa {new_num} —")
    # Update checklist indicators
    content = re.sub(r"Etapa (\d+)/87", f"Etapa {new_num}/103", content)
    content = re.sub(r"Etapa (\d+)/85", f"Etapa {new_num}/103", content)
    content = re.sub(r"Etapa (\d+)/103", f"Etapa {new_num}/103", content)
    # Update progress global indicators
    content = re.sub(r"Progreso global \(\d+ etapas\)", "Progreso global (103 etapas)", content)
    # Write and delete old
    new_file.write_text(content, encoding="utf-8")
    old_file.unlink()
    print(f"Shifted: {old_name} -> {new_name}")

print("\nExisting stages shifted successfully.")
