import json
import re
from pathlib import Path

def run_audit():
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

    all_target_stages = set(range(1, 104))
    mapped_target_stages = set(shift_map.values())
    unmapped_target_stages = all_target_stages - mapped_target_stages
    
    print("New stages added in the 103 version (not in original 87):")
    print(sorted(list(unmapped_target_stages)))
    
    # Get details of these new stages from dashboard.html
    dash_path = Path('dashboard.html')
    content = dash_path.read_text(encoding='utf-8')
    match = re.search(r'const COURSE_DATA = (\[.*?\]);', content, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            new_stage_details = [s for s in data if s['stage'] in unmapped_target_stages]
            for s in sorted(new_stage_details, key=lambda x: x['stage']):
                print(f"Stage {s['stage']}: {s['title']} ({s['phase_name']})")
        except Exception as e:
            print("Error parsing JSON:", e)

if __name__ == "__main__":
    run_audit()
