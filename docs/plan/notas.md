---
title: Sistema de notas
---

# Sistema de notas

> La diferencia entre "leí muchos libros" y "aprendí de ellos" es exactamente esto. Sin sistema de notas, en 12 meses recordarás el 10% de lo leído. Con sistema, el conocimiento **compounding**: cada libro nuevo te da más porque dialoga con los anteriores que tienes archivados.

---

## :material-target: Por qué importa especialmente en tu caso

Tres condiciones específicas tuyas hacen esto crítico:

1. **Lees en ebook** — no puedes anotar márgenes físicos. Necesitas un workflow digital deliberado.
2. **70+ autores en 28 meses** — el volumen es alto. Sin sistema, los últimos meses olvidas los primeros.
3. **Quieres pensar, no solo leer** — el objetivo del plan es producir un ensayo propio en F5 y haberlo formado tu criterio. Eso requiere **archivar tus propias ideas**, no las ajenas.

---

## :material-school: El sistema híbrido: Zettelkasten + Adler + Anki

Tras investigar Zettelkasten (Luhmann/Ahrens), PARA (Forte), Cornell, Anki, los notebooks de Benjamin/Arendt/Wittgenstein/Barthes, y workflows de doctorandos en humanidades, lo que **mejor te sirve** es una versión disciplinada del Zettelkasten + lectura analítica de Adler + Anki quirúrgico. **No es marketing — es lo que hacen los doctorandos serios en filosofía hoy.**

### Los 4 tipos de notas

| Tipo | Qué es | Cuándo se crea | Dónde vive |
|------|--------|-----------------|-------------|
| **Fleeting** (al vuelo) | Idea suelta capturada mientras lees, ves vídeo, paseas. Texto rápido y desechable. | En cualquier momento | App móvil / inbox |
| **Literature** (de lectura) | Notas SOBRE el libro: lo que **dice el autor**, citado con página, en frases cortas con tus palabras. Una por libro o por capítulo. | Al terminar la sesión de lectura | `lecturas/<autor>-<titulo>.md` |
| **Permanent** (permanente) ⭐ | **Lo que TÚ piensas**, no lo que dice el autor. Una idea atómica autosuficiente, título declarativo, enlazada a otras notas permanentes. | Al destilar literature notes | `permanent/` o `conceptos/` |
| **Structure / Index** | Mapa que conecta varias permanent notes sobre un tema. Es donde ocurre el pensamiento sintópico (varios autores sobre un mismo problema). | Cuando ya tienes 5-10 permanents sobre un tema | `mapas/` |

**La regla crítica:** una literature note dice "Marx argumenta que..." (con cita). Una permanent note dice "**El velo de ignorancia presupone un sujeto desencarnado que la crítica feminista refuta**" — sin "Rawls dice", sin "según...", sino tu posición. **Sin esta distinción, el sistema no funciona.**

### Por qué este sistema y no otros

- **PARA de Tiago Forte** (Projects/Areas/Resources/Archives): bueno para knowledge workers corporativos, **mediocre para humanidades**. Su "Progressive Summarization" (resaltar lo ya resaltado) es uno de los métodos peor evaluados por la investigación pedagógica (Dunlosky et al., 2013).
- **Cornell Notes**: bueno para clases en vivo + texto STEM. **Insuficiente** para filosofía política densa: no captura red de conceptos ni escala a 70 autores.
- **Solo Anki**: atomiza tanto que pierdes el argumento. Es bisturí, no aspiradora.
- **Solo "tomar notas a mano en cuaderno"**: bonito pero NO compounding. A los 18 meses no encuentras lo que escribiste hace 12.

---

## :material-tools: Stack técnico recomendado (~225€ total para 28 meses)

### Lectura

| App | Para qué | Coste |
|-----|----------|-------|
| **Kindle app en iPad** | Libros comerciales en español (Akal, Alianza, FCE) | Gratis (libros aparte) |
| **PDF Expert / Apple Books** | PDFs académicos sueltos | Gratis (Apple) / ~$10 |
| **MarginNote 4** *(opcional)* | Los 8-12 libros vertebrales del curso. Outline + mindmap + flashcards. | ~$60-100 one-time |
| *Más adelante*: Boox e-ink | Descansar la vista | 400-700€ (no necesario ahora) |

### Captura automática

| App | Para qué | Coste |
|-----|----------|-------|
| **Readwise** ⭐ | Aspira automáticamente highlights de Kindle, Apple Books, Kobo, Twitter, web. **Daily Review** con spaced repetition de highlights antiguos. Plugin Obsidian nativo. | ~$8/mes · ~225€ en 28 meses |
| **Zotero** + Better BibTeX | Gestor bibliográfico académico. **Estándar real de doctorandos.** | Gratis |

### Procesado y conocimiento

| App | Para qué | Coste |
|-----|----------|-------|
| **Obsidian** ⭐ | Tu cuaderno principal. Markdown plano, archivos locales (no lock-in), enlaces bidireccionales, grafo, plugins. | Gratis |
| Plugins esenciales | Readwise Official, Obsidian-Git, Templater, Dataview, Zotero Integration | Gratis |
| **Anki** | Spaced repetition quirúrgico (15-30 tarjetas por libro vertebral, no más) | Gratis |

### Publicación

Tu sitio MkDocs en GitHub Pages ya está. **No necesitas Obsidian Publish** ni nada más.

---

## :material-cog: Workflow paso a paso (por autor)

### Antes de empezar (una vez)

1. Crear Vault Obsidian en `c:\Users\vicen\Documents\Libros Politica\` (el mismo repo).
2. Carpetas: `inbox/`, `lecturas/` (que ya tienes en docs/), `permanent/`, `mapas/`.
3. En `.gitignore` decidir si `permanent/` se publica o queda privado.
4. Configurar Readwise → conectar Kindle → instalar plugin Readwise en Obsidian.
5. Configurar Zotero con Better BibTeX.

### Por cada autor (~3 semanas para autor mayor)

#### Semana 1 — Lectura inspeccional (Adler nivel 1)

- 1-2 días: índice, prólogo, capítulos clave. Velocidad alta.
- **Salida:** una `lecturas/<autor>-<titulo>.md` vacía con:
  - Frontmatter (autor, año, fase, bloom: 0)
  - Sección "Preguntas que voy a responder" (3-5 preguntas)
  - Sección "Tesis central (mi hipótesis previa)"

#### Semana 1-2 — Lectura analítica (Adler nivel 2)

- Lees subrayando con **criterio**. Máximo ~15-25 highlights por libro denso. Si vas pasando de 50, estás subrayando, no leyendo.
- Readwise importa todos los highlights a `inbox/Readwise/<libro>.md` automáticamente.
- **Cada sesión termina con la pregunta de cierre obligatoria**: "En una frase, ¿qué he aprendido hoy que no sabía esta mañana?" (cierre Adler).

#### Semana 2 — Destilación (lo crítico)

- Abres tu literature note y los highlights de Readwise.
- Escribes la **literature note completa**: tesis del autor en 3 frases, 5 ideas clave con página, citas memorables.
- **Identifica entre 5 y 15 ideas que TE inspiran a pensar**. Cada una se vuelve una **permanent note**.

**Anatomía de una permanent note bien hecha:**

```markdown
---
fecha: 2026-05-14
fuente: lecturas/rawls-teoria-justicia.md
tags: [justicia, liberalismo, contractualismo]
bloom: 4
---

# El velo de ignorancia presupone un sujeto sin género ni raza

Rawls construye la posición original eliminando atributos
contingentes (clase, género, raza, talento). El supuesto operativo:
si quitas esos atributos, lo que queda es **el sujeto racional moral**
de base, capaz de elegir principios universales.

**Crítica feminista (Crenshaw, Mohanty):** ese "sujeto sin atributos"
no es neutralidad — es **el sujeto liberal blanco varonado**
universalizado. El velo no oculta el género; lo invisibiliza.

**Crítica decolonial (Quijano, Cusicanqui):** el sujeto contractualista
es producto histórico del 1492. No preexiste — fue producido por
la colonialidad.

**Mi posición:** la posición original NO es desencarnación —
es una desencarnación específica (la occidental moderna). Útil para
diagnósticos intra-occidentales, inválida para situaciones donde
las categorías mismas están en disputa colonial.

**Conecta con:**
- [[Crenshaw - Mapping the Margins]]
- [[Quijano - colonialidad del poder]]
- [[Sandel - critica comunitarista a Rawls]]
- [[Sujeto racional moderno como ficción]]
```

**Reglas inviolables:**

- **Una idea por nota.** Si son dos, parte.
- **Título declarativo** (afirmación completa, no "Rawls").
- **En tus palabras**, no copia.
- **Mínimo 2 enlaces** a otras notas existentes (o créalas si no existen).
- **Sin enlaces, la nota NO existe en el sistema**.

#### Semana 2-3 — Tarjetas Anki quirúrgicas

Tras destilar permanent notes, identifica **5-8 conceptos** que querrás recordar en 18 meses:

- Vocabulario técnico (qué es *phronesis*, *Aufhebung*, plusvalía, ch'ixi).
- Distinciones pareadas (libertad negativa vs positiva, ética de la convicción vs responsabilidad).
- Fechas de pivote (Schmitt → 1933, *El Capital* → 1867).

Plugin **Obsidian to Anki**: marcas conceptos con sintaxis cloze y se exportan a tu mazo de Anki.

**No más de 8 tarjetas por libro.** En 28 meses tendrás ~500 tarjetas de las que vale la pena acordarse. Mejor 500 cards que valen la pena que 3000 que ignoras.

#### Mensual — Ritual Feynman

**Una vez al mes** (último domingo): escribe un **ensayo corto** (500-800 palabras) explicando a un lector NO-filósofo el autor del mes. Lo guardas en `docs/ensayos/`.

A los 28 meses tendrás ~28 ensayos. **Eso es el borrador de un libro.**

#### Trimestral — Revisión sintópica (lectura cruzada de Adler nivel 3)

Cada 3 meses:

1. Abres el **grafo de Obsidian**. Ves dónde han crecido los clusters.
2. Identificas **nodos huérfanos** (notas sin conexiones). O las conectas o las archivas.
3. Encuentras **clusters temáticos** (ej. todo lo que has acumulado sobre "justicia distributiva" o "soberanía") y creas una **structure note** que los une.
4. **Decides el siguiente autor del plan** en función de qué preguntas tienes abiertas.

---

## :material-warning: Las trampas que matan el sistema

### 1. Collector's Fallacy

> Creer que **tener** la nota equivale a **saber**.

Capturas highlights de Kindle, los pasas a Readwise, los importas a Obsidian, te sientes productivo. **Pero no has hecho nada cognitivamente.** Las literature notes capturadas son archivo, no pensamiento. **Sin permanent notes propias, el sistema es Pinterest filosófico.**

**Test:** revisa tu Obsidian a las 4 semanas de leer un libro. Si todo lo que tienes son highlights, fallaste. Vuelve a destilar.

### 2. Sistema sin output

El sistema sirve a la escritura, no al revés. **Si en 6 meses no has producido un ensayo Feynman, el sistema está roto, no tú.**

### 3. Demasiadas tarjetas Anki

200 cards por libro no es virtud — es ruido. **5-8 cards por autor**, máximo 15 para los vertebrales. El umbral mental: *"¿voy a necesitar recordar esto en frío dentro de 18 meses?"* Si no, no es card.

### 4. Sobreoptimización del setup

Pasarse 3 semanas eligiendo el plugin perfecto antes de leer una sola página. **Empieza con setup mínimo viable y mejóralo después de leer 3 libros.**

### 5. Notas demasiado largas o demasiado cortas

- **Demasiado largas** (>500 palabras): no son ideas atómicas, son ensayos. Pártelas.
- **Demasiado cortas** (<50 palabras): no tienen suficiente argumento para enlazar. Profundízalas.

### 6. Highlighting pasivo en exceso

Si en un libro de 250 pp tienes 100 highlights, no leíste — coloreaste. **Máximo ~15-25 highlights bien elegidos por libro.**

---

## :material-format-list-checks: Higiene mensual

Última hora del último domingo del mes:

- [ ] Revisar `inbox/` — procesar todo lo pendiente o archivar.
- [ ] Cada literature note nueva debe haber generado ≥3 permanent notes. Si no, ¿qué leíste?
- [ ] Buscar nodos huérfanos en el grafo. Conectar o archivar.
- [ ] Escribir el ensayo Feynman del mes.
- [ ] Revisar Daily Review de Readwise — ¿hay highlights antiguos que ahora ves distinto? Convertir en nueva permanent note.

---

## :material-arrow-right: Integración con el resto del curso

| Elemento del curso | Cómo se integra |
|--------------------|------------------|
| **[Plantilla de lectura](../lecturas/plantilla.md)** | Es la **literature note** que abres al empezar cada autor. Ya está calibrada. |
| **[Ritual diario](ejecutar.md)** | El paso "20-30 min escribir en `lecturas/`" es la destilación de literature → permanent. |
| **[Rúbricas Bloom](bloom-rubricas.md)** | Una permanent note bien hecha está en Bloom N3-N4 (aplicar/analizar). Tu autoevaluación Bloom mide la calidad de tus notas. |
| **[Mapa de conexiones](conexiones.md)** | Las structure notes son la versión personal de este mapa. El plan te da las conexiones canónicas; tú las reconstruyes en tu vault. |
| **[Sitio MkDocs](../index.md)** | Cuando una permanent note esté madura, la mueves a `docs/conceptos/`. Se publica con el próximo push. |
| **Anki** | Plugin obsidian-to-anki sincroniza tu vault con tu mazo Anki. |

---

## :material-bookmark-multiple: Tres plantillas que necesitas

### 1. Plantilla de literature note (por libro)

Ya existe: [`docs/lecturas/plantilla.md`](../lecturas/plantilla.md). Cópiala al empezar cada libro.

### 2. Plantilla de permanent note (por idea)

```markdown
---
fecha: AAAA-MM-DD
fuente: [[lecturas/autor-titulo]]
tags: [tag1, tag2]
bloom: N
---

# [Título declarativo: una afirmación completa en una frase]

[Cuerpo: 100-300 palabras desarrollando la idea con TUS palabras]

**Crítica / objeción que detecto:** [opcional pero recomendado]

**Conecta con:**
- [[otra-nota-permanente-1]]
- [[otra-nota-permanente-2]]
- [[otra-nota-permanente-3]]
```

### 3. Plantilla de structure note (por tema)

```markdown
---
tema: [nombre del tema]
fecha-creada: AAAA-MM-DD
fecha-actualizada: AAAA-MM-DD
---

# Mapa: [tema]

## Pregunta central
[La pregunta que estructura este tema]

## Posiciones encontradas
1. **[Autor X]:** [resumen en 1 frase + enlace a permanent note]
2. **[Autor Y]:** ...
3. ...

## Lo que pienso ahora
[Tu posición provisional]

## Notas conectadas
- [[permanent-1]]
- [[permanent-2]]
- ...

## Lecturas pendientes para profundizar
- ...
```

---

## :material-clock-fast: Tiempos realistas

- **Setup técnico inicial** (Obsidian + Zotero + Readwise + plantillas + primer autor): **2-3 semanas**.
- **Fluidez** (ya no piensas en el sistema, solo lees y escribes): **3-4 meses**.
- **Primer retorno no obvio** (conexión que descubres entre dos autores que no buscabas): **mes 6-8**.
- **Compounding real** (el grafo te enseña cosas): **mes 12+**.
- **A 28 meses**: ~700-1.500 permanent notes, ~400-600 cards de Anki, ~25 ensayos Feynman, dominio operativo comparable al final de un máster bien hecho.

---

## :material-link-variant: Recursos verificados

### Documentación canónica

- **Sönke Ahrens — *How to Take Smart Notes* (2017):** [soenkeahrens.de/en/takesmartnotes](https://www.soenkeahrens.de/en/takesmartnotes). El libro que sistematizó el Zettelkasten digital. Léelo entero (180 pp).
- **Mortimer Adler — *Cómo leer un libro* (1940/1972):** ya en tu plan (Fase 0). Define lectura inspeccional, analítica, sintópica.
- **Andy Matuschak — Evergreen notes:** [notes.andymatuschak.org/Evergreen_notes](https://notes.andymatuschak.org/Evergreen_notes). El análisis más serio de notas conceptuales.
- **Zettelkasten.de — Introduction:** [zettelkasten.de/introduction](https://zettelkasten.de/introduction/). Comunidad activa, debates serios.
- **Critique al hype:** [Zettelkasten as a coping mechanism](https://forum.zettelkasten.de/discussion/1069/zettelkasten-as-a-coping-mechanism-or-why-i-abdicate-the-zettelkasten-method). Léelo para no caer en la trampa de productividad.

### Apps y herramientas

- **Obsidian:** [obsidian.md](https://obsidian.md/)
- **Readwise:** [readwise.io](https://readwise.io/) (~$8/mes, vale para tu volumen)
- **Zotero:** [zotero.org](https://zotero.org/) (gratis)
- **Anki:** [apps.ankiweb.net](https://apps.ankiweb.net/) (gratis)
- **Plugin Readwise-Obsidian:** [github.com/readwiseio/obsidian-readwise](https://github.com/readwiseio/obsidian-readwise)
- **Plugin Obsidian-Git:** [github.com/Vinzent03/obsidian-git](https://github.com/Vinzent03/obsidian-git)
- **Plugin Obsidian-to-Anki:** [github.com/Pseudonium/Obsidian_to_Anki](https://github.com/Pseudonium/Obsidian_to_Anki)
- **Calibre:** [calibre-ebook.com](https://calibre-ebook.com/) (gestor de biblioteca, gratis)
- **MarginNote 4** *(opcional, $60-100):* [marginnote.com](https://marginnote.com/) — solo si vas a tratar 8-12 PDFs vertebrales con outline + mindmap.

### Humanidades digitales

- **Regina Martínez Ponciano — Research methods for a Humanities PhD:** [martinezponciano.es/2021/04/05/research-methods-and-tools-for-a-humanities-phd-zettelkasten-obsidian-zotero-and-pandoc](https://martinezponciano.es/2021/04/05/research-methods-and-tools-for-a-humanities-phd-zettelkasten-obsidian-zotero-and-pandoc/). El workflow real de doctorandos en humanidades.

---

[:material-arrow-left: Volver al Plan](index.md){ .md-button }
[:material-notebook-edit: Plantilla literature note](../lecturas/plantilla.md){ .md-button }
[:material-download: Plantillas descargables](../plantillas/index.md){ .md-button .md-button--primary }
