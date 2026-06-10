import zlib, re, sys

path = sys.argv[1]
data = open(path, 'rb').read()
streams = re.findall(rb'stream\r?\n(.*?)endstream', data, re.S)
out = []
for s in streams:
    try:
        out.append(zlib.decompress(s))
    except Exception:
        pass
text = b'\n'.join(out)
chunks = re.findall(rb'\((?:[^()\\]|\\.)*\)', text)
joined = b' '.join(c[1:-1] for c in chunks)
joined = joined.replace(b'\\(', b'(').replace(b'\\)', b')')
sys.stdout.buffer.write(joined.decode('latin-1', 'replace').encode('utf-8', 'replace'))
