# Read build_dashboard.py and exec it, catching UnicodeEncodeError
with open(r"scratch\build_dashboard.py", "r", encoding="utf-8") as f:
    code = f.read()

# Let's remove the writing part from code to avoid writing it
code_lines = code.split("\n")
# Find line with f.write(html_template)
write_line_idx = -1
for i, line in enumerate(code_lines):
    if "f.write(html_template)" in line:
        write_line_idx = i
        break

if write_line_idx != -1:
    # Let's replace the write line with a print or custom inspection while keeping indentation
    indentation = len(code_lines[write_line_idx]) - len(code_lines[write_line_idx].lstrip())
    code_lines[write_line_idx] = (" " * indentation) + "raise Exception('inspect_template', html_template)"

code_to_exec = "\n".join(code_lines)

try:
    exec(code_to_exec, {})
except Exception as e:
    if e.args[0] == 'inspect_template':
        html_template = e.args[1]
        print("Successfully intercepted html_template.")
        # Let's try to encode it to utf-8 and catch the UnicodeEncodeError
        try:
            html_template.encode('utf-8')
            print("Encoding succeeded in exec environment!")
        except UnicodeEncodeError as uee:
            print(f"Caught UnicodeEncodeError: {uee}")
            pos = uee.start
            print(f"Error start: {pos}, end: {uee.end}")
            # Let's print the character and surrounding context safely using ascii()
            char = html_template[pos]
            print(f"Character at {pos}: {ascii(char)}")
            print(f"Context: {ascii(html_template[max(0, pos-100):pos+100])}")
            # Is it a surrogate?
            print(f"Is surrogate: {0xd800 <= ord(char) <= 0xdfff}")
    else:
        import traceback
        traceback.print_exc()

