/* ============================================================
   Libros Política — Glance-style interactive widgets
   Pure vanilla JS, localStorage-backed
   ============================================================ */

(function () {
  'use strict';

  // ---------- Storage keys ----------
  const STORAGE = {
    startDate: 'lp.startDate',
    dailyMinutes: 'lp.dailyMinutes',
    falacias: 'lp.falacias',
    bestStreak: 'lp.bestStreak',
  };

  // ---------- Helpers ----------

  function todayISO(d) {
    const date = d || new Date();
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${day}`;
  }

  function daysSince(startISO) {
    if (!startISO) return null;
    const start = new Date(startISO + 'T00:00:00');
    const now = new Date();
    now.setHours(0, 0, 0, 0);
    start.setHours(0, 0, 0, 0);
    return Math.floor((now - start) / 86400000);
  }

  function phaseFor(day) {
    if (day == null) return ['—', '—'];
    if (day < 0) return ['No empezado', '—'];
    const month = Math.floor(day / 30) + 1;
    if (month <= 2) return ['0 · Cimientos', month];
    if (month <= 8) return ['1 · Filosofía clásica', month];
    if (month <= 12) return ['2 · Economía política', month];
    if (month <= 17) return ['3 · Sociopolítica s. XX', month];
    if (month <= 22) return ['4 · Iberoamericana', month];
    if (month <= 28) return ['5 · Síntesis', month];
    return ['Plan completado', month];
  }

  function isoWeek(d) {
    const dt = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    const dayNum = dt.getUTCDay() || 7;
    dt.setUTCDate(dt.getUTCDate() + 4 - dayNum);
    const yearStart = new Date(Date.UTC(dt.getUTCFullYear(), 0, 1));
    const weekNo = Math.ceil(((dt - yearStart) / 86400000 + 1) / 7);
    return `${dt.getUTCFullYear()}-W${String(weekNo).padStart(2, '0')}`;
  }

  function fmtDateES(iso) {
    const d = new Date(iso + 'T00:00:00');
    return d.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' });
  }

  function saveJSON(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) {}
  }

  function loadJSON(key, fallback) {
    try {
      const raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }

  // ---------- Clock (live, updates each second) ----------

  let clockTimer = null;

  function updateClock() {
    const dateEl = document.getElementById('g-date');
    const timeEl = document.getElementById('g-time');
    if (!dateEl || !timeEl) return;
    const now = new Date();
    const day = String(now.getDate());
    const month = now.toLocaleDateString('es-ES', { month: 'short' }).replace('.', '');
    const year = now.getFullYear();
    dateEl.textContent = `${day} ${month} ${year}`;
    timeEl.textContent = now.toTimeString().slice(0, 8);
  }

  function startClock() {
    updateClock();
    if (clockTimer) clearInterval(clockTimer);
    clockTimer = setInterval(updateClock, 1000);
  }

  // ---------- Hero dashboard render ----------

  function renderDashboard() {
    const dayEl = document.getElementById('g-day');
    const phaseEl = document.getElementById('g-phase');
    const monthEl = document.getElementById('g-month');
    const weekglobalEl = document.getElementById('g-weekglobal');
    const progressBar = document.getElementById('g-progress-bar');
    const hoursTodayEl = document.getElementById('g-hours-today');
    const hoursWeekEl = document.getElementById('g-hours-week');
    const hoursTotalEl = document.getElementById('g-hours-total');
    const streakNumEl = document.getElementById('g-streak-num');
    const streakBestEl = document.getElementById('g-streak-best');

    if (!dayEl) return; // not on landing

    const startDate = localStorage.getItem(STORAGE.startDate);
    const day = daysSince(startDate);

    if (day != null && day >= 0) {
      dayEl.textContent = `Día ${day + 1} del plan`;
      const [phaseLabel, monthNum] = phaseFor(day);
      phaseEl.textContent = phaseLabel;
      monthEl.textContent = `${monthNum} / 28`;
      const week = Math.floor(day / 7) + 1;
      weekglobalEl.textContent = `${week} / 120`;
      const pct = Math.min(100, ((day + 1) / (28 * 30)) * 100);
      progressBar.style.width = pct.toFixed(1) + '%';
    } else {
      dayEl.textContent = 'Configura tu inicio ↓';
      phaseEl.textContent = '—';
      monthEl.textContent = '—';
      weekglobalEl.textContent = '—';
      progressBar.style.width = '0%';
    }

    // Hours
    const daily = loadJSON(STORAGE.dailyMinutes, {});
    const now = new Date();
    const todayStr = todayISO(now);
    const todayMin = daily[todayStr] || 0;
    hoursTodayEl.textContent = (todayMin / 60).toFixed(1) + ' h';

    // Week sum
    const currentWeek = isoWeek(now);
    let weekMin = 0;
    Object.keys(daily).forEach((d) => {
      if (isoWeek(new Date(d + 'T00:00:00')) === currentWeek) weekMin += daily[d];
    });
    hoursWeekEl.textContent = (weekMin / 60).toFixed(1) + ' h';

    // Total
    let totalMin = 0;
    Object.values(daily).forEach((m) => (totalMin += m));
    hoursTotalEl.textContent = (totalMin / 60).toFixed(1) + ' h';

    // Streak
    const streak = computeStreak(daily);
    streakNumEl.textContent = streak;
    const best = loadJSON(STORAGE.bestStreak, 0);
    if (streak > best) {
      saveJSON(STORAGE.bestStreak, streak);
      streakBestEl.textContent = `Récord ${streak}`;
    } else {
      streakBestEl.textContent = `Récord ${best}`;
    }
  }

  function computeStreak(daily) {
    // Walk backwards from today; count consecutive days with > 0 minutes
    let count = 0;
    const cur = new Date();
    cur.setHours(0, 0, 0, 0);
    while (true) {
      const iso = todayISO(cur);
      if ((daily[iso] || 0) > 0) {
        count += 1;
        cur.setDate(cur.getDate() - 1);
      } else {
        // Allow skipping today if today has 0 (so streak doesn't reset before night)
        if (count === 0 && iso === todayISO()) {
          cur.setDate(cur.getDate() - 1);
          continue;
        }
        break;
      }
    }
    return count;
  }

  // ---------- Start date setup ----------

  function setupStartDate() {
    const input = document.getElementById('start-date-input');
    const button = document.getElementById('start-date-save');
    const status = document.getElementById('start-date-status');
    if (!input || !button) return;

    const stored = localStorage.getItem(STORAGE.startDate);
    if (stored) {
      input.value = stored;
      status.textContent = `Guardado: ${fmtDateES(stored)}`;
      status.classList.add('success');
    }

    button.addEventListener('click', () => {
      const value = input.value;
      if (!value) {
        status.textContent = 'Elige una fecha';
        status.classList.remove('success');
        return;
      }
      localStorage.setItem(STORAGE.startDate, value);
      status.textContent = `Guardado: ${fmtDateES(value)}`;
      status.classList.add('success');
      renderDashboard();
      renderThisWeek();
    });
  }

  // ---------- Time tracker buttons ----------

  function setupTimeButtons() {
    const buttons = document.querySelectorAll('.g-actions .g-btn[data-add]');
    if (buttons.length === 0) return;
    buttons.forEach((b) => {
      b.addEventListener('click', () => {
        const add = parseInt(b.dataset.add, 10);
        const daily = loadJSON(STORAGE.dailyMinutes, {});
        const today = todayISO();
        const next = Math.max(0, (daily[today] || 0) + add);
        if (next === 0) delete daily[today];
        else daily[today] = next;
        saveJSON(STORAGE.dailyMinutes, daily);
        renderDashboard();
        // micro feedback animation
        b.style.transform = 'scale(0.94)';
        setTimeout(() => (b.style.transform = ''), 100);
      });
    });
  }

  // ---------- This week content ----------

  function renderThisWeek() {
    const box = document.getElementById('this-week');
    if (!box) return;

    const startDate = localStorage.getItem(STORAGE.startDate);
    const day = daysSince(startDate);
    if (day == null || day < 0) {
      box.innerHTML = '<p class="g-empty">Configura tu fecha de inicio arriba para ver qué te toca.</p>';
      return;
    }

    const month = Math.floor(day / 30) + 1;
    const week = Math.floor(day / 7) + 1;

    let items = [];

    if (month <= 2) {
      items = [
        'Avanzar en <em>Cómo leer un libro</em> de Adler',
        '1 vídeo de CrashCourse Philosophy sobre falacias',
        '≥3 falacias en el log esta semana',
        'Ritual diario: 10 min de lectura en voz alta',
      ];
    } else if (month <= 8) {
      items = [
        'Libro primario fase 1 (Platón → Maquiavelo → Hobbes → Rousseau → Mill)',
        '1 clase de Yale PLSC 114 (Steven Smith)',
        'Ficha semanal en <code>lecturas/</code>',
        'Grabación de 3-5 min resumiendo lo leído',
      ];
    } else if (month <= 12) {
      items = [
        'Fase 2 economía: Chang → Smith → Marx → Mariátegui',
        'Curso de David Harvey en YouTube acompañando a Marx',
        'M3 Pluriverso: Said <em>Orientalismo</em> en paralelo',
      ];
    } else if (month <= 17) {
      items = [
        'Fase 3: Weber fijo + 3 de 5 corrientes',
        'M3: Fanon <em>Los condenados de la tierra</em>',
        'Informe trimestral: Elcano + V-Dem',
      ];
    } else if (month <= 22) {
      items = [
        'Fase 4: Bolívar/Martí → Bueno/Armesilla → Dussel/Quijano/Cusicanqui',
        'Cinco emancipaciones: Freire + Gutiérrez',
        'fgbueno.es + CLACSO TV + entrevistas a Rivera Cusicanqui',
      ];
    } else if (month <= 28) {
      items = [
        'Fase 5: Mearsheimer + novela política + relectura',
        'Ensayo final 1500-2000 palabras',
        'Grabación de 10 min argumentando una tesis',
      ];
    } else {
      items = ['Plan completado · releer mejores notas + nuevo proyecto propio'];
    }

    box.innerHTML = `<p style="font-size: 0.72rem; color: var(--g-label);">Semana ${week} · Mes ${month}</p><ul>${items.map((i) => `<li>${i}</li>`).join('')}</ul>`;
  }

  // ---------- Falacia capture form ----------

  function escapeHTML(s) {
    return (s || '').replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function renderFalacias() {
    const list = document.getElementById('fal-list');
    if (!list) return;
    const entries = loadJSON(STORAGE.falacias, []);
    if (entries.length === 0) {
      list.innerHTML = '<p class="g-empty">Aún no hay capturas. Añade una arriba.</p>';
      return;
    }
    list.innerHTML = entries.slice().reverse().map((e, i) => `
      <div class="falacia-entry">
        <div class="meta">
          <span>${e.date}</span><span>${escapeHTML(e.source)}</span><span>${escapeHTML(e.family)} · ${escapeHTML(e.name)}</span>
        </div>
        <p class="quote">"${escapeHTML(e.quote)}"</p>
        <p><strong>Respuesta:</strong> ${escapeHTML(e.reply)}</p>
        <button data-idx="${entries.length - 1 - i}" class="g-btn fal-delete">Eliminar</button>
      </div>`).join('');
    list.querySelectorAll('.fal-delete').forEach((btn) => {
      btn.addEventListener('click', (ev) => {
        const idx = parseInt(ev.target.dataset.idx, 10);
        const cur = loadJSON(STORAGE.falacias, []);
        cur.splice(idx, 1);
        saveJSON(STORAGE.falacias, cur);
        renderFalacias();
      });
    });
  }

  function setupFalacias() {
    const dateEl = document.getElementById('fal-date');
    const saveBtn = document.getElementById('fal-save');
    const exportBtn = document.getElementById('fal-export');
    if (!saveBtn) return;

    if (dateEl) dateEl.value = todayISO();

    saveBtn.addEventListener('click', () => {
      const entry = {
        date: document.getElementById('fal-date').value || todayISO(),
        source: document.getElementById('fal-source').value.trim(),
        quote: document.getElementById('fal-quote').value.trim(),
        family: document.getElementById('fal-family').value,
        name: document.getElementById('fal-name').value.trim(),
        reply: document.getElementById('fal-reply').value.trim(),
      };
      const status = document.getElementById('fal-status');
      if (!entry.source || !entry.quote || !entry.family) {
        status.textContent = 'Faltan campos: medio, cita y familia.';
        status.classList.remove('success');
        return;
      }
      const entries = loadJSON(STORAGE.falacias, []);
      entries.push(entry);
      saveJSON(STORAGE.falacias, entries);
      status.textContent = `Guardada (${entries.length})`;
      status.classList.add('success');
      ['fal-source', 'fal-quote', 'fal-name', 'fal-reply'].forEach((id) => (document.getElementById(id).value = ''));
      document.getElementById('fal-family').value = '';
      renderFalacias();
    });

    exportBtn.addEventListener('click', () => {
      const entries = loadJSON(STORAGE.falacias, []);
      if (entries.length === 0) {
        document.getElementById('fal-status').textContent = 'Nada que exportar';
        return;
      }
      const header = '| Fecha | Medio / autor | Cita corta | Familia | Falacia | Mi respuesta |\n|---|---|---|---|---|---|\n';
      const rows = entries.map((e) => `| ${e.date} | ${e.source} | "${e.quote.replace(/\|/g, '\\|')}" | ${e.family} | ${e.name} | ${e.reply.replace(/\|/g, '\\|')} |`).join('\n');
      const md = `# Log de falacias\n\nExportado ${todayISO()} · ${entries.length} capturas.\n\n${header}${rows}\n`;
      const blob = new Blob([md], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `falacias-log-${todayISO()}.md`;
      a.click();
      URL.revokeObjectURL(url);
    });

    renderFalacias();
  }

  // ---------- Template cards (download / copy / create on GitHub) ----------

  const REPO_URL = 'https://github.com/MrSpagVi/Libros-Politica';

  function getTemplateContent(card) {
    // Find the first <code> inside the <details><pre><code> structure
    const code = card.querySelector('.template-content pre code, .template-content code');
    if (!code) return '';
    // Strip trailing newlines, preserve internal whitespace
    return code.textContent.replace(/\n+$/, '') + '\n';
  }

  function todayDateForFilename() {
    return todayISO().replace(/-/g, '-');
  }

  function setupTemplateCards() {
    const cards = document.querySelectorAll('.template-card');
    cards.forEach((card) => {
      const filenameTpl = card.dataset.filename || 'plantilla.md';
      const path = card.dataset.path || 'docs';
      // Replace $DATE in filename with today
      const filename = filenameTpl.replace('$DATE', todayDateForFilename());

      const downloadBtn = card.querySelector('[data-action="download"]');
      const copyBtn = card.querySelector('[data-action="copy"]');
      const ghLink = card.querySelector('[data-action="github"]');

      // GitHub "new file" URL — opens editor with filename suggested; user pastes content
      if (ghLink) {
        const ghUrl = `${REPO_URL}/new/main/${path}?filename=${encodeURIComponent(filename)}`;
        ghLink.href = ghUrl;
      }

      if (downloadBtn) {
        downloadBtn.addEventListener('click', () => {
          const content = getTemplateContent(card);
          if (!content.trim()) {
            alert('No se pudo leer la plantilla. Recarga la página.');
            return;
          }
          const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = filename;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          flashButton(downloadBtn, 'Descargada ✓');
        });
      }

      if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
          const content = getTemplateContent(card);
          try {
            await navigator.clipboard.writeText(content);
            flashButton(copyBtn, 'Copiada ✓');
          } catch (e) {
            // Fallback: select the code block text
            const code = card.querySelector('.template-content code');
            if (code) {
              const range = document.createRange();
              range.selectNodeContents(code);
              const sel = window.getSelection();
              sel.removeAllRanges();
              sel.addRange(range);
              flashButton(copyBtn, 'Seleccionada, Ctrl+C');
            }
          }
        });
      }
    });
  }

  function flashButton(btn, text) {
    const original = btn.textContent;
    btn.textContent = text;
    btn.style.borderColor = 'var(--g-accent)';
    setTimeout(() => {
      btn.textContent = original;
      btn.style.borderColor = '';
    }, 1500);
  }

  // ---------- Task list persistence ----------

  function persistTaskLists() {
    const items = document.querySelectorAll('.md-typeset .task-list-item');
    if (items.length === 0) return;
    const pageKey = `lp.tasks.${location.pathname}`;
    const state = loadJSON(pageKey, {});
    items.forEach((li, idx) => {
      const cb = li.querySelector('input[type="checkbox"]');
      if (!cb) return;
      const key = `${idx}::${li.textContent.trim().slice(0, 80)}`;
      if (state[key]) cb.checked = true;
      cb.addEventListener('change', () => {
        const cur = loadJSON(pageKey, {});
        if (cb.checked) cur[key] = true;
        else delete cur[key];
        saveJSON(pageKey, cur);
      });
    });
  }

  // ---------- Curso progress meter (per-page fallback) ----------

  function setupCursoProgress() {
    const box = document.getElementById('curso-progress');
    if (!box) return;
    // If global progress already rendered into this box, skip.
    if (box.dataset.globalRendered === '1') return;
    const items = document.querySelectorAll('.md-typeset .task-list-item input[type="checkbox"]');
    if (items.length === 0) return;
    const total = items.length;
    const elCompleted = document.getElementById('curso-completed');
    const elTotal = document.getElementById('curso-total');
    const elPct = document.getElementById('curso-pct');
    const elBar = document.getElementById('curso-bar');
    if (elTotal) elTotal.textContent = total;
    box.style.display = '';

    function update() {
      const checked = document.querySelectorAll('.md-typeset .task-list-item input[type="checkbox"]:checked').length;
      const pct = total > 0 ? Math.round((checked / total) * 100) : 0;
      if (elCompleted) elCompleted.textContent = checked;
      if (elPct) elPct.textContent = pct + '%';
      if (elBar) elBar.style.width = pct + '%';
    }
    items.forEach(cb => cb.addEventListener('change', update));
    setTimeout(update, 50);
  }

  // ---------- Tronco común — global progress (11 etapas) ----------
  // Source of truth: localStorage keys `lp.tasks.<path>` written by persistTaskLists.
  // Totals are hardcoded — if you edit checkbox counts in an etapa file, update here too.
  const ETAPAS = [
    { slug: 'etapa-01-setup-notas',            total: 5 },
    { slug: 'etapa-02-tutorial-notas',         total: 2 },
    { slug: 'etapa-03-falacias-familias',      total: 3 },
    { slug: 'etapa-04-dia-1-adler',            total: 4 },
    { slug: 'etapa-05-adler-2-4',              total: 4 },
    { slug: 'etapa-06-primera-ficha',          total: 4 },
    { slug: 'etapa-07-primera-nota-permanente',total: 4 },
    { slug: 'etapa-08-schopenhauer',           total: 3 },
    { slug: 'etapa-09-falacias-top-5',         total: 2 },
    { slug: 'etapa-10-maquiavelo',             total: 4 },
    { slug: 'etapa-11-hobbes',                 total: 4 }
  ];

  function etapaPathCandidates(slug) {
    // MkDocs builds with directory URLs by default → `/etapas/etapa-XX-foo/`.
    // Site is served under `/Libros-Politica/` on GitHub Pages. We accept both
    // shapes (with and without trailing slash, with and without base) so the
    // logic also works on local `mkdocs serve` at `/etapas/...`.
    const base = location.pathname.match(/^(\/[^/]+)\/?$/) ||
                 location.pathname.match(/^(\/[^/]+)\//);
    const prefixes = ['', '/Libros-Politica'];
    if (base && base[1] && !prefixes.includes(base[1])) prefixes.push(base[1]);
    const paths = [];
    prefixes.forEach(p => {
      paths.push(`${p}/etapas/${slug}/`);
      paths.push(`${p}/etapas/${slug}`);
    });
    return paths;
  }

  function countCompletedForEtapa(slug) {
    for (const path of etapaPathCandidates(slug)) {
      const state = loadJSON(`lp.tasks.${path}`, null);
      if (state && typeof state === 'object') {
        return Object.values(state).filter(Boolean).length;
      }
    }
    return 0;
  }

  function renderGlobalProgressInto(box) {
    if (!box) return;
    const elCompleted = box.querySelector('#curso-completed');
    const elTotal = box.querySelector('#curso-total');
    const elPct = box.querySelector('#curso-pct');
    const elBar = box.querySelector('#curso-bar');
    const total = ETAPAS.reduce((s, e) => s + e.total, 0);
    const completed = ETAPAS.reduce((s, e) => s + Math.min(countCompletedForEtapa(e.slug), e.total), 0);
    const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
    if (elCompleted) elCompleted.textContent = completed;
    if (elTotal) elTotal.textContent = total;
    if (elPct) elPct.textContent = pct + '%';
    if (elBar) elBar.style.width = pct + '%';
    box.style.display = '';
    box.dataset.globalRendered = '1';
  }

  function setupCursoGlobalProgress() {
    const boxes = [
      document.getElementById('curso-progress'),
      document.getElementById('curso-progress-mini')
    ].filter(Boolean);
    if (boxes.length === 0) return;
    boxes.forEach(renderGlobalProgressInto);
    // Re-render after any checkbox toggle on this page (state lives in localStorage,
    // and persistTaskLists' change handler runs first because it was registered first).
    const items = document.querySelectorAll('.md-typeset .task-list-item input[type="checkbox"]');
    items.forEach(cb => cb.addEventListener('change', () => boxes.forEach(renderGlobalProgressInto)));
  }

  // ---------- Legacy migration: curso.md monolith → 11 etapas ----------
  // The old /curso/ page held all 11 etapas' checkboxes. After the split, those
  // localStorage entries are orphan. We translate them into the new per-etapa keys
  // using substrings of the task text (stable across the migration).
  function migrateCursoTaskState() {
    const FLAG = 'lp.tasks.migrated.v1';
    if (localStorage.getItem(FLAG)) return;
    const oldCandidates = [
      'lp.tasks./Libros-Politica/curso/',
      'lp.tasks./curso/',
      'lp.tasks./Libros-Politica/curso',
      'lp.tasks./curso'
    ];
    let oldKey = null;
    let oldState = null;
    for (const k of oldCandidates) {
      const raw = localStorage.getItem(k);
      if (raw) {
        try {
          const parsed = JSON.parse(raw);
          if (parsed && typeof parsed === 'object' && Object.keys(parsed).length > 0) {
            oldKey = k;
            oldState = parsed;
            break;
          }
        } catch (e) { /* ignore */ }
      }
    }
    if (!oldState) {
      localStorage.setItem(FLAG, '1');
      return;
    }

    // Each entry: substring(s) that appear in old text → target etapa slug + index in the new file.
    const MAP = [
      // Etapa 1
      { match: 'Sistema de notas',          slug: 'etapa-01-setup-notas',             newIdx: 0, newText: 'Leer la página Sistema de notas (~15 min)' },
      { match: 'Elegir un workflow',        slug: 'etapa-01-setup-notas',             newIdx: 1, newText: 'Elegir un workflow: papel · Notion · híbrido (recomendado)' },
      { match: 'Comprar materiales',        slug: 'etapa-01-setup-notas',             newIdx: 2, newText: 'Comprar materiales si elegiste papel/híbrido' },
      { match: 'Configurar setup digital',  slug: 'etapa-01-setup-notas',             newIdx: 3, newText: 'Configurar setup digital si elegiste Notion/Obsidian' },
      { match: 'Poner fecha de inicio',     slug: 'etapa-01-setup-notas',             newIdx: 4, newText: 'Poner fecha de inicio en el panel' },
      // Etapa 2
      { match: 'Tutorial de 30 días, hacer días 1-7', slug: 'etapa-02-tutorial-notas', newIdx: 0, newText: 'Tutorial de 30 días: hacer días 1-7' },
      { match: 'días 8-30 se hacen en paralelo',      slug: 'etapa-02-tutorial-notas', newIdx: 1, newText: 'Los días 8-30 se hacen en paralelo' },
      // Etapa 3
      { match: 'Leer entrada Falacias',     slug: 'etapa-03-falacias-familias',       newIdx: 0, newText: 'Leer entrada Falacias — Empezar acá' },
      { match: 'primera falacia',           slug: 'etapa-03-falacias-familias',       newIdx: 1, newText: 'Capturar tu primera falacia' },
      // Etapa 4
      { match: 'Yale PLSC clase 1',         slug: 'etapa-04-dia-1-adler',             newIdx: 0, newText: 'Mirar primeros 10 min de Yale PLSC clase 1' },
      { match: 'Cómo leer un libro',        slug: 'etapa-04-dia-1-adler',             newIdx: 1, newText: 'Empezar Adler — Cómo leer un libro' },
      { match: 'Capturar 1 falacia más',    slug: 'etapa-04-dia-1-adler',             newIdx: 2, newText: 'Capturar 1 falacia más' },
      { match: 'Marcar 30 min en el contador', slug: 'etapa-04-dia-1-adler',          newIdx: 3, newText: 'Marcar 30 min en el contador del panel' },
      // Etapa 5
      { match: 'Adler caps 2-4',            slug: 'etapa-05-adler-2-4',               newIdx: 0, newText: 'Adler caps 2-4 (lectura analítica + sintópica)' },
      { match: 'Yale PLSC clase 2',         slug: 'etapa-05-adler-2-4',               newIdx: 1, newText: 'Yale PLSC clase 2' },
      { match: '3 falacias capturadas',     slug: 'etapa-05-adler-2-4',               newIdx: 2, newText: '3 falacias capturadas durante la semana' },
      { match: 'días 8-14',                 slug: 'etapa-05-adler-2-4',               newIdx: 3, newText: 'Tutorial de notas: avanzar a días 8-14' },
      // Etapa 6
      { match: 'Adler caps 5-7',            slug: 'etapa-06-primera-ficha',           newIdx: 0, newText: 'Adler caps 5-7' },
      { match: 'Yale PLSC clase 3',         slug: 'etapa-06-primera-ficha',           newIdx: 1, newText: 'Yale PLSC clase 3' },
      { match: 'primera literature note',   slug: 'etapa-06-primera-ficha',           newIdx: 2, newText: 'Escribir tu primera literature note completa sobre Adler' },
      { match: 'días 15-21',                slug: 'etapa-06-primera-ficha',           newIdx: 3, newText: 'Tutorial de notas: días 15-21' },
      // Etapa 7
      { match: 'Adler cap 8',               slug: 'etapa-07-primera-nota-permanente', newIdx: 0, newText: 'Adler cap 8 (síntesis)' },
      { match: 'primera nota permanente real', slug: 'etapa-07-primera-nota-permanente', newIdx: 1, newText: 'Escribir tu primera nota permanente real' },
      { match: 'Grabarte 5-10 min',         slug: 'etapa-07-primera-nota-permanente', newIdx: 2, newText: 'Grabarte 5-10 min explicando una idea de Adler' },
      { match: 'días 22-30',                slug: 'etapa-07-primera-nota-permanente', newIdx: 3, newText: 'Tutorial de notas: días 22-30' },
      // Etapa 8
      { match: 'Schopenhauer',              slug: 'etapa-08-schopenhauer',            newIdx: 0, newText: 'Schopenhauer — El arte de tener razón' },
      { match: '5 estratagemas de Schopenhauer', slug: 'etapa-08-schopenhauer',       newIdx: 1, newText: 'Identificar 5 estratagemas de Schopenhauer en un debate real' },
      { match: '10-15 capturas',            slug: 'etapa-08-schopenhauer',            newIdx: 2, newText: 'Ya tenés ~10-15 capturas de falacias en tu log' },
      // Etapa 9
      { match: 'Las 5 más frecuentes',      slug: 'etapa-09-falacias-top-5',          newIdx: 0, newText: 'Leer Las 5 más frecuentes' },
      { match: 'Releer tus capturas previas', slug: 'etapa-09-falacias-top-5',        newIdx: 1, newText: 'Releer tus capturas previas e identificar nombre concreto' },
      // Etapa 10
      { match: 'Maquiavelo — El Príncipe',  slug: 'etapa-10-maquiavelo',              newIdx: 0, newText: 'Maquiavelo — El Príncipe' },
      { match: 'Yale PLSC clases 6-8',      slug: 'etapa-10-maquiavelo',              newIdx: 1, newText: 'Yale PLSC clases 6-8 (Maquiavelo)' },
      { match: 'lecturas/maquiavelo',       slug: 'etapa-10-maquiavelo',              newIdx: 2, newText: 'Ficha de lectura completa en lecturas/maquiavelo.md' },
      { match: 'virtù vs fortuna',          slug: 'etapa-10-maquiavelo',              newIdx: 3, newText: '1 nota permanente sobre virtù vs fortuna' },
      // Etapa 11
      { match: 'Hobbes — Leviatán',         slug: 'etapa-11-hobbes',                  newIdx: 0, newText: 'Hobbes — Leviatán (selección caps. 13-21)' },
      { match: 'Yale PLSC clases 9-11',     slug: 'etapa-11-hobbes',                  newIdx: 1, newText: 'Yale PLSC clases 9-11 (Hobbes)' },
      { match: 'monopolio de la violencia', slug: 'etapa-11-hobbes',                  newIdx: 2, newText: 'Ficha de lectura + 1 nota permanente sobre el monopolio de la violencia' },
      { match: 'Auto-test de falacias',     slug: 'etapa-11-hobbes',                  newIdx: 3, newText: 'Auto-test de falacias (si tenés 20+ capturas)' }
    ];

    // Build per-etapa new state objects.
    const newStates = {};
    Object.entries(oldState).forEach(([oldKey, val]) => {
      if (!val) return;
      const rule = MAP.find(r => oldKey.indexOf(r.match) !== -1);
      if (!rule) return;
      const newKey = `${rule.newIdx}::${rule.newText.slice(0, 80)}`;
      if (!newStates[rule.slug]) newStates[rule.slug] = {};
      newStates[rule.slug][newKey] = true;
    });

    // Write — pick the prefix used by the current host (matches what persistTaskLists writes today).
    const prefix = location.pathname.startsWith('/Libros-Politica') ? '/Libros-Politica' : '';
    Object.entries(newStates).forEach(([slug, state]) => {
      const target = `lp.tasks.${prefix}/etapas/${slug}/`;
      const existing = loadJSON(target, {});
      saveJSON(target, Object.assign({}, existing, state));
    });

    localStorage.setItem(FLAG, '1');
    // Note: we keep the old key for one more release as a safety net.
  }

  // ---------- Boot ----------

  function boot() {
    migrateCursoTaskState();
    startClock();
    renderDashboard();
    setupStartDate();
    setupTimeButtons();
    renderThisWeek();
    setupFalacias();
    setupTemplateCards();
    persistTaskLists();
    setupCursoGlobalProgress();
    setupCursoProgress();
  }

  if (typeof document$ !== 'undefined') {
    // eslint-disable-next-line no-undef
    document$.subscribe(() => {
      if (clockTimer) clearInterval(clockTimer);
      boot();
    });
  } else if (document.readyState !== 'loading') {
    boot();
  } else {
    document.addEventListener('DOMContentLoaded', boot);
  }
})();
