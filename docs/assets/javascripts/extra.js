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
    if (day < 0) return ['no empezado', '—'];
    const month = Math.floor(day / 30) + 1;
    if (month <= 2) return ['0 · cimientos', month];
    if (month <= 8) return ['1 · filosofía clásica', month];
    if (month <= 12) return ['2 · economía política', month];
    if (month <= 17) return ['3 · sociopolítica s.xx', month];
    if (month <= 22) return ['4 · iberoamericana', month];
    if (month <= 28) return ['5 · síntesis', month];
    return ['plan completado', month];
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
      dayEl.textContent = `día ${day + 1} del plan`;
      const [phaseLabel, monthNum] = phaseFor(day);
      phaseEl.textContent = phaseLabel;
      monthEl.textContent = `${monthNum} / 28`;
      const week = Math.floor(day / 7) + 1;
      weekglobalEl.textContent = `${week} / 120`;
      const pct = Math.min(100, ((day + 1) / (28 * 30)) * 100);
      progressBar.style.width = pct.toFixed(1) + '%';
    } else {
      dayEl.textContent = 'configura tu inicio ↓';
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
      streakBestEl.textContent = `récord ${streak}`;
    } else {
      streakBestEl.textContent = `récord ${best}`;
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
      status.textContent = `guardado: ${fmtDateES(stored)}`;
      status.classList.add('success');
    }

    button.addEventListener('click', () => {
      const value = input.value;
      if (!value) {
        status.textContent = 'elige una fecha';
        status.classList.remove('success');
        return;
      }
      localStorage.setItem(STORAGE.startDate, value);
      status.textContent = `guardado: ${fmtDateES(value)}`;
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
      box.innerHTML = '<p class="g-empty">configura tu fecha de inicio arriba para ver qué te toca.</p>';
      return;
    }

    const month = Math.floor(day / 30) + 1;
    const week = Math.floor(day / 7) + 1;

    let items = [];

    if (month <= 2) {
      items = [
        'avanzar en <em>Cómo leer un libro</em> de Adler',
        '1 vídeo de CrashCourse Philosophy sobre falacias',
        '≥3 falacias en el log esta semana',
        'ritual diario: 10 min lectura en voz alta',
      ];
    } else if (month <= 8) {
      items = [
        'libro primario fase 1 (Platón → Maquiavelo → Hobbes → Rousseau → Mill)',
        '1 clase Yale PLSC 114 (Steven Smith)',
        'ficha semanal en <code>lecturas/</code>',
        'grabación de 3-5 min resumiendo lo leído',
      ];
    } else if (month <= 12) {
      items = [
        'fase 2 economía: Chang → Smith → Marx → Mariátegui',
        'curso David Harvey en YouTube acompañando a Marx',
        'M3 pluriverso: Said <em>Orientalismo</em> en paralelo',
      ];
    } else if (month <= 17) {
      items = [
        'fase 3: Weber fijo + 3 de 5 corrientes',
        'M3: Fanon <em>Los condenados de la tierra</em>',
        'informe trimestral: Elcano + V-Dem',
      ];
    } else if (month <= 22) {
      items = [
        'fase 4: Bolívar/Martí → Bueno/Armesilla → Dussel/Quijano/Cusicanqui',
        'cinco emancipaciones: Freire + Gutiérrez',
        'fgbueno.es + CLACSO TV + entrevistas a Rivera Cusicanqui',
      ];
    } else if (month <= 28) {
      items = [
        'fase 5: Mearsheimer + novela política + relectura',
        'ensayo final 1500-2000 palabras',
        'grabación 10 min argumentando una tesis',
      ];
    } else {
      items = ['plan completado · releer mejores notas + nuevo proyecto propio'];
    }

    box.innerHTML = `<p style="font-size: 0.72rem; color: var(--g-label);">semana ${week} · mes ${month}</p><ul>${items.map((i) => `<li>${i}</li>`).join('')}</ul>`;
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
      list.innerHTML = '<p class="g-empty">aún no hay capturas. añade una arriba.</p>';
      return;
    }
    list.innerHTML = entries.slice().reverse().map((e, i) => `
      <div class="falacia-entry">
        <div class="meta">
          <span>${e.date}</span><span>${escapeHTML(e.source)}</span><span>${escapeHTML(e.family)} · ${escapeHTML(e.name)}</span>
        </div>
        <p class="quote">"${escapeHTML(e.quote)}"</p>
        <p><strong>respuesta:</strong> ${escapeHTML(e.reply)}</p>
        <button data-idx="${entries.length - 1 - i}" class="g-btn fal-delete">eliminar</button>
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
        status.textContent = 'faltan campos: medio, cita y familia.';
        status.classList.remove('success');
        return;
      }
      const entries = loadJSON(STORAGE.falacias, []);
      entries.push(entry);
      saveJSON(STORAGE.falacias, entries);
      status.textContent = `guardada (${entries.length})`;
      status.classList.add('success');
      ['fal-source', 'fal-quote', 'fal-name', 'fal-reply'].forEach((id) => (document.getElementById(id).value = ''));
      document.getElementById('fal-family').value = '';
      renderFalacias();
    });

    exportBtn.addEventListener('click', () => {
      const entries = loadJSON(STORAGE.falacias, []);
      if (entries.length === 0) {
        document.getElementById('fal-status').textContent = 'nada que exportar';
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

  // ---------- Boot ----------

  function boot() {
    startClock();
    renderDashboard();
    setupStartDate();
    setupTimeButtons();
    renderThisWeek();
    setupFalacias();
    persistTaskLists();
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
