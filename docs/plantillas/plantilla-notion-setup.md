---
title: Plantilla — Setup Notion (gratis)
---

# Plantilla — Setup Notion (gratis)

> **Notion plan personal es gratis para siempre** (mientras seas un solo usuario). Bloques ilimitados. Acceso desde web, móvil, escritorio. Sin pagar nada.

Esta plantilla te lleva paso a paso a montar tu sistema de notas en Notion en ~2-3 horas. Después, abrir una nueva entrada es 1 clic.

---

## :material-account-plus: Paso 1 — Crear cuenta (5 min)

1. Ve a [notion.so](https://www.notion.so/).
2. Crea cuenta con tu email (gratis, sin tarjeta).
3. Elige "Personal Plan" (gratis).
4. Skip todos los tours guiados.

**No necesitas Notion AI ni planes pagos para nada de esto.**

---

## :material-home-plus: Paso 2 — Crear la página principal (10 min)

1. En el sidebar izquierdo, click "+ Add a page".
2. Título: **"Curso de Ciencia Política"**.
3. Estructura de la página:

```
📚 Curso de Ciencia Política
├── 🏠 Dashboard (página principal)
├── 📖 Lecturas (database)
├── 💡 Permanent notes (database)
├── ✍️ Autores (database)
├── 📝 Ensayos Feynman (database)
└── 🗂️ Inbox (página simple para capturas al vuelo)
```

En el Dashboard pon una breve descripción, las fechas del plan, y links a las 4 databases.

---

## :material-database: Paso 3 — Database 1: Lecturas (literature notes)

Esta es donde tomas notas SOBRE los libros (lo que dice el autor).

### Crear la database

1. Dentro de "Curso de Ciencia Política", click "+ Add new" → **Database — Full page** → da el nombre **"Lecturas"**.

### Configurar las propiedades (columnas)

Click en "+ Add a property" para cada una:

| Nombre propiedad | Tipo | Valores / configuración |
|------------------|------|--------------------------|
| **Título** | Title | (viene por defecto) — formato: "Apellido — *Título corto*" |
| **Autor** | Text | — |
| **Año** | Number | — |
| **Fase** | Select | Crear opciones: 0, 1, 2, 3, 4, 5, M3, M4 |
| **Estado** | Select | Por leer · En curso · Terminado |
| **Bloom nivel** | Number | 0-6 (autoevaluación al cerrar) |
| **Tags temáticos** | Multi-select | justicia · liberalismo · contractualismo · marxismo · decolonialidad · feminismo · geopolítica · etc. |
| **Fecha empezado** | Date | — |
| **Fecha terminado** | Date | — |
| **Permanent notes** | Relation → Permanent notes | (configurarás esta relation después de crear database 2) |

### Crear el template de página de cada lectura

1. Hover sobre el botón "**New**" arriba a la derecha → flecha desplegable → "**+ New template**".
2. Llama al template **"Plantilla lectura"**.
3. Dentro del template, escribe la estructura siguiente como contenido por defecto:

```
## Tesis central (3 frases)
Resume el argumento principal en 3 frases. Si no puedes, no lo entendiste.

## Capítulos leídos
- [ ] Cap. 1: …
- [ ] Cap. 2: …

## 5 ideas que me marcaron
1. **Idea breve** — p. XX. Por qué me marca: ...
2. ...

## Mi crítica / objeción
¿Qué no me convenció? ¿Dónde falla?

## Diálogo con otros autores del plan
- Coincide con: [@autor X] en...
- Contradice a: [@autor Y] en...

## Citas memorables
> "Cita textual" — p. XX

## Permanent notes generadas
- (links a database 2 cuando las crees)

## Bloom autoevaluado: ___
```

Ahora cada vez que añadas un nuevo libro, click "New" y selecciona "Plantilla lectura" — aparece toda la estructura pre-llenada.

---

## :material-lightbulb-on: Paso 4 — Database 2: Permanent notes (LA CRÍTICA)

Esta es la pieza central. Donde **archivas tus ideas, no las del autor**.

### Crear la database

1. En la página principal, click "+ Add new" → **Database — Full page** → "**Permanent notes**".

### Propiedades

| Nombre propiedad | Tipo | Configuración |
|------------------|------|---------------|
| **Título** | Title | **Declarativo en una frase** — afirmación completa |
| **Fecha creada** | Created time | (automático) |
| **Fecha modificada** | Last edited time | (automático) |
| **Tags** | Multi-select | Comparte tags con database 1 |
| **Bloom nivel** | Number | 2-6 (qué nivel te parece) |
| **Fuente** | Relation → Lecturas | El libro que la disparó |
| **Conexiones** | Relation → Permanent notes (a sí misma) | Las otras permanent notes con las que dialoga |
| **Estado** | Select | Borrador · Madura · Publicable (para enviar al sitio) |

### Template

```
[Aquí desarrollas la idea en 100-300 palabras EN TUS PALABRAS — no la voz del autor]

## Crítica / objeción que detecto
[Opcional pero recomendado: el contraargumento más fuerte contra TU idea]

## Origen
Esta idea nació leyendo [@Lectura]. Cita textual que la disparó:
> "..." — Autor, *Libro*, p. XX

## Conecta con
- [@Permanent note relacionada 1]
- [@Permanent note relacionada 2]
- [@Permanent note relacionada 3]
```

### Conectar las dos databases

Ahora ve a la database **Lecturas** y configura la propiedad "Permanent notes" como **Relation → Permanent notes**. Marca "Show on Permanent notes" para que el enlace funcione en ambas direcciones (similar a enlace bidireccional).

---

## :material-account: Paso 5 — Database 3: Autores

Para tener una vista por pensador, no por libro.

### Propiedades

| Propiedad | Tipo |
|-----------|------|
| **Nombre** | Title (Apellido, Nombre) |
| **Años** | Text (ej. "1921-2002") |
| **Nacionalidad** | Text |
| **Fase principal** | Select |
| **Tesis central** | Text (largo) |
| **Conceptos clave** | Multi-select |
| **Libros leídos** | Relation → Lecturas |
| **Permanent notes** | Relation → Permanent notes |
| **Dialoga con** | Relation → Autores (a sí misma) |

### Template

```
## Tesis central
[1-2 frases que resumen su posición]

## Contexto humano
[Anécdota o contexto biográfico relevante]

## Conceptos clave
- Concepto 1: definición operativa
- Concepto 2: ...

## Libros leídos del autor
[@Lectura 1]
[@Lectura 2]

## Permanent notes sobre este autor
[@PN 1]
[@PN 2]

## Dialoga con
[@Autor X]: en qué coincide / discrepa
```

---

## :material-feather: Paso 6 — Database 4: Ensayos Feynman

Mensual: un ensayo de 500-800 palabras explicando a no-filósofo el autor del mes.

### Propiedades

| Propiedad | Tipo |
|-----------|------|
| **Título** | Title |
| **Fecha** | Date |
| **Autor sobre el que escribes** | Relation → Autores |
| **Mes del plan** | Number |
| **Palabras** | Number |
| **Estado** | Select (Borrador · Revisado · Publicado en sitio) |

### Template

```
## Tesis
[Lo que defiendes en una frase]

## Argumento
[3-5 párrafos. Citas con número de página de [@Lectura]]

## La mejor objeción posible
[El contraargumento más fuerte, sin caricatura]

## Mi respuesta a esa objeción
[1-2 párrafos]

## Conclusión
[¿Qué cambia tu tesis para quien la acepta?]

## Bibliografía citada
- [@Lectura 1]
- [@Lectura 2]
```

---

## :material-eye: Paso 7 — Vistas útiles

Para cada database, puedes crear múltiples vistas filtradas. Las más útiles:

### En Lecturas

- **"En curso ahora"** — filtra Estado = En curso. Ordenado por Fecha empezado.
- **"Por fase"** — agrupa por Fase. Ves qué te queda en cada una.
- **"Por terminar"** — filtra Estado = Por leer. Ordenado por Fase.

### En Permanent notes

- **"Recientes"** — última semana, ordenado por Fecha creada.
- **"Daily Review · hace 90 días"** — filtra Fecha creada hace ~90 días. **Esto es tu sustituto GRATIS de Readwise Daily Review.**
- **"Borradores"** — Estado = Borrador. Para refinar.
- **"Publicables al sitio"** — Estado = Publicable. Para mover a MkDocs cuando estés listo.
- **"Por tag"** — agrupa por Tags. Ves clusters temáticos automáticos.

### En Autores

- **"Por fase"** — agrupa por Fase principal.

---

## :material-import: Paso 8 — Importar highlights de Kindle (gratis)

1. Termina un libro en Kindle.
2. Ve a [read.amazon.com/notebook](https://read.amazon.com/notebook) (web del Kindle Notebook).
3. Selecciona el libro.
4. Instala el bookmarklet **Bookcision** (gratis): https://readwise.io/bookcision
5. Click en el bookmarklet → descarga TXT con todos tus highlights.
6. En Notion, abre la entrada del libro → pega el TXT en una sección "Highlights brutos".
7. Destila los highlights → mueve los importantes a "5 ideas que me marcaron" y a Permanent notes.

**No requiere pagar Readwise.** Bookcision es de Readwise pero gratis y standalone.

---

## :material-shield-lock: Paso 9 — Backup (gratis)

Notion vive en cloud. Si se cae o cambian precios, debes poder rescatar tus notas.

**Backup mensual gratis:**

1. En cada database, click "**...**" → **Export**.
2. Formato: **Markdown & CSV**.
3. Descarga el ZIP.
4. Guarda el ZIP en tu repo GitHub (carpeta `notas-privadas/backup-AAAA-MM/`) o en Google Drive.

**Tiempo: 5 min/mes.** Tu trabajo no depende de Notion sobreviviendo.

---

## :material-publish: Paso 10 — Publicar al sitio MkDocs

Cuando una permanent note esté **madura** (Estado = Publicable):

1. En Notion, click "**...**" en la nota → **Export → Markdown**.
2. Descarga el archivo `.md`.
3. Cópialo a tu repo en `docs/conceptos/<titulo-corto>.md`.
4. Edita los enlaces si es necesario (los `[@Lectura X]` de Notion se traducen a `[texto](enlace)`).
5. Commit + push.
6. En 1-2 min aparece en tu sitio público.

**No necesitas Obsidian para esto.** Notion → markdown → MkDocs funciona limpio.

---

## :material-clock-fast: Tiempos realistas

- **Setup inicial siguiendo esta plantilla:** 2-3 horas.
- **Cada libro nuevo:** abrir entrada con template (1 clic), ir rellenando.
- **Destilación semanal:** 60-90 min para crear 3-7 permanent notes.
- **Backup mensual:** 5 min.

---

## :material-help-circle: FAQ

??? question "¿Notion en móvil sirve?"
    Sí — la app móvil de Notion es buena. Puedes capturar fleeting notes en móvil mientras lees en Kindle. Después en escritorio las refinas.

??? question "¿Y si quiero pasar de Notion a Obsidian más adelante?"
    El export de Notion a Markdown funciona razonablemente. Las relations entre databases se traducen a wikilinks. Esperar perder ~10% en estructura, pero el contenido se preserva.

??? question "¿Hay límites en el plan gratis?"
    Notion Free Personal: bloques **ilimitados**, miembros ilimitados (si es solo para ti — 1 persona). Limita: subidas grandes (5 MB por archivo en free, suficiente para markdown), Notion AI (incluido en Plus). **Para tu caso, NO te chocas con ningún límite.**

??? question "¿Y mi privacidad?"
    Notion ve todo lo que escribes (son servidores cloud). Si te preocupa: usa Obsidian (archivos locales tuyos) en su lugar. La plantilla nota permanente en markdown sirve para Obsidian.

??? question "¿Puedo usar Notion + papel a la vez?"
    Sí. Es el **workflow C híbrido** del [Sistema de notas](../plan/notas.md). Notion = backup digital + búsqueda; papel = donde piensas.

---

## :material-link-variant: Enlaces

- [Notion personal plan (gratis)](https://www.notion.so/pricing)
- [Bookcision (Kindle highlights gratis)](https://readwise.io/bookcision)
- [Notion templates oficiales](https://www.notion.so/templates)
- [Sistema completo de notas en el curso](../plan/notas.md)
- [Plantilla cuaderno papel (alternativa)](plantilla-cuaderno-papel.md)
- [Plantilla fichas Zettelkasten papel](plantilla-zettelkasten-papel.md)

---

[:material-arrow-left: Volver a Plantillas](index.md){ .md-button }
[:material-school: Sistema completo de notas](../plan/notas.md){ .md-button .md-button--primary }
