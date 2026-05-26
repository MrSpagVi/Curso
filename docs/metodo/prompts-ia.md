---
title: Prompts para usar con IA
---

# Prompts para usar con IA (con guardrails)

!!! warning "Regla anti-Dunning-Kruger"
    La IA aparece **solo después** de que ya leíste, escribiste literatura notes y produjiste una nota permanente. **Nunca antes ni en lugar de.** Hay evidencia 2025 de que usar IA antes acelera la falsa sensación de comprensión ("reverse Dunning-Kruger").

---

## Los 5 prompts canónicos

Probados con Claude y ChatGPT. Copiá-pegá adaptando los corchetes al contexto.

### 1. Devil's advocate (después de leer)

```
Soy lector de izquierda no dogmática. Acabo de leer [X].
Hacé el caso más fuerte EN CONTRA de la tesis principal,
citando autores que la refutaron. No me halagues, no concedas,
no digas "buena pregunta".
```

**Cuándo usarlo:** después de terminar un libro o capítulo importante, antes de escribir tu nota permanente. Te obliga a articular la objeción seria.

### 2. Examen socrático (post lectura)

```
Voy a explicarte con mis palabras [concepto X].
Después hacéme 5 preguntas que un examinador hostil de
doctorado me haría para detectar si entendí o estoy chamuyando.
No me corrijas hasta que responda.
```

**Cuándo usarlo:** al terminar una fase o capítulo. Es Feynman technique con IA como sparring. Si fallás 3 de 5 preguntas, no entendiste.

### 3. Caza-falacia (en captura diaria)

```
Pegá este pasaje. Identificá: (a) la tesis, (b) los supuestos
no enunciados, (c) las falacias o saltos lógicos si las hay,
(d) qué evidencia haría falta para refutarla.
```

**Cuándo usarlo:** sobre un fragmento de prensa, columna o tweet. Te ayuda a calibrar tu propia identificación. **No reemplaza tu captura** — primero capturás vos, después comparás con la IA.

### 4. Steelman comparado (autores opuestos)

```
Construí el steelman de Marx sobre [X] y el steelman de Hayek
sobre [X] en paralelo. Sin ganador. Sin matices conciliadores
tipo "ambos tienen razón".
```

**Cuándo usarlo:** antes de un ensayo donde vas a discutir 2 posiciones rivales. La IA te ayuda a no caricaturizar a ninguno de los dos.

### 5. Detector de sesgo propio (sobre tus notas)

```
Te paso mi nota sobre [X]. ¿Qué autores/argumentos importantes
estoy ignorando porque chocan con mi posición previa?
```

**Cuándo usarlo:** al cerrar una nota permanente o ensayo. Es el más incómodo y el más valioso.

---

## Riesgos de la IA que tenés que conocer

1. **Sicofancia.** Los modelos grandes coinciden con la opinión del usuario >90% en filosofía/política (estudio Anthropic 2023). **Pedile explícitamente que disienta.** "No me halagues, no concedas" debería ser regla por defecto en cada prompt.

2. **Alucinación de citas.** NUNCA citar en un ensayo una referencia que diste por IA sin verificarla en biblioteca, Google Scholar, JSTOR o el texto original. La IA inventa autores, fechas y obras con confianza absoluta.

3. **Falsa comprensión.** La IA-explicación se siente como aprendizaje y no lo es. Por eso la regla: **nunca pedir explicación de un texto que no leíste primero**. Cuando leés primero y después usás IA para discutir, la IA te ayuda. Cuando reemplazás la lectura con IA, te perdés la transformación.

4. **Reverse Dunning-Kruger** (estudio 2025). Mientras más usás IA, más sobreestimás tu competencia. Test rápido: ¿podés explicar esto a un colega sin abrir Claude/ChatGPT? Si no, no lo sabés. **No importa cuántas conversaciones con IA tuviste.**

---

## Modelo recomendado y costo

| Tarea | Modelo | Costo |
|---|---|---|
| Devil's advocate, steelman, examen socrático | Claude Sonnet (4.x) o Opus | Free tier alcanza si lo usás 1 sesión por semana · Pro 20 USD/mes para uso intensivo |
| Caza-falacia rápida | Cualquier LLM grande | Free tier |
| Detector de sesgo | Claude (suele dar mejor disenso que GPT) | Free tier |

**No uses LLM locales chicos** (Llama 3 7B o similares) para humanidades. Saben menos que vos en el momento que arranques Fase 2 — te van a dar respuestas equivocadas con confianza.

---

## Si la IA te falla

Síntomas frecuentes y qué hacer:

- **"Excelente pregunta, X tiene razón en muchos puntos…"** → Sicofancia. Repreguntá: "no me halagues, hacé el contraargumento más duro posible".
- **Cita un libro que no encontrás en biblioteca** → Alucinación. Pedí "verificá esta cita: autor + libro + año + editorial. Si no podés verificar, decímelo".
- **Responde lo que ya sabés sin agregar nada** → mala prompting. Pediles algo específico: "qué objeción haría un kantiano a esta tesis utilitarista" en vez de "qué pensás de esto".
- **Te da listas largas sin profundidad** → pedile 1 idea desarrollada en 3 párrafos en vez de 10 viñetas.

[:material-arrow-left: Volver a Método](../metodo.md){ .md-button }
