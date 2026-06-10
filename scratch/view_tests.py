with open("tests/runner.html", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for test cases F5-T24 and F5-T25
import re
pattern = re.compile(r'it\("(?:F5-T24|F5-T25|F5-T|BC-F5-23).*?"\s*,\s*(?:async\s*)?\(\)\s*=>\s*\{.*?\n\s*\}\);', re.DOTALL)
matches = pattern.findall(content)
for m in matches:
    print(m)
    print("-" * 50)
