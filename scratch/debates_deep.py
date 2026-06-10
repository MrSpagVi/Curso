# -*- coding: utf-8 -*-
"""
Debates de post-lectura INVESTIGADOS (investigacion web profunda) por etapa.

FUENTE DE VERDAD: un archivo JSON por etapa en scratch/research/etapa-NN.json.
Este modulo solo los carga y arma DEBATES_DEEP (clave = numero de etapa int).

Cada JSON:
- debate_deep: { intro, supporters[{school,view}], critics[{school,view}], contrasts, sources[{label,url}] }
- socratic: prompt copiable para usar con cualquier LLM.

Sin emojis. Spanish academico. Se llena de forma incremental, un lote por sesion.
"""

import json
import os
import re

_RESEARCH_DIR = os.path.join(os.path.dirname(__file__), "research")
_FNAME_RE = re.compile(r"etapa-(\d+)\.json$")


def _load_all():
    out = {}
    if not os.path.isdir(_RESEARCH_DIR):
        return out
    for fn in sorted(os.listdir(_RESEARCH_DIR)):
        m = _FNAME_RE.search(fn)
        if not m:
            continue
        stage = int(m.group(1))
        path = os.path.join(_RESEARCH_DIR, fn)
        try:
            with open(path, encoding="utf-8") as f:
                out[stage] = json.load(f)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"debates_deep: no pude cargar {fn}: {e}")
    return out


DEBATES_DEEP = _load_all()
