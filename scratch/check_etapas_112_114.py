# -*- coding: utf-8 -*-
import json, re, io, os

base = r"C:\Users\vicen\Documents\Libros Politica - Copy\scratch\research"
for n in ("112", "113", "114"):
    p = os.path.join(base, "etapa-%s.json" % n)
    with io.open(p, encoding="utf-8") as f:
        raw = f.read()
    try:
        d = json.loads(raw)
    except Exception as e:
        print(p, "FAIL", e)
        continue
    bad = re.findall(u"[áéíóúÁÉÍÓÚü]", raw)
    emoji = [c for c in raw if ord(c) > 0x2100]
    dd = d["debate_deep"]
    intro_w = len(dd["intro"].split())
    contr_w = len(dd["contrasts"].split())
    soc_w = len(d["socratic"].split())
    print(p, "OK | supporters:", len(dd["supporters"]), "critics:", len(dd["critics"]),
          "sources:", len(dd["sources"]), "| intro:", intro_w, "w contrasts:", contr_w,
          "w socratic:", soc_w, "w | tildes:", bad or "ninguna", "| emojis:", emoji or "ninguno")
    for v in dd["supporters"] + dd["critics"]:
        assert set(v.keys()) == {"school", "view"}, v.keys()
    for s in dd["sources"]:
        assert set(s.keys()) == {"label", "url"}, s.keys()
print("estructura interna OK")
