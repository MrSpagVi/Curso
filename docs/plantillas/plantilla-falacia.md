---
title: Plantilla — log de falacias
---

# Log de falacias — plantilla

> Crea un archivo `docs/falacias-log.md` y pega esta tabla. Añade una fila por captura.

```markdown
# Mi log de falacias

| Fecha       | Medio / autor             | Cita corta                                  | Familia     | Falacia              | Mi respuesta en una frase                    |
|-------------|---------------------------|---------------------------------------------|-------------|----------------------|----------------------------------------------|
| AAAA-MM-DD  | (medio o autor)           | "..."                                       | Lenguaje    | (ejemplo: equivocación) | (cómo responderías en directo)            |
```

## Recordatorio de las 4 familias

| Familia | Qué hace |
|---------|---------|
| **Lenguaje** | Trampa lingüística (ambigüedad, redefinición). |
| **Emoción** | Sustituye razón por sentimiento (miedo, pena, indignación). |
| **Distracción** | Desvía la conversación a otro tema. |
| **Inducción defectuosa** | Generaliza mal, confunde correlación y causa. |

Lista completa con ejemplos políticos: [manual de falacias](../plan/falacias.md).

## Captura rápida desde el navegador

<div class="falacia-form">
  <label>Fecha
    <input type="date" id="fal-date">
  </label>
  <label>Medio / autor
    <input type="text" id="fal-source" placeholder="Ej: El País — columna XX">
  </label>
  <label>Cita corta
    <textarea id="fal-quote" rows="2" placeholder='"..."'></textarea>
  </label>
  <label>Familia
    <select id="fal-family">
      <option value="">—</option>
      <option>Lenguaje</option>
      <option>Emoción</option>
      <option>Distracción</option>
      <option>Inducción defectuosa</option>
    </select>
  </label>
  <label>Falacia concreta
    <input type="text" id="fal-name" placeholder="Ej: Falsa dicotomía">
  </label>
  <label>Mi respuesta en una frase
    <textarea id="fal-reply" rows="2"></textarea>
  </label>
  <button id="fal-save" class="md-button md-button--primary">Guardar captura</button>
  <button id="fal-export" class="md-button">Exportar a markdown</button>
  <p id="fal-status" class="status-msg"></p>
</div>

<div id="fal-list" class="falacia-list"></div>
