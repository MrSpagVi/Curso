"""Regenera el array ETAPAS[] de extra.js tras insertar Hegel (etapa 22).

NO auto-cuenta checkboxes: algunos archivos tienen checkboxes de RUBRICA
(criterios de autoevaluacion) que el total original excluia a proposito
(ej. tesina-final: 6 tareas, no las 8 de la rubrica). Por eso usamos los
totales originales curados + las modificaciones de esta iteracion.

Transformacion:
- etapas 1-21: igual (Pocock 19 +1 por Steelman)
- nueva etapa 22: Hegel (5 tareas)
- etapas viejas 22-84 -> nuevas 23-85, mismo total salvo las editadas (+1)
"""
import re
import pathlib

EXTRA_JS = pathlib.Path("docs/assets/javascripts/extra.js")

# (old_number, slug_suffix, original_total) — copia fiel del array previo
OLD = [
    (1, "setup-sistema-de-notas", 6), (2, "tutorial-tomar-notas", 4),
    (3, "adler-como-leer-un-libro", 5), (4, "schopenhauer-arte-tener-razon", 4),
    (5, "crashcourse-falacias", 4), (6, "manual-falacias", 5),
    (7, "platon-apologia", 4), (8, "aristoteles-politica", 4),
    (9, "maquiavelo-principe", 5), (10, "yale-maquiavelo", 3),
    (11, "hobbes-leviatan", 5), (12, "yale-hobbes", 3),
    (13, "rousseau-contrato-social", 5), (14, "yale-rousseau", 3),
    (15, "mill-sobre-la-libertad", 5), (16, "sandel-justice", 3),
    (17, "locke-segundo-tratado", 5), (18, "tocqueville-democracia-en-america", 5),
    (19, "pocock-momento-maquiavelico", 5), (20, "chang-economia-99", 4),
    (21, "smith-riqueza-naciones", 5), (22, "marx-capital", 5),
    (23, "harvey-reading-marx", 3), (24, "mariategui-7-ensayos", 4),
    (25, "weber-politica-vocacion", 4), (26, "foucault", 5),
    (27, "rawls-teoria-justicia", 5), (28, "berlin-dos-conceptos", 4),
    (29, "habermas-esfera-publica", 4), (30, "lenin-imperialismo", 4),
    (31, "gramsci-cuadernos", 5), (32, "hayek-camino-servidumbre", 4),
    (33, "popper-sociedad-abierta", 5), (34, "nozick-anarquia-estado-utopia", 4),
    (35, "bolivar-carta-jamaica", 4), (36, "marti-nuestra-america", 4),
    (37, "rodo-ariel", 4), (38, "vasconcelos-raza-cosmica", 4),
    (39, "paz-laberinto-soledad", 5), (40, "galeano-venas-abiertas", 5),
    (41, "bueno-mito-izquierda", 5), (42, "echeverria-modernidad-blanquitud", 4),
    (43, "dussel-1492", 5), (44, "quijano-colonialidad", 3),
    (45, "cusicanqui-chixinakax", 4), (46, "freire-pedagogia-oprimido", 5),
    (47, "gutierrez-teologia-liberacion", 4), (48, "gonzalez-feminismo-afrolatinoamericano", 3),
    (49, "lugones-heterosexualismo", 3), (50, "gago-potencia-feminista", 4),
    (51, "segato-guerra-mujeres", 4), (52, "wallerstein-sistemas-mundo", 4),
    (53, "mearsheimer-great-power", 5), (54, "agamben", 4),
    (55, "mbembe-necropolitica", 4), (56, "novela-politica", 3),
    (57, "relectura-activa", 3), (58, "gandhi-hind-swaraj", 4),
    (59, "confucio-analectas", 4), (60, "sen-identidad-violencia", 4),
    (61, "hardt-negri-imperio", 5), (62, "wang-hui", 4),
    (63, "maruyama", 4), (64, "ambedkar-annihilation-caste", 4),
    (65, "ensayo-final", 5), (66, "grabacion-final", 4),
    (67, "marshall-ciudadania", 4), (68, "polanyi-gran-transformacion", 5),
    (69, "esping-andersen", 4), (70, "filgueira-universalismo-basico", 4),
    (71, "tesina-m5", 5), (72, "williams-marxismo-literatura", 4),
    (73, "benjamin-obra-arte", 4), (74, "bourdieu-distincion", 5),
    (75, "hall-encoding-decoding", 3), (76, "garcia-canclini-culturas-hibridas", 4),
    (77, "martin-barbero", 4), (78, "zuboff-vigilancia", 5),
    (79, "ensayo-neoliberalismo", 4), (80, "ensayo-ciudadania", 4),
    (81, "ensayo-trabajo", 4), (82, "ensayo-estado", 4),
    (83, "ensayo-desigualdad", 4), (84, "tesina-final", 6),
]

# Etapas que ganaron +1 checkbox esta iteracion (por NUMERO VIEJO)
PLUS_ONE = {19, 24, 27, 29, 34, 51, 64}  # Pocock, Mariategui, Rawls(Kymlicka), Habermas(Fraser), Nozick, Segato, Ambedkar

new_rows = []
for num, suffix, total in OLD:
    t = total + 1 if num in PLUS_ONE else total
    if num < 22:
        new_rows.append((f"etapa-{num:02d}-{suffix}", t))
    else:
        if num == 22:  # insertar Hegel justo antes del viejo 22 (Marx)
            new_rows.append(("etapa-22-hegel-fenomenologia", 5))
        new_rows.append((f"etapa-{num + 1:02d}-{suffix}", t))

lines = ["  const ETAPAS = ["]
for slug, total in new_rows:
    lines.append(f"    {{ slug: '{slug}', total: {total} }},")
lines.append("  ];")
block = "\n".join(lines)

js = EXTRA_JS.read_text(encoding="utf-8")
new_js, n = re.subn(r"  const ETAPAS = \[.*?\];", lambda m: block, js, count=1, flags=re.DOTALL)
assert n == 1, f"esperaba reemplazar 1 array, reemplace {n}"
EXTRA_JS.write_text(new_js, encoding="utf-8")
print(f"ETAPAS[] regenerado: {len(new_rows)} etapas, {sum(t for _, t in new_rows)} checkboxes totales")
