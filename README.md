# Libros Política — Mi plan personal de estudio

Sitio web personal con mi plan de estudio de pensamiento crítico, filosofía política, sociología y economía, generado con [MkDocs](https://www.mkdocs.org/) + [Material](https://squidfunk.github.io/mkdocs-material/).

## Trabajo diario (sin terminal)

1. **Editar notas:** abrir Obsidian → abrir la carpeta `Libros Politica` como Vault → editar cualquier `.md` dentro de `docs/`.
2. **Publicar cambios:** abrir GitHub Desktop → ver los cambios → poner mensaje de commit → "Commit to main" → "Push origin".
3. En ~1 minuto los cambios se ven en la web.

## Comandos (solo si necesitas)

Levantar el sitio en local (preview en `http://127.0.0.1:8000`):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve
```

Build estático (no necesario — lo hace GitHub Actions automáticamente):

```powershell
mkdocs build
```

## Estructura del repo

```
docs/
  index.md           ← landing
  plan/              ← plan maestro, cómo ejecutar, falacias
  lecturas/          ← una nota por libro leído
  ensayos/           ← textos propios
  oratoria/          ← log de grabaciones
  plantillas/        ← descargas
  seguimiento.md     ← checklist + Bloom
  assets/            ← CSS y JS custom
mkdocs.yml           ← config del sitio
requirements.txt     ← dependencias Python
.github/workflows/
  deploy.yml         ← CI auto-deploy a GitHub Pages
```
