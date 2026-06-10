import sys
import unicodedata

def is_emoji(char):
    name = unicodedata.name(char, "")
    if "EMOJI" in name or "SNOWMAN" in name or "SPADE" in name or "HEART" in name:
        return True
    # Check unicode block/properties if possible
    # Emoji properties aren't directly in standard library, but we can do a range check
    codepoint = ord(char)
    # Common emoji ranges
    if 0x1F300 <= codepoint <= 0x1F9FF:
        return True
    if 0x1FA00 <= codepoint <= 0x1FAFF:
        return True
    if 0x2600 <= codepoint <= 0x26FF:
        return True
    if 0x2700 <= codepoint <= 0x27BF:
        return True
    return False

with open("dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

emojis = []
for idx, char in enumerate(content):
    if is_emoji(char):
        # Find line number
        line_num = content[:idx].count("\n") + 1
        emojis.append((line_num, char, unicodedata.name(char, "UNKNOWN")))

if emojis:
    print(f"Detected {len(emojis)} potential emojis/symbols:")
    for line, char, name in emojis[:50]:
        print(f"Line {line}: {char} ({name})")
else:
    print("Zero emojis detected via unicode name and range check.")
