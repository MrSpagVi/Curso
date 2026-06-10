import json, re, io

base = r"c:\Users\vicen\Documents\Libros Politica - Copy\scratch\research"
for n in (115, 116, 117):
    p = base + r"\etapa-%d.json" % n
    with io.open(p, encoding="utf-8") as f:
        data = json.load(f)
    txt = json.dumps(data, ensure_ascii=False)
    accents = re.findall(u"[áéíóúÁÉÍÓÚü]", txt)
    emojis = [c for c in txt if ord(c) > 0x2100]
    dd = data["debate_deep"]
    print("etapa-%d.json OK | supporters=%d critics=%d sources=%d | tildes=%d emojis=%d"
          % (n, len(dd["supporters"]), len(dd["critics"]), len(dd["sources"]), len(accents), len(emojis)))
    assert "socratic" in data
