
        // Los datos del curso se cargan desde assets/course-data.js (window.COURSE_DATA).
        const COURSE_DATA = window.COURSE_DATA || [];

        // Rutas derivadas de los datos (cada etapa declara sus tracks). Agregar una
        // etapa con sus tracks actualiza esto automaticamente; nada hardcodeado.
        const TRACK_SIMPLE = COURSE_DATA.filter(s => (s.tracks || []).includes('simple')).map(s => s.stage);
        const TRACK_INTERMEDIATE = COURSE_DATA.filter(s => (s.tracks || []).includes('intermediate')).map(s => s.stage);
        const TRACK_ADVANCED = COURSE_DATA.filter(s => (s.tracks || []).includes('advanced')).map(s => s.stage);

        const QUIZ_QUESTIONS = {
            0: [
                { q: "¿Cuál es la diferencia entre notas de lectura y notas permanentes en el método Zettelkasten?", a: "Las notas de lectura resumen contenidos del texto original; las notas permanentes expresan ideas propias de forma autónoma en el fichero." },
                { q: "¿Por qué Adler insiste en anotar un libro para leer activamente?", a: "Anotar mantiene despierto al lector, estimula la reflexión crítica y ayuda a conectar los conceptos con el propio pensamiento." }
            ],
            1: [
                { q: "¿Cómo se diferencia el estado de naturaleza de Hobbes del de Locke?", a: "Para Hobbes es una guerra constante de todos contra todos por autoconservación; para Locke es una paz relativa regulada por ley natural, pero sin protección eficaz." },
                { q: "¿Qué caracteriza al filósofo-rey de Platón en La República?", a: "Une el conocimiento supremo del Bien con el poder estatal, previniendo la demagogia de las masas en la asamblea." }
            ],
            2: [
                { q: "¿Qué es la división del trabajo según Adam Smith?", a: "Es la especialización de tareas en la manufactura, incrementando la productividad y generando riqueza colectiva." },
                { q: "¿Cómo define Marx la plusvalía en El Capital?", a: "Es el valor del trabajo excedente no remunerado al obrero, el cual es apropiado por el poseedor de capital." }
            ],
            3: [
                { q: "¿Cuáles son los tipos de dominación legítima según Weber?", a: "Dominación racional-legal (leyes), tradicional (costumbres e historia) y carismática (heroísmo o virtudes de un líder)." },
                { q: "¿En qué consiste la justicia como equidad de Rawls?", a: "Principios acordados bajo un velo de ignorancia que garantizan libertades iguales y que las desigualdades beneficien a los menos favorecidos." }
            ],
            4: [
                { q: "¿Qué plantea la teoría de colonialidad del poder de Quijano?", a: "El fin del colonialismo formal no eliminó la clasificación social racial del trabajo impuesta por la hegemonía eurocéntrica." }
            ],
            5: [
                { q: "¿Cómo define Carl Schmitt la distinción definitoria de lo político?", a: "La distinción amigo-enemigo, representando el nivel máximo de asociación o confrontación colectiva." }
            ],
            6: [
                { q: "¿Qué es la guerra de posiciones teórica en Gramsci?", a: "La lucha cultural en la sociedad civil para construir una hegemonía ideológica previa a la toma formal del poder estatal." }
            ],
            7: [
                { q: "¿Cómo describe Polanyi el doble movimiento del mercado autorregulado?", a: "La imposición de desincrustar el mercado genera una reacción social autodefensiva para proteger la naturaleza y la sociedad humana." }
            ],
            8: [
                { q: "¿Qué sostiene Berger sobre la relación entre ver y saber?", a: "La vista llega antes que las palabras: lo que sabemos o creemos afecta el modo en que vemos las cosas, y toda imagen encarna un modo de ver." }
            ],
            9: [
                { q: "¿Qué describe Foucault con el término biopolítica?", a: "Técnicas de soberanía estatal dirigidas a gestionar biológicamente los procesos colectivos de la población." }
            ]
        };

        let selectedStageNum = null;
        // Exponer selectedStageNum en window (las variables let no son propiedades de window por defecto).
        try { Object.defineProperty(window, 'selectedStageNum', { get: function() { return selectedStageNum; }, configurable: true }); } catch (e) {}
        let searchQuery = "";
        let openPhases = {0: true};  // {phaseIndex: bool} -- soporta fases dinamicas
        let activeTrack = 'advanced';
        
        function init() {
            // Load key preferences
            activeTrack = localStorage.getItem('active-track') || 'advanced';
            document.getElementById('track-selector').value = activeTrack;
            // Etiquetas del selector de ruta con conteos reales (data-driven).
            const _tn = { simple: 'Ruta Simple', intermediate: 'Ruta Intermedia', advanced: 'Ruta Avanzada' };
            const _tc = { simple: TRACK_SIMPLE.length, intermediate: TRACK_INTERMEDIATE.length, advanced: TRACK_ADVANCED.length };
            Object.keys(_tn).forEach(t => {
                const o = document.querySelector('#track-selector option[value="' + t + '"]');
                if (o) o.textContent = _tn[t] + ' (' + _tc[t] + ' etapas)';
            });
            
            // Sync theme button icon
            updateThemeIcon();
            applyReadTheme();
            applyFoco();

            loadCheckboxStates();
            renderNavigation();
            updateGlobalProgress();
            
            // Modal close listener on Esc
            window.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    closeBackupModal();
                }
            });
            
            // Router por hash: la URL decide qué se muestra. Cada etapa tiene su propia
            // dirección (curso.html#/etapa-9), con atrás/adelante del navegador y links directos.
            window.addEventListener('popstate', routeFromHash);
            window.addEventListener('hashchange', routeFromHash);
            routeFromHash();
        }

        function routeFromHash() {
            // Vista del plan Harada: curso.html#/harada
            if ((location.hash || '').indexOf('#/harada') === 0) {
                selectedStageNum = null;
                renderHaradaPage();
                return;
            }
            const m = (location.hash || '').match(/^#\/etapa-(\d+)/);
            let n = m ? parseInt(m[1], 10) : null;
            // Sin etapa en la URL: recuperar la ultima etapa de la sesion (apertura fresca).
            if (n === null) {
                const saved = localStorage.getItem('selected-stage-num');
                if (saved !== null) n = parseInt(saved, 10);
            }
            if (n !== null && COURSE_DATA.find(d => d.stage === n)) {
                selectStage(n);
                return;
            }
            // Nada que restaurar: home de la app.
            selectedStageNum = null;
            renderWelcomePage();
        }

        function goHome() {
            selectedStageNum = null;
            localStorage.removeItem('selected-stage-num');
            if (location.hash && location.hash !== '#/') {
                history.pushState(null, '', '#/');
            }
            renderWelcomePage();
        }

        function filterEmojis(text) {
            const emojiRegex = /[\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2600-\u26FF]|\uD83E[\uDD10-\uDDFF]/g;
            return text.replace(emojiRegex, '');
        }

        function stripHtmlTags(htmlStr) {
            return htmlStr.replace(/<[^>]*>/g, '');
        }

        function getStageIdeas(stage) {
            const secs = stage.sections || [];
            const ideaSec = secs.find(s => /idea/i.test(s.title)) || secs.find(s => /contexto/i.test(s.title)) || secs[0];
            return ideaSec ? ideaSec.html : '';
        }

        function saveApiKey(key) {
            localStorage.setItem('gemini-api-key', key.trim());
        }

        function toggleTheme() {
            const body = document.body;
            const currentTheme = body.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            body.setAttribute('data-theme', newTheme);
            
            updateThemeIcon();
        }

        function updateThemeIcon() {
            const theme = document.body.getAttribute('data-theme') || 'dark';
            const iconContainer = document.getElementById('theme-btn-icon');
            const textContainer = document.getElementById('theme-btn-text');
            
            if (theme === 'dark') {
                iconContainer.innerHTML = `<svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width:14px; height:14px; fill:none;"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
                textContainer.textContent = 'Modo Claro';
            } else {
                iconContainer.innerHTML = `<svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="width:14px; height:14px; fill:none;"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;
                textContainer.textContent = 'Modo Oscuro';
            }
        }
        
        function selectTrackFromWelcome(track) {
            const sel = document.getElementById('track-selector');
            if (sel) sel.value = track;
            changeTrack(track);
        }

        function changeTrack(trackValue) {
            activeTrack = trackValue;
            localStorage.setItem('active-track', trackValue);
            loadCheckboxStates();
            renderNavigation();
            updateGlobalProgress();
            
            if (selectedStageNum === null) {
                renderWelcomePage();
            } else {
                // If the selected stage is no longer in this track, go to the app home
                let trackStages = getActiveTrackStages();
                if (!trackStages.includes(selectedStageNum)) {
                    goHome();
                } else {
                    selectStage(selectedStageNum);
                }
            }
        }

        function getActiveTrackStages() {
            if (activeTrack === 'simple') return TRACK_SIMPLE;
            if (activeTrack === 'intermediate') return TRACK_INTERMEDIATE;
            return TRACK_ADVANCED;
        }

        // ---- Senda guiada: proxima etapa / continuar ----
        function isStageDone(stage) {
            if (!stage) return false;
            if (stage.tasks && stage.tasks.length > 0) return getStageStats(stage).pct === 1.0;
            return localStorage.getItem('visited-stage-' + stage.stage) === '1';
        }
        function getNextStageNum() {
            const t = getActiveTrackStages();
            for (let i = 0; i < t.length; i++) {
                const s = COURSE_DATA.find(d => d.stage === t[i]);
                if (s && !isStageDone(s)) return t[i];
            }
            return t.length ? t[t.length - 1] : null; // todo completo: ultima
        }
        function continueStudy() {
            const n = getNextStageNum();
            if (n !== null) selectStage(n);
        }
        function goNextFromStage(cur) {
            const t = getActiveTrackStages();
            const i = t.indexOf(cur);
            if (i >= 0 && i < t.length - 1) selectStage(t[i + 1]);
            else goHome();
        }

        // ---- Racha de estudio (dias con actividad) ----
        function markStudyToday() {
            let days = [];
            try { days = JSON.parse(localStorage.getItem('study-days') || '[]'); } catch (e) {}
            const today = new Date().toISOString().slice(0, 10);
            if (!days.includes(today)) { days.push(today); localStorage.setItem('study-days', JSON.stringify(days)); }
        }
        function getStreak() {
            let days = [];
            try { days = JSON.parse(localStorage.getItem('study-days') || '[]'); } catch (e) {}
            const set = new Set(days);
            const iso = x => x.toISOString().slice(0, 10);
            let d = new Date(), streak = 0;
            if (!set.has(iso(d))) d.setDate(d.getDate() - 1); // tolera no haber estudiado hoy todavia
            while (set.has(iso(d))) { streak++; d.setDate(d.getDate() - 1); }
            return streak;
        }

        // ---- Lectura editorial: tema de lectura y modo foco ----
        function setReadTheme(t) {
            document.documentElement.setAttribute('data-read', t);
            localStorage.setItem('read-theme', t);
            const wrap = document.querySelector('.read-themes');
            if (wrap) wrap.querySelectorAll('.rt-btn').forEach(b => b.classList.toggle('on', b.dataset.rt === t));
        }
        function applyReadTheme() {
            setReadTheme(localStorage.getItem('read-theme') || 'oscuro');
        }
        function toggleFoco() {
            const on = document.body.classList.toggle('foco');
            localStorage.setItem('foco', on ? '1' : '0');
            const btn = document.getElementById('foco-btn');
            if (btn) btn.textContent = on ? 'Salir de foco' : 'Modo foco';
        }
        function applyFoco() {
            if (localStorage.getItem('foco') === '1') document.body.classList.add('foco');
        }

        function loadCheckboxStates() {
            COURSE_DATA.forEach(stage => {
                stage.tasks.forEach((task, tIdx) => {
                    const key = `${activeTrack}-stage-${stage.stage}-task-${tIdx}`;
                    const saved = localStorage.getItem(key);
                    task.completed = saved === 'true';
                });
            });
        }
        
        function toggleTask(stageNum, taskIdx, checkbox) {
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            const task = stage.tasks[taskIdx];
            task.completed = checkbox.checked;
            
            const key = `${activeTrack}-stage-${stageNum}-task-${taskIdx}`;
            localStorage.setItem(key, checkbox.checked);
            if (checkbox.checked) markStudyToday();

            // Update UI elements
            const cardEl = document.getElementById(`task-card-${stageNum}-${taskIdx}`);
            if (checkbox.checked) {
                cardEl.classList.add('completed');
            } else {
                cardEl.classList.remove('completed');
            }
            
            updateGlobalProgress();
            updateStageProgressRing(stageNum);
        }
        
        function getStageStats(stage) {
            const total = stage.tasks.length;
            const completed = stage.tasks.filter(t => t.completed).length;
            const pct = total > 0 ? (completed / total) : 0;
            return { total, completed, pct };
        }
        
        function updateStageProgressRing(stageNum) {
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            const { pct } = getStageStats(stage);
            
            // Update sidebar ring
            const ringEl = document.getElementById(`ring-fill-${stageNum}`);
            if (ringEl) {
                const r = 7;
                const circ = 2 * Math.PI * r;
                const offset = circ - (pct * circ);
                ringEl.style.strokeDashoffset = offset;
            }
        }
        
        function updateGlobalProgress() {
            let total = 0;
            let completed = 0;
            
            let trackStages = getActiveTrackStages();
            
            COURSE_DATA.forEach(stage => {
                if (trackStages.includes(stage.stage)) {
                    stage.tasks.forEach(t => {
                        total++;
                        if (t.completed) completed++;
                    });
                }
            });
            
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            document.getElementById('global-pct-text').textContent = `${pct}%`;
            document.getElementById('global-progress-bar').style.width = `${pct}%`;
        }
        
        function togglePhaseCollapse(pIdx) {
            openPhases[pIdx] = !openPhases[pIdx];
            renderNavigation();
        }
        
        function handleSearch() {
            searchQuery = document.getElementById('search-box').value.toLowerCase().trim();
            renderNavigation();
        }
        
        function renderNavigation() {
            const scroller = document.getElementById('nav-scroller');
            const savedScrollTop = scroller ? scroller.scrollTop : 0;
            
            // Fases armadas dinamicamente desde los datos (soporta fases nuevas).
            let trackStages = getActiveTrackStages();
            const phaseMap = {};
            COURSE_DATA.forEach(stage => {
                if (trackStages.includes(stage.stage)) {
                    if (!phaseMap[stage.phase_index]) {
                        phaseMap[stage.phase_index] = { index: stage.phase_index, name: stage.phase_name, stages: [] };
                    }
                    phaseMap[stage.phase_index].stages.push(stage);
                }
            });
            const phases = Object.values(phaseMap).sort((a, b) => a.index - b.index);

            let html = '';
            
            phases.forEach(phase => {
                let filteredStages = phase.stages;
                if (searchQuery !== "") {
                    filteredStages = phase.stages.filter(s => {
                        const searchStr = `${s.stage} ${s.title} ${s.reading_type} ${s.english_title}`.toLowerCase();
                        return searchStr.includes(searchQuery);
                    });
                }
                
                if (searchQuery !== "" && filteredStages.length === 0) {
                    return;
                }
                
                const isOpen = searchQuery !== "" ? true : openPhases[phase.index];
                const caret = isOpen ? "▼" : "▶";
                
                // Get phase quiz completion status
                const isPassed = getPhaseQuizStatus(phase.index);
                const statusIndicator = isPassed ? `<span style="font-size:0.7rem; color:var(--accent); font-weight:bold; margin-right:0.25rem;">Aprobada</span>` : '';

                // Progreso de la fase (goal-gradient): cuantas etapas de la ruta estan completas.
                const pTotal = phase.stages.length;
                const pDone = phase.stages.filter(s => isStageDone(s)).length;
                const pPct = pTotal ? Math.round((pDone / pTotal) * 100) : 0;
                const almost = pTotal > 0 && pDone < pTotal && (pTotal - pDone) <= 2;

                html += `
                    <div class="phase-group${almost ? ' phase-almost' : ''}">
                        <button class="phase-header-btn" onclick="selectPhase(${phase.index})">
                            <span>${phase.name}</span>
                            <span style="font-size:0.7rem; color:var(--text-muted); display:flex; align-items:center; gap:0.4rem;">
                                ${statusIndicator}
                                <span class="phase-count">${pDone}/${pTotal}</span>
                                ${caret}
                            </span>
                        </button>
                        <div class="phase-mini-bar"><i style="width:${pPct}%"></i></div>
                        ${almost ? `<div class="phase-almost-note">Te faltan ${pTotal - pDone} para cerrar la fase</div>` : ''}
                        <div class="phase-stages-list" style="display: ${isOpen ? 'flex' : 'none'};">
                            ${filteredStages.map(s => {
                                const activeClass = s.stage === selectedStageNum ? 'active' : '';
                                const doneClass = isStageDone(s) ? 'done' : '';
                                const { pct } = getStageStats(s);
                                const circ = 2 * Math.PI * 7;
                                const offset = circ - (pct * circ);

                                return `
                                    <button class="stage-nav-item ${activeClass} ${doneClass}" onclick="selectStage(${s.stage})">
                                        <svg class="progress-ring-mini" viewBox="0 0 16 16">
                                            <circle class="ring-bg" cx="8" cy="8" r="7" />
                                            <circle class="ring-fill" id="ring-fill-${s.stage}" cx="8" cy="8" r="7" style="stroke-dashoffset: ${offset};" />
                                        </svg>
                                        <span style="flex-grow:1;">${s.stage}. ${s.title}</span>
                                    </button>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            });
            
            if (scroller) {
                scroller.innerHTML = html;
                scroller.scrollTop = savedScrollTop;
            }

            // Resaltar el acceso al plan Harada cuando es la vista activa.
            const hb = document.getElementById('harada-nav-btn');
            if (hb) hb.classList.toggle('active', selectedStageNum === null && (location.hash || '').indexOf('#/harada') === 0);
        }

        function selectPhase(pIdx) {
            selectedStageNum = null;
            const items = document.querySelectorAll('.stage-nav-item');
            items.forEach(it => it.classList.remove('active'));
            
            // Toggle sidebar expand state
            openPhases[pIdx] = !openPhases[pIdx];
            renderNavigation();
            
            const panel = document.getElementById('workspace-panel');
            const phaseStages = COURSE_DATA.filter(s => s.phase_index === pIdx);
            const trackStages = getActiveTrackStages();
            const visibleStages = phaseStages.filter(s => trackStages.includes(s.stage));
            
            let totalTasks = 0;
            let completedTasks = 0;
            visibleStages.forEach(s => {
                s.tasks.forEach(t => {
                    totalTasks++;
                    if (t.completed) completedTasks++;
                });
            });
            
            const pct = totalTasks > 0 ? Math.round((completedTasks / totalTasks) * 100) : 100;
            
            let quizWidgetHtml = '';
            if (visibleStages.length > 0) {
                quizWidgetHtml = `
                    <div class="socratic-assessment-widget" id="socratic-quiz-container">
                        <!-- Examen socrático renderizado dinámicamente -->
                    </div>
                `;
            } else {
                quizWidgetHtml = `
                    <div class="socratic-assessment-widget">
                        <p>No hay lecturas disponibles en tu ruta para esta fase.</p>
                    </div>
                `;
            }
            
            panel.innerHTML = `
                <div class="stage-hero">
                    <div class="stage-hero-meta">
                        <span class="hero-num-badge">Fase ${pIdx}</span>
                    </div>
                    <h2>Fase ${pIdx} — Resumen Teórico e Hitos</h2>
                </div>
                
                <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem;">
                    <h3>Estado del Módulo</h3>
                    <p style="font-size: 1.1rem; font-family: var(--font-editorial); margin-top: 0.5rem;">
                        Has completado <strong>${completedTasks}</strong> de <strong>${totalTasks}</strong> tareas (${pct}%).
                    </p>
                    <div style="height: 8px; background: rgba(255,255,255,0.05); border-radius: 999px; overflow: hidden; margin-top: 0.75rem; border: 1px solid var(--border-color);">
                        <div style="width: ${pct}%; height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent));"></div>
                    </div>
                </div>
                
                <div style="margin-top: 1.5rem;">
                    <h3>Evaluación Socrática de la Fase</h3>
                    <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">
                        El paso final para marcar esta fase como acreditada es responder correctamente el control socrático.
                    </p>
                    ${quizWidgetHtml}
                </div>
            `;
            
            if (visibleStages.length > 0) {
                renderSocraticQuiz(pIdx);
            }
            
            // Reset right sidebar
            const right = document.getElementById('sidebar-right');
            right.innerHTML = `
                <div class="workspace-welcome" style="text-align:center; height:auto;">
                    <p>Selecciona una etapa individual de la barra lateral para ver su checklist de tareas.</p>
                </div>
            `;
        }

        function getPhaseQuizStatus(pIdx) {
            const questions = QUIZ_QUESTIONS[pIdx] || [];
            if (questions.length === 0) return true;
            
            const key = `socratic-quiz-phase-${pIdx}`;
            const saved = localStorage.getItem(key);
            if (saved) {
                const state = JSON.parse(saved);
                return state.passed === true;
            }
            return false;
        }

        function renderSocraticQuiz(pIdx) {
            const container = document.getElementById('socratic-quiz-container');
            if (!container) return;
            
            const questions = QUIZ_QUESTIONS[pIdx] || [];
            if (questions.length === 0) {
                container.innerHTML = `
                    <div style="background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; text-align: center;">
                        <p>Evaluación socrática no requerida. Fase desbloqueada.</p>
                    </div>
                `;
                return;
            }
            
            const key = `socratic-quiz-phase-${pIdx}`;
            let state = { currentQuestionIdx: 0, correctCount: 0, passed: false, failed: false };
            const saved = localStorage.getItem(key);
            if (saved) {
                state = JSON.parse(saved);
            } else {
                localStorage.setItem(key, JSON.stringify(state));
            }
            
            if (state.passed) {
                container.innerHTML = `
                    <div style="background: var(--bg-card); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 1.5rem; text-align: center;">
                        <p style="color: var(--accent); font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">Examen Socrático Aprobado</p>
                        <p style="font-size: 0.9rem; color: var(--text-muted);">Has respondido todas las preguntas críticas del módulo.</p>
                        <button class="theme-toggle-btn" style="margin: 1rem auto 0 auto;" onclick="resetQuiz(${pIdx})">Reiniciar Examen</button>
                    </div>
                `;
                return;
            }
            
            if (state.failed) {
                container.innerHTML = `
                    <div style="background: var(--bg-card); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 1.5rem; text-align: center;">
                        <p style="color: #ef4444; font-weight: bold; font-size: 1.1rem; margin-bottom: 0.5rem;">Examen No Superado</p>
                        <p style="font-size: 0.9rem; color: var(--text-muted); margin-bottom: 1rem;">Debes responder de forma óptima para poder completar la fase.</p>
                        <button class="theme-toggle-btn" style="margin: 0 auto;" onclick="resetQuiz(${pIdx})">Reintentar</button>
                    </div>
                `;
                return;
            }
            
            const qIdx = state.currentQuestionIdx;
            const q = questions[qIdx];
            
            container.innerHTML = `
                <div class="socratic-card" id="quiz-card-${pIdx}" onclick="flipQuizCard(${pIdx})">
                    <div class="socratic-card-inner" id="quiz-card-inner-${pIdx}">
                        <div class="socratic-card-front">
                            <div>
                                <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--primary); font-weight: bold;">Control Socrático — Pregunta ${qIdx + 1} de ${questions.length}</span>
                                <p style="font-family: var(--font-editorial); font-size: 1.2rem; margin-top: 1rem; line-height: 1.5;">${q.q}</p>
                            </div>
                            <p style="font-size: 0.75rem; color: var(--text-muted); text-align: center;">Haz clic en la tarjeta para reflexionar e inspeccionar la respuesta patrón.</p>
                        </div>
                        <div class="socratic-card-back">
                            <div>
                                <span style="font-size: 0.75rem; text-transform: uppercase; color: var(--accent); font-weight: bold;">Respuesta Patrón</span>
                                <p style="font-family: var(--font-editorial); font-size: 1.1rem; margin-top: 1rem; line-height: 1.5;">${q.a}</p>
                            </div>
                            <div style="display: flex; gap: 0.75rem; margin-top: 1rem; pointer-events: auto;" onclick="event.stopPropagation();">
                                <button class="theme-toggle-btn" style="background: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.2); color: var(--accent); flex: 1; justify-content: center;" onclick="answerQuiz(${pIdx}, true)">Correcto</button>
                                <button class="theme-toggle-btn" style="background: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.2); color: #ef4444; flex: 1; justify-content: center;" onclick="answerQuiz(${pIdx}, false)">Incorrecto</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function flipQuizCard(pIdx) {
            const cardInner = document.getElementById(`quiz-card-inner-${pIdx}`);
            if (cardInner) {
                cardInner.classList.toggle('flipped');
            }
        }

        function answerQuiz(pIdx, isCorrect) {
            const key = `socratic-quiz-phase-${pIdx}`;
            const saved = localStorage.getItem(key);
            if (!saved) return;
            
            let state = JSON.parse(saved);
            const questions = QUIZ_QUESTIONS[pIdx] || [];
            
            if (isCorrect) {
                state.correctCount++;
                state.currentQuestionIdx++;
            } else {
                state.failed = true; 
            }
            
            if (!state.failed && state.currentQuestionIdx >= questions.length) {
                state.passed = true;
                localStorage.setItem(`phase-${pIdx}-completed`, "true");
            }
            
            localStorage.setItem(key, JSON.stringify(state));
            renderSocraticQuiz(pIdx);
            updateGlobalProgress();
            renderNavigation();
        }

        function resetQuiz(pIdx) {
            const key = `socratic-quiz-phase-${pIdx}`;
            const state = { currentQuestionIdx: 0, correctCount: 0, passed: false, failed: false };
            localStorage.setItem(key, JSON.stringify(state));
            localStorage.removeItem(`phase-${pIdx}-completed`);
            renderSocraticQuiz(pIdx);
            updateGlobalProgress();
            renderNavigation();
        }
        
        // ==== Plan Harada (Open Window 64) ====
        // Meta central editable + areas derivadas de las fases del curso (data-driven):
        // cada area = una fase de la ruta activa; cada practica = una obra que se
        // autoevalua en 4 niveles de dominio conversacional. Sin hardcodear fases.
        const HARADA_LEVELS = ['Sin empezar', 'Lo leí', 'Lo explico', 'Lo defiendo', 'Lo debato'];
        const HARADA_DEFAULT_GOAL = 'Poder sostener una conversación seria, con argumentos y fuentes, sobre cualquier tema del curso.';
        let haradaOpenArea = null;

        function getHaradaLevel(n) {
            const v = parseInt(localStorage.getItem('harada-lvl-stage-' + n) || '0', 10);
            return isNaN(v) ? 0 : Math.max(0, Math.min(4, v));
        }
        function setHaradaLevel(n, lvl) {
            try { localStorage.setItem('harada-lvl-stage-' + n, String(lvl)); } catch (e) {}
            renderHaradaPage();
        }
        function saveHaradaGoal(v) {
            try { localStorage.setItem('harada-goal', v); } catch (e) {}
        }
        function getHaradaAreas() {
            // Fases de la ruta activa, excluyendo el cierre: los ensayos finales son
            // la meta central, no un area. Una fase nueva aparece como area sola.
            const tk = getActiveTrackStages();
            const map = {};
            COURSE_DATA.forEach(s => {
                if (!tk.includes(s.stage)) return;
                if (/cierre/i.test(s.phase_name)) return;
                if (!map[s.phase_index]) map[s.phase_index] = { index: s.phase_index, name: s.phase_name, stages: [] };
                map[s.phase_index].stages.push(s);
            });
            return Object.values(map).sort((a, b) => a.index - b.index);
        }
        function haradaAreaScore(area) {
            if (!area.stages.length) return 0;
            const sum = area.stages.reduce((acc, s) => acc + getHaradaLevel(s.stage), 0);
            return Math.round((sum / (area.stages.length * 4)) * 100);
        }
        function haradaGlobalScore() {
            let n = 0, sum = 0;
            getHaradaAreas().forEach(a => a.stages.forEach(s => { n++; sum += getHaradaLevel(s.stage); }));
            return n ? Math.round((sum / (n * 4)) * 100) : 0;
        }
        function toggleHaradaArea(i) {
            haradaOpenArea = haradaOpenArea === i ? null : i;
            renderHaradaPage();
        }
        function goHarada() {
            selectedStageNum = null;
            localStorage.removeItem('selected-stage-num');
            if (location.hash !== '#/harada') { history.pushState(null, '', '#/harada'); }
            renderHaradaPage();
        }

        function renderHaradaPage() {
            rsvpPause();
            const panel = document.getElementById('workspace-panel');
            const areas = getHaradaAreas();
            const goal = localStorage.getItem('harada-goal') || HARADA_DEFAULT_GOAL;
            const score = haradaGlobalScore();

            const cellHtml = a => {
                const pct = haradaAreaScore(a);
                const shortName = a.name.replace(/^Fase \d+\s*[—-]+\s*/, '');
                return `<button class="hw-cell${haradaOpenArea === a.index ? ' open' : ''}" onclick="toggleHaradaArea(${a.index})">
                    <span class="nm">${shortName}</span>
                    <span class="mt">${a.stages.length} prácticas &middot; ${pct}%</span>
                    <span class="mini"><i style="width:${pct}%"></i></span>
                </button>`;
            };
            const centerCell = `<div class="hw-cell center"><span class="nm">${goal}</span><span class="mt">Índice de interlocutor: ${score}%</span></div>`;

            // Open Window: 3x3 con la meta al centro si hay exactamente 8 areas;
            // si el curso crece a mas o menos areas, la grilla se adapta sola.
            let gridHtml;
            if (areas.length === 8) {
                const c = areas.map(cellHtml);
                gridHtml = `<div class="hw-grid">${c[0]}${c[1]}${c[2]}${c[3]}${centerCell}${c[4]}${c[5]}${c[6]}${c[7]}</div>`;
            } else {
                gridHtml = `<div class="hw-grid flat">${centerCell}${areas.map(cellHtml).join('')}</div>`;
            }

            const openArea = areas.find(a => a.index === haradaOpenArea);
            let detailHtml = '';
            if (openArea) {
                const rows = openArea.stages.map(s => {
                    const lvl = getHaradaLevel(s.stage);
                    const btns = [1, 2, 3, 4].map(l =>
                        `<button class="hw-lvl${lvl >= l ? ' on' : ''}" title="${HARADA_LEVELS[l]}" onclick="setHaradaLevel(${s.stage}, ${lvl === l ? l - 1 : l})">${l}</button>`
                    ).join('');
                    return `<div class="hw-row">
                        <div class="hw-row-t"><a href="#/etapa-${s.stage}" style="color:inherit;">${s.stage}. ${s.title}</a></div>
                        <div class="hw-lvls">${btns}</div>
                        <div class="hw-row-lvl">${HARADA_LEVELS[lvl]}</div>
                    </div>`;
                }).join('');
                detailHtml = `<div class="hw-detail">
                    <h3>${openArea.name}</h3>
                    <div class="hint">Marcá tu nivel real, no el deseado. Tocá el nivel actual para bajarlo un paso.</div>
                    ${rows}
                </div>`;
            }

            panel.innerHTML = `
                <div class="workspace-welcome" style="height:auto; align-items:stretch; text-align:left; gap:0;">
                    <div class="hw-head">
                        <h2>Plan Harada: tu norte</h2>
                        <p class="hw-lead">El método Harada baja una meta ambiciosa a prácticas concretas y medibles. Acá la meta central es tuya (editala), las áreas son las fases del curso y cada práctica es una obra que evaluás en 4 niveles de dominio conversacional. El objetivo no es leer mucho: es poder conversar con solvencia.</p>
                    </div>
                    <div class="hw-goal">
                        <div class="k">Meta central (editable)</div>
                        <textarea rows="2" oninput="saveHaradaGoal(this.value)">${goal}</textarea>
                    </div>
                    <div class="hw-score">
                        <span class="pct">${score}%</span>
                        <div class="bar"><i style="width:${score}%"></i></div>
                        <span class="lbl">índice de interlocutor (ruta activa)</span>
                    </div>
                    ${gridHtml}
                    ${detailHtml || '<p class="hw-lead" style="font-size:0.82rem;">Tocá un área para autoevaluarte obra por obra.</p>'}
                </div>
            `;

            const right = document.getElementById('sidebar-right');
            right.innerHTML = `
                <div class="workspace-welcome" style="height:auto; text-align:left; align-items:stretch; gap:1rem;">
                    <div>
                        <h3>Los 4 niveles</h3>
                        <div class="hw-legend">
                            <div class="lg"><b>1 &middot; Lo leí</b><span>Conozco el texto, su contexto y su tesis.</span></div>
                            <div class="lg"><b>2 &middot; Lo explico</b><span>Puedo exponerlo con mis palabras a alguien que no lo leyó.</span></div>
                            <div class="lg"><b>3 &middot; Lo defiendo</b><span>Puedo argumentar a favor citando pasajes y fuentes.</span></div>
                            <div class="lg"><b>4 &middot; Lo debato</b><span>Puedo sostener la objeción más fuerte en contra y responderla.</span></div>
                        </div>
                    </div>
                    <div>
                        <h3>Rutina sugerida</h3>
                        <div class="hw-legend">
                            <div class="lg"><b>Diario</b><span>30-60 min de lectura + 1 nota permanente en tu Zettelkasten.</span></div>
                            <div class="lg"><b>Por etapa</b><span>Al cerrar el texto, leé el debate investigado y usá el prompt socrático.</span></div>
                            <div class="lg"><b>Semanal</b><span>Explicale un concepto a alguien (o grabate). Si no podés, volvés al nivel 1.</span></div>
                            <div class="lg"><b>Mensual</b><span>Revisá esta grilla y actualizá tus niveles a la baja sin piedad.</span></div>
                        </div>
                    </div>
                </div>
            `;

            renderNavigation();
        }

        function renderWelcomePage() {
            selectedStageNum = null;
            localStorage.removeItem('selected-stage-num');
            rsvpPause(); // detener RSVP si venia reproduciendo

            const panel = document.getElementById('workspace-panel');
            
            let trackStages = getActiveTrackStages();
            let totalStages = trackStages.length;
            
            let completedStages = 0;
            COURSE_DATA.forEach(s => {
                if (trackStages.includes(s.stage)) {
                    const { pct } = getStageStats(s);
                    if (pct === 1.0 && s.tasks.length > 0) completedStages++;
                }
            });
            
            const percent = totalStages > 0 ? Math.round((completedStages / totalStages) * 100) : 0;
            
            const TRACK_INFO = {
                simple: {
                    name: 'Ruta Simple', count: TRACK_SIMPLE.length, tagline: 'Fundamentos',
                    who: 'Para empezar de cero o repasar lo esencial.',
                    desc: 'Los textos imprescindibles. Recorre los debates y conceptos fundacionales del pensamiento político (Platón, Maquiavelo, Hobbes, Rousseau, Mill, Rawls) sin las ramificaciones más técnicas.'
                },
                intermediate: {
                    name: 'Ruta Intermedia', count: TRACK_INTERMEDIATE.length, tagline: 'Canon estándar',
                    who: 'Para quien ya tiene base y quiere profundizar.',
                    desc: 'El canon ampliado. Suma economía política (Smith, Marx, Keynes, Hayek), sociología y teoría política del siglo XX, y abre el pensamiento crítico e iberoamericano.'
                },
                advanced: {
                    name: 'Ruta Avanzada', count: TRACK_ADVANCED.length, tagline: 'Programa completo',
                    who: 'Para dominio exhaustivo, nivel máster.',
                    desc: 'El programa completo: tradición occidental e iberoamericana, teoría decolonial, feminista, poscolonial y pensamiento global (Gramsci, Foucault, Fanon, Quijano, Mbembe, y más).'
                }
            };
            const trackOrder = ['simple', 'intermediate', 'advanced'];
            const pathCards = trackOrder.map(t => {
                const info = TRACK_INFO[t];
                const isActive = activeTrack === t;
                return `
                    <div class="path-card${isActive ? ' path-card-active' : ''}">
                        <div class="path-card-tag">${info.tagline}</div>
                        <h4>${info.name}</h4>
                        <div class="path-card-count">${info.count} etapas</div>
                        <p class="path-card-desc">${info.desc}</p>
                        <p class="path-card-who">${info.who}</p>
                        <button class="path-card-btn${isActive ? ' path-card-btn-active' : ''}" onclick="selectTrackFromWelcome('${t}')">
                            ${isActive ? 'Ruta activa' : 'Elegir esta ruta'}
                        </button>
                    </div>
                `;
            }).join('');

            const activeInfo = TRACK_INFO[activeTrack] || TRACK_INFO.advanced;

            // Continuar donde quedaste (Dir 1 + Dir 6)
            const nextN = getNextStageNum();
            const nextStage = nextN !== null ? COURSE_DATA.find(d => d.stage === nextN) : null;
            const streak = getStreak();
            let studyDays = [];
            try { studyDays = JSON.parse(localStorage.getItem('study-days') || '[]'); } catch (e) {}
            const hasProgress = completedStages > 0 || studyDays.length > 0;
            const continueCard = nextStage ? `
                <div class="continue-card">
                    <div class="cc-k">${hasProgress ? 'Continua donde quedaste' : 'Empeza tu recorrido'}</div>
                    <div class="cc-title">Etapa ${nextStage.stage} &middot; ${nextStage.title}</div>
                    <div class="cc-sub">${nextStage.phase_name}${streak > 0 ? ` &middot; Racha: ${streak} dia${streak > 1 ? 's' : ''}` : ''}</div>
                    <button class="cc-btn" onclick="continueStudy()">${hasProgress ? 'Retomar' : 'Empezar'} &rarr;</button>
                </div>` : '';

            // Progreso por fase (ruta activa) y hitos por fase cerrada
            const tk = getActiveTrackStages();
            const phaseIdxs = [...new Set(COURSE_DATA.filter(s => tk.includes(s.stage)).map(s => s.phase_index))].sort((a, b) => a - b);
            let phaseProg = '', milestones = '';
            phaseIdxs.forEach(i => {
                const st = COURSE_DATA.filter(s => s.phase_index === i && tk.includes(s.stage));
                if (!st.length) return;
                const done = st.filter(s => isStageDone(s)).length;
                const pct = Math.round((done / st.length) * 100);
                phaseProg += `<div class="home-phase"><div class="hp-name">${st[0].phase_name}</div><div class="hp-bar"><i style="width:${pct}%"></i></div><div class="hp-c">${done}/${st.length}</div></div>`;
                if (done === st.length) milestones += `<div class="milestone-line">Cerraste: ${st[0].phase_name}</div>`;
            });
            if (!milestones) milestones = '<div class="milestone-empty">Cada fase que completes aparece aca como un hito.</div>';

            // Acceso al plan Harada con el indice de interlocutor actual.
            const hScore = haradaGlobalScore();
            const haradaCard = `
                <div class="harada-home-card" onclick="goHarada()">
                    <div>
                        <div class="k">Plan Harada</div>
                        <div class="t">Tu norte: de lector a interlocutor</div>
                        <div class="s">Meta central, ${getHaradaAreas().length} áreas (una por fase) y autoevaluación en 4 niveles por obra.</div>
                    </div>
                    <div class="pct">${hScore}%</div>
                </div>`;

            panel.innerHTML = `
                <div class="workspace-welcome" style="height: auto; align-items: stretch; text-align: left; gap: 1.5rem;">
                    <div class="welcome-hero">
                        <h2>Tu espacio de estudio</h2>
                        <p class="welcome-intro">
                            Retomá donde quedaste, o elegí una etapa en la barra lateral. Cada etapa tiene su propia
                            dirección, así que podés volver a ella o compartirla. Tu progreso se guarda en este navegador.
                            <a href="index.html" class="dashboard-link">Volver a la portada del curso</a>.
                        </p>
                    </div>

                    ${continueCard}

                    ${haradaCard}

                    <div class="welcome-progress-box">
                        <div>
                            <h4>Ruta activa: ${activeInfo.name}</h4>
                            <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 0.25rem;">${activeInfo.who}</p>
                        </div>
                        <div style="text-align: right;">
                            <p style="font-size: 1.25rem; font-weight: bold; color: var(--primary);">
                                ${completedStages} / ${totalStages} etapas
                            </p>
                            <div style="font-size: 0.85rem; color: var(--text-muted);">${percent}% de avance</div>
                        </div>
                    </div>

                    <div>
                        <h3>Progreso por fase</h3>
                        <div class="home-phases">${phaseProg}</div>
                    </div>

                    <div>
                        <h3>Hitos</h3>
                        <div class="milestones">${milestones}</div>
                    </div>

                    <div>
                        <h3>Cambiar de ruta</h3>
                        <p class="welcome-section-lead">Podés cambiar de ruta cuando quieras: tu progreso se conserva.</p>
                        <div class="path-card-grid">
                            ${pathCards}
                        </div>
                    </div>

                    <div>
                        <h3>Mapa mental del syllabus</h3>
                        <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.5rem;">Vínculos secuenciales entre las 103 etapas del curso. Las etapas completadas y las de tu ruta activa están resaltadas.</p>
                        <div id="syllabus-mindmap">
                            <svg id="mindmap-svg"></svg>
                        </div>
                    </div>
                </div>
            `;
            
            // Clear right panel on welcome page
            const right = document.getElementById('sidebar-right');
            right.innerHTML = `
                <div class="workspace-welcome" style="text-align:center; height:auto;">
                    <p>Selecciona una etapa de la barra lateral izquierda para comenzar a estudiar.</p>
                </div>
            `;
            
            // Draw mindmap
            initMindmap();
            resetZoom();
        }

        function getNodeCoords(stageNum) {
            const stage = COURSE_DATA.find(s => s.stage === stageNum);
            if (!stage) return { x: 0, y: 0 };
            
            const phaseIdx = stage.phase_index;
            const phaseStages = COURSE_DATA.filter(s => s.phase_index === phaseIdx);
            const idxInPhase = phaseStages.findIndex(s => s.stage === stageNum);
            
            // Grid spacing across coordinates
            const x = 80 + phaseIdx * 110 + (idxInPhase % 2 === 0 ? 12 : -12);
            
            const totalInPhase = phaseStages.length;
            const spacing = 320 / Math.max(1, totalInPhase);
            const y = 40 + idxInPhase * spacing + (idxInPhase % 2 === 0 ? 0 : 8);
            
            return { x, y };
        }

        function initMindmap() {
            const svg = document.getElementById('mindmap-svg');
            if (!svg) return;
            
            svg.innerHTML = '';
            
            const zoomGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            zoomGroup.setAttribute('id', 'mindmap-zoom-container');
            svg.appendChild(zoomGroup);
            
            const edgesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            edgesGroup.setAttribute('id', 'mindmap-edges');
            zoomGroup.appendChild(edgesGroup);
            
            const nodesGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            nodesGroup.setAttribute('id', 'mindmap-nodes');
            zoomGroup.appendChild(nodesGroup);
            
            // Render stages
            COURSE_DATA.forEach(s => {
                const coords = getNodeCoords(s.stage);
                
                const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
                g.setAttribute('class', `node`);
                g.setAttribute('data-stage', s.stage);
                g.onclick = () => selectStage(s.stage);
                
                // Halo protection circle
                const halo = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                halo.setAttribute('class', 'node-halo');
                halo.setAttribute('cx', coords.x);
                halo.setAttribute('cy', coords.y);
                halo.setAttribute('r', 16);
                halo.setAttribute('fill', 'var(--bg-workspace)');
                g.appendChild(halo);
                
                // Core circle
                const core = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
                core.setAttribute('class', 'node-core');
                core.setAttribute('cx', coords.x);
                core.setAttribute('cy', coords.y);
                core.setAttribute('r', 9);
                g.appendChild(core);
                
                // Label text
                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', coords.x);
                text.setAttribute('y', coords.y + 3);
                text.setAttribute('text-anchor', 'middle');
                text.setAttribute('style', 'font-size: 7px; font-weight: bold; fill: var(--text-main); pointer-events: none;');
                text.textContent = s.stage;
                g.appendChild(text);
                
                nodesGroup.appendChild(g);
            });
            
            // Draw sequential links
            for (let i = 0; i < COURSE_DATA.length - 1; i++) {
                const s1 = COURSE_DATA[i];
                const s2 = COURSE_DATA[i+1];
                const coords1 = getNodeCoords(s1.stage);
                const coords2 = getNodeCoords(s2.stage);
                
                const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
                line.setAttribute('x1', coords1.x);
                line.setAttribute('y1', coords1.y);
                line.setAttribute('x2', coords2.x);
                line.setAttribute('y2', coords2.y);
                line.setAttribute('class', 'edge');
                line.setAttribute('data-from', s1.stage);
                line.setAttribute('data-to', s2.stage);
                edgesGroup.appendChild(line);
            }
            
            updateMindmapStates();
        }

        function updateMindmapStates() {
            let trackStages = getActiveTrackStages();
            
            COURSE_DATA.forEach(s => {
                const isNodeActive = trackStages.includes(s.stage);
                const { pct } = getStageStats(s);
                const isNodeCompleted = pct === 1.0 && s.tasks.length > 0;
                
                const nodeEl = document.querySelector(`.node[data-stage="${s.stage}"]`);
                if (nodeEl) {
                    nodeEl.setAttribute('style', `opacity: ${isNodeActive ? 1.0 : 0.2}; cursor: pointer;`);
                    const core = nodeEl.querySelector('.node-core');
                    if (core) {
                        if (isNodeCompleted) {
                            core.setAttribute('fill', 'var(--accent)');
                            core.setAttribute('stroke', 'var(--text-main)');
                            core.setAttribute('stroke-width', '1.5');
                        } else if (isNodeActive) {
                            core.setAttribute('fill', 'var(--primary)');
                            core.setAttribute('stroke', 'var(--text-main)');
                            core.setAttribute('stroke-width', '1.5');
                        } else {
                            core.setAttribute('fill', '#4b5563');
                            core.setAttribute('stroke', 'transparent');
                        }
                    }
                }
            });
            
            const edges = document.querySelectorAll('.edge');
            edges.forEach(edge => {
                const from = parseInt(edge.getAttribute('data-from'));
                const to = parseInt(edge.getAttribute('data-to'));
                
                const isFromActive = trackStages.includes(from);
                const isToActive = trackStages.includes(to);
                const isEdgeActive = isFromActive && isToActive;
                
                if (isEdgeActive) {
                    edge.setAttribute('stroke', 'var(--primary)');
                    edge.setAttribute('stroke-width', '2');
                    edge.setAttribute('opacity', '0.7');
                } else {
                    edge.setAttribute('stroke', '#4b5563');
                    edge.setAttribute('stroke-width', '0.75');
                    edge.setAttribute('opacity', '0.15');
                }
            });
        }

        function zoomToNode(stageNum) {
            const coords = getNodeCoords(stageNum);
            const container = document.getElementById('mindmap-zoom-container');
            if (!container) return;
            
            const svgWidth = 1000;
            const svgHeight = 400;
            
            const scale = 2.2;
            const tx = svgWidth / 2 - coords.x * scale;
            const ty = svgHeight / 2 - coords.y * scale;
            
            container.style.transform = `translate(${tx}px, ${ty}px) scale(${scale})`;
            container.style.transformOrigin = '0px 0px';
            container.style.transition = 'transform 0.4s ease-in-out';
        }

        function resetZoom() {
            const container = document.getElementById('mindmap-zoom-container');
            if (!container) return;
            container.style.transform = 'translate(0px, 0px) scale(1)';
            container.style.transition = 'transform 0.4s ease-in-out';
        }
        
        function selectStage(stageNum) {
            selectedStageNum = stageNum;
            localStorage.setItem('selected-stage-num', stageNum);
            // Cada etapa tiene su propia URL. Si el cambio vino de un click (no del router),
            // empujamos la nueva dirección al historial del navegador.
            const _stageHash = '#/etapa-' + stageNum;
            if (location.hash !== _stageHash) { history.pushState(null, '', _stageHash); }
            localStorage.setItem('visited-stage-' + stageNum, '1');
            markStudyToday();
            rsvpPause(); // detener cualquier RSVP de una etapa previa
            // Sincronizar el estado de las tareas con el almacenamiento de la pista activa.
            loadCheckboxStates();

            const items = document.querySelectorAll('.stage-nav-item');
            items.forEach(it => it.classList.remove('active'));
            
            renderNavigation();
            
            // Expand the phase containing this stage in navigation
            const stage = COURSE_DATA.find(d => d.stage === stageNum);
            openPhases[stage.phase_index] = true;
            
            const panel = document.getElementById('workspace-panel');
            let quoteHtml = stage.quote ? `<div class="workspace-quote">"${stage.quote}"</div>` : '';
            
            // Dynamic generation of Growth Application section
            let growthHtml = stage.growth_html;

            // Dynamic generation of Debates section
            let debatesHtml = stage.debates_html;

            // Render ALL stage sections from the markdown, in document order.
            let sectionsHtml = (stage.sections || []).map(s => `
                <div class="workspace-section">
                    <h3>${s.title}</h3>
                    ${s.html}
                </div>
            `).join('');

            const _rt = localStorage.getItem('read-theme') || 'oscuro';
            const _focoOn = document.body.classList.contains('foco');
            const _trk = getActiveTrackStages();
            const _stIdx = _trk.indexOf(stageNum);
            const _hasNext = _stIdx >= 0 && _stIdx < _trk.length - 1;

            panel.innerHTML = `
                <div class="stage-hero">
                    <div class="stage-hero-meta">
                        <span class="hero-num-badge">Etapa ${stage.stage}</span>
                        <span class="hero-phase-badge">${stage.phase_name}</span>
                        <span class="hero-time-badge">
                            <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
                            ${stage.hours}
                        </span>
                        <span class="hero-type-badge">
                            <svg viewBox="0 0 24 24"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
                            ${stage.reading_type}
                        </span>
                    </div>
                    <h2>${stage.title}</h2>
                </div>

                <div class="reading-toolbar">
                    <div class="read-themes">
                        <span class="rt-label">Lectura</span>
                        <button class="rt-btn${_rt==='claro'?' on':''}" data-rt="claro" onclick="setReadTheme('claro')">Claro</button>
                        <button class="rt-btn${_rt==='sepia'?' on':''}" data-rt="sepia" onclick="setReadTheme('sepia')">Sepia</button>
                        <button class="rt-btn${_rt==='oscuro'?' on':''}" data-rt="oscuro" onclick="setReadTheme('oscuro')">Oscuro</button>
                    </div>
                    <button id="foco-btn" class="rt-btn foco-toggle" onclick="toggleFoco()">${_focoOn?'Salir de foco':'Modo foco'}</button>
                </div>

                <div class="reading-area">
                    ${quoteHtml}

                    ${sectionsHtml}

                    ${growthHtml}
                    ${debatesHtml}
                </div>

                <div class="stage-footer">
                    <button class="stage-foot-btn" onclick="goHome()">Volver al inicio</button>
                    ${_hasNext
                        ? `<button class="stage-foot-btn next-cta" onclick="goNextFromStage(${stageNum})">Siguiente etapa &rarr;</button>`
                        : `<button class="stage-foot-btn next-cta" onclick="goHome()">Terminaste tu ruta &middot; volver al inicio</button>`}
                </div>
            `;
            
            // Render right sidebar
            const right = document.getElementById('sidebar-right');
            
            let specsHtml = '';
            const hasSpecs = stage.english_title || stage.recommended_edition || stage.first_published;
            if (hasSpecs) {
                specsHtml = `
                    <div class="right-section">
                        <h3>Metadatos del Libro</h3>
                        <div class="book-details-card">
                            ${stage.english_title ? `<div class="book-detail-row"><strong>Título en inglés</strong><span>${stage.english_title}</span></div>` : ''}
                            ${stage.first_published ? `<div class="book-detail-row"><strong>Primera publicación</strong><span>${stage.first_published}</span></div>` : ''}
                            ${stage.recommended_edition ? `<div class="book-detail-row"><strong>Edición recomendada</strong><span>${stage.recommended_edition}</span></div>` : ''}
                        </div>
                    </div>
                `;
            }
            
            let checklistHtml = '';
            if (stage.tasks.length > 0) {
                checklistHtml = `
                    <div class="right-section">
                        <h3>Checklist de Tareas</h3>
                        <div class="checklist-wrapper">
                            ${stage.tasks.map((task, tIdx) => {
                                const completedClass = task.completed ? 'completed' : '';
                                const checked = task.completed ? 'checked' : '';
                                return `
                                    <div class="task-card ${completedClass}" id="task-card-${stage.stage}-${tIdx}" onclick="document.getElementById('check-${stage.stage}-${tIdx}').click();">
                                        <input type="checkbox" id="check-${stage.stage}-${tIdx}" ${checked} onchange="toggleTask(${stage.stage}, ${tIdx}, this); event.stopPropagation();">
                                        <span class="task-label">${task.label}</span>
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                `;
            }
            
            // Bloque de prompt socrático (copiable para usar con cualquier LLM)
            const chatWidgetHtml = renderSocraticPromptBlock(stage);
            
            right.innerHTML = `
                ${specsHtml}
                ${checklistHtml}
                
                ${stage.how_to_study_html ? `
                    <div class="right-section">
                        <h3>Guía de Estudio</h3>
                        <div style="font-size:0.85rem; color:var(--text-main);">${stage.how_to_study_html}</div>
                    </div>
                ` : ''}
                
                ${stage.resources_html ? `
                    <div class="right-section">
                        <h3>Recursos y Enlaces</h3>
                        <div style="font-size:0.85rem; color:var(--text-main);">${stage.resources_html}</div>
                    </div>
                ` : ''}

                ${chatWidgetHtml}
            `;
            
            // Handle viewport zoom on the SVG mindmap
            const mindmap = document.getElementById('mindmap-svg');
            if (mindmap) {
                zoomToNode(stageNum);
            }
            
            // Si la etapa trae el segmento RSVP, primear el visor con su texto.
            if (document.getElementById('rsvp-src')) { rsvpLoadFromUI(); }

            panel.scrollTop = 0;
            right.scrollTop = 0;
        }

        function escapeHtml(str) {
            return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
        }

        function renderSocraticPromptBlock(stage) {
            const prompt = stage.socratic || '';
            return `
                <div class="socratic-prompt-block" id="socratic-block-${stage.stage}">
                    <h3>Prompt Socrático para tu LLM</h3>
                    <p class="sp-desc">Copiá este prompt y pegalo en cualquier asistente de IA (Claude, ChatGPT, Gemini u otro). Está diseñado para hacerte pensar y llegar vos mismo a los conceptos, no para darte las respuestas.</p>
                    <pre class="socratic-prompt-text" id="socratic-prompt-${stage.stage}">${escapeHtml(prompt)}</pre>
                    <div class="sp-actions">
                        <button class="path-card-btn" onclick="copyStagePrompt(${stage.stage})">Copiar prompt</button>
                        <span class="sp-feedback" id="sp-feedback-${stage.stage}"></span>
                    </div>
                </div>
            `;
        }

        function copyStagePrompt(stageNum) {
            const el = document.getElementById('socratic-prompt-' + stageNum);
            const fb = document.getElementById('sp-feedback-' + stageNum);
            if (!el) return;
            const text = el.textContent;
            const done = function() { if (fb) { fb.textContent = 'Copiado'; setTimeout(function(){ fb.textContent = ''; }, 2000); } };
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(text).then(done).catch(function(){ fallbackCopy(text, done); });
            } else {
                fallbackCopy(text, done);
            }
        }

        function fallbackCopy(text, cb) {
            const ta = document.createElement('textarea');
            ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
            document.body.appendChild(ta); ta.select();
            try { document.execCommand('copy'); } catch (e) {}
            document.body.removeChild(ta);
            if (cb) cb();
        }

        // ---- Lector RSVP (segmento de lectura rapida, etapa 0) ----
        var _rsvpWords = [], _rsvpI = 0, _rsvpTimer = null, _rsvpPlaying = false, _rsvpWpm = 300, _rsvpSlow = 0;
        function rsvpGetORP(w){ var l=w.length; if(l<=1)return 0; if(l<=5)return 1; if(l<=9)return 2; if(l<=13)return 3; return 4; }
        function rsvpRender(w){ var b=document.getElementById('rsvp-before'),p=document.getElementById('rsvp-pivot'),a=document.getElementById('rsvp-after'); if(!p)return; w=w||''; var o=rsvpGetORP(w); b.textContent=w.slice(0,o); p.textContent=w.charAt(o); a.textContent=w.slice(o+1); }
        function rsvpProgress(){ var bar=document.getElementById('rsvp-bar'),c=document.getElementById('rsvp-counter'); var p=_rsvpWords.length?_rsvpI/_rsvpWords.length:0; if(bar)bar.style.width=(p*100)+'%'; if(c)c.textContent=_rsvpI+' / '+_rsvpWords.length; }
        function rsvpLoad(text){ _rsvpWords=(text||'').trim().split(/\s+/).filter(Boolean); _rsvpI=0; _rsvpSlow=5; rsvpRender(_rsvpWords[0]||''); rsvpProgress(); rsvpSyncBtn(); }
        function rsvpLoadFromUI(){ rsvpPause(); var ta=document.getElementById('rsvp-src'); rsvpLoad(ta?ta.value:''); }
        function rsvpDelay(w){ var t=60000/_rsvpWpm; var len=w.replace(/[^A-Za-z0-9áéíóúñÁÉÍÓÚÑ]/g,'').length; if(/[.!?:;]$/.test(w))t*=2.4; else if(/[,)\]"”—–]$/.test(w))t*=1.6; if(len<=5)t*=1.15; else if(len>=10)t*=1.4; if(_rsvpSlow>1){t*=_rsvpSlow;_rsvpSlow--;} return t; }
        function rsvpTick(){ if(!_rsvpPlaying||_rsvpI>=_rsvpWords.length){ _rsvpPlaying=false; rsvpSyncBtn(); return; } var w=_rsvpWords[_rsvpI]; rsvpRender(w); rsvpProgress(); var d=rsvpDelay(w); _rsvpI++; _rsvpTimer=setTimeout(rsvpTick,d); }
        function rsvpPlay(){ if(_rsvpPlaying)return; if(!_rsvpWords.length)rsvpLoadFromUI(); if(!_rsvpWords.length)return; if(_rsvpI>=_rsvpWords.length){_rsvpI=0;_rsvpSlow=5;} _rsvpPlaying=true; rsvpSyncBtn(); rsvpTick(); }
        function rsvpPause(){ _rsvpPlaying=false; if(_rsvpTimer)clearTimeout(_rsvpTimer); rsvpSyncBtn(); }
        function rsvpToggle(){ _rsvpPlaying?rsvpPause():rsvpPlay(); }
        function rsvpReset(){ rsvpPause(); _rsvpI=0; _rsvpSlow=5; rsvpRender(_rsvpWords[0]||''); rsvpProgress(); }
        function rsvpSetWpm(v){ _rsvpWpm=parseInt(v,10)||300; var l=document.getElementById('rsvp-wpm-label'); if(l)l.textContent=_rsvpWpm+' ppm'; }
        function rsvpSyncBtn(){ var b=document.getElementById('rsvp-play'); if(b)b.textContent=_rsvpPlaying?'Pausa':'Reproducir'; }

        // Backup and recovery functions
        function openBackupModal() {
            document.getElementById('backup-error').style.display = 'none';
            document.getElementById('backup-textarea').value = '';
            document.getElementById('backup-modal').style.display = 'flex';
        }

        function closeBackupModal() {
            document.getElementById('backup-modal').style.display = 'none';
        }

        function exportData() {
            const keys = {};
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key.includes('stage-') || key.startsWith('active-track') || key.startsWith('socratic-') || key.startsWith('phase-') || key.startsWith('harada-')) {
                    keys[key] = localStorage.getItem(key);
                }
            }
            document.getElementById('backup-textarea').value = JSON.stringify(keys, null, 2);
        }

        function importData() {
            const text = document.getElementById('backup-textarea').value.trim();
            if (!text) return;
            
            try {
                const parsed = JSON.parse(text);
                Object.keys(parsed).forEach(k => {
                    localStorage.setItem(k, parsed[k]);
                });
                
                document.getElementById('backup-error').style.display = 'none';
                closeBackupModal();
                
                // Reload states
                activeTrack = localStorage.getItem('active-track') || 'advanced';
                document.getElementById('track-selector').value = activeTrack;
                loadCheckboxStates();
                renderNavigation();
                updateGlobalProgress();
                
                if (selectedStageNum !== null) {
                    selectStage(selectedStageNum);
                } else {
                    renderWelcomePage();
                }
            } catch(e) {
                document.getElementById('backup-error').style.display = 'block';
            }
        }

        function resetData() {
            if (confirm("¿Estás seguro de que quieres restablecer todo tu progreso? Esta acción no se puede deshacer.")) {
                // Clear scoped items
                const keysToRemove = [];
                for (let i = 0; i < localStorage.length; i++) {
                    const key = localStorage.key(i);
                    if (key.includes('stage-') || key.startsWith('socratic-') || key.startsWith('phase-') || key.startsWith('harada-')) {
                        keysToRemove.push(key);
                    }
                }
                keysToRemove.forEach(k => localStorage.removeItem(k));
                
                closeBackupModal();
                loadCheckboxStates();
                renderNavigation();
                updateGlobalProgress();
                
                if (selectedStageNum !== null) {
                    selectStage(selectedStageNum);
                } else {
                    renderWelcomePage();
                }
            }
        }
        
        window.onload = init;
    