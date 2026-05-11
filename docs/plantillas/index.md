---
title: Plantillas
---

# Plantillas

Cada plantilla es un archivo `.md`. Tres formas de usarla:

- **Descargar** — baja el archivo a tu portátil. Lo abres en Antigravity / cualquier editor.
- **Copiar** — copia el contenido al portapapeles. Pegas donde quieras.
- **Crear en GitHub** — abre el editor de GitHub para tu repo con la plantilla ya pegada. Solo escribes lo tuyo y "commit".

!!! info "¿Por qué `.md` y no `.docx`?"
    Todo el sistema funciona sobre **markdown**. Es lo que renderiza tu sitio, lo que entiende GitHub, lo que indexa la búsqueda. Word `.docx` es un formato binario que rompería el pipeline.

    **Si necesitas Word de verdad** (para imprimir, compartir con alguien que no usa Markdown): descarga el `.md`, ábrelo en [Pandoc](https://pandoc.org/) o pega el contenido en [dillinger.io](https://dillinger.io) y exporta a `.docx` desde ahí.

    En el día a día, no lo vas a necesitar.

---

## Nota de lectura

Una por libro completado. La guardas en `docs/lecturas/[apellido-titulo].md`.

<div class="template-card" data-template="lectura" data-filename="mi-libro.md" data-path="docs/lecturas">
  <div class="g-actions template-actions">
    <button class="g-btn g-btn-primary" data-action="download">Descargar .md</button>
    <button class="g-btn" data-action="copy">Copiar al portapapeles</button>
    <a class="g-btn" data-action="github" target="_blank" rel="noopener">Crear en GitHub →</a>
  </div>
  <details class="template-content">
    <summary>Ver contenido de la plantilla</summary>

````markdown
---
title: "[Título del libro] — [Autor]"
fase: [0-5]
fechas: AAAA-MM-DD → AAAA-MM-DD
edicion: "[editorial, año, traductor]"
bloom: [1-6]
---

# [Título del libro] — [Autor]

## 1. Tesis central (3 frases)

> Si no puedes en 3 frases, no lo entendiste todavía.

…

## 2. Cinco ideas que me marcaron

1. **[Idea]** — p. XX. *Por qué me marca:* …
2. **[Idea]** — p. XX.
3. **[Idea]** — p. XX.
4. **[Idea]** — p. XX.
5. **[Idea]** — p. XX.

## 3. Mi crítica / objeción

¿Qué no me convenció? ¿Dónde podría estar haciendo trampa el autor?

…

## 4. Diálogo con otros autores del plan

- **Coincide con / desarrolla:** [autor + en qué]
- **Contradice / refuta:** [autor + en qué]

## 5. Citas para releer

> "…" — p. XX

## 6. Notas de práctica

- Se lo expliqué a: [persona / fecha]
- Lo grabé argumentando: [archivo en `../oratoria/`]
- Aparece en ensayo: [archivo en `../ensayos/`]
````

  </details>
</div>

---

## Ensayo propio

Tus textos en `docs/ensayos/`. Convención de nombre: `AAAA-MM-DD_titulo-corto.md`.

<div class="template-card" data-template="ensayo" data-filename="$DATE_titulo-corto.md" data-path="docs/ensayos">
  <div class="g-actions template-actions">
    <button class="g-btn g-btn-primary" data-action="download">Descargar .md</button>
    <button class="g-btn" data-action="copy">Copiar al portapapeles</button>
    <a class="g-btn" data-action="github" target="_blank" rel="noopener">Crear en GitHub →</a>
  </div>
  <details class="template-content">
    <summary>Ver contenido de la plantilla</summary>

````markdown
---
title: "[Tu título]"
date: AAAA-MM-DD
tags: [fase, tema]
---

# [Tu título]

## Tesis

Una frase clara de lo que defiendes.

## Argumento

[3-5 párrafos. Razones, ejemplos, citas con número de página.]

## La mejor objeción posible

[El contraargumento más fuerte que se te ocurra, sin caricatura. Esto separa un ensayo de un alegato.]

## Mi respuesta a esa objeción

[1-2 párrafos.]

## Conclusión

¿Qué cambia tu tesis para quien la acepta?

## Bibliografía

- Autor, *Título*, editorial, año.
````

  </details>
</div>

---

## Log de falacias

Para captura semanal/diaria. O usa el [**formulario web**](plantilla-falacia.md) que guarda en navegador y exporta a `.md`.

<div class="template-card" data-template="falacia" data-filename="falacias-log.md" data-path="docs">
  <div class="g-actions template-actions">
    <button class="g-btn g-btn-primary" data-action="download">Descargar .md</button>
    <button class="g-btn" data-action="copy">Copiar al portapapeles</button>
    <a class="g-btn" data-action="github" target="_blank" rel="noopener">Crear en GitHub →</a>
  </div>
  <details class="template-content">
    <summary>Ver contenido de la plantilla</summary>

````markdown
# Mi log de falacias

Una fila por captura. Familia: Lenguaje / Emoción / Distracción / Inducción defectuosa.

| Fecha | Medio / autor | Cita corta | Familia | Falacia | Mi respuesta en una frase |
|---|---|---|---|---|---|
| AAAA-MM-DD | (medio o autor) | "..." | (familia) | (ejemplo: falsa dicotomía) | (cómo responderías) |
````

  </details>
</div>

---

## Log de oratoria

Para registrar grabaciones semanales y debates mensuales. Ya tienes uno en [`oratoria/log.md`](../oratoria/log.md).

<div class="template-card" data-template="oratoria" data-filename="oratoria-log.md" data-path="docs/oratoria">
  <div class="g-actions template-actions">
    <button class="g-btn g-btn-primary" data-action="download">Descargar .md</button>
    <button class="g-btn" data-action="copy">Copiar al portapapeles</button>
    <a class="g-btn" data-action="github" target="_blank" rel="noopener">Crear en GitHub →</a>
  </div>
  <details class="template-content">
    <summary>Ver contenido de la plantilla</summary>

````markdown
# Log de oratoria

## Práctica semanal: grabaciones de 3-5 min

| Fecha | Tema / libro | Duración | Muletillas detectadas | Qué mejorar |
|---|---|---|---|---|
|  |  |  |  |  |

## Debates reales (mensual)

| Fecha | Con quién | Tema | Cómo fue | Qué aprendí |
|---|---|---|---|---|
|  |  |  |  |  |
````

  </details>
</div>
