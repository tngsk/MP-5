
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace HTML
old_html = '''    <div class="matrix">
        <div class="row">
            <div class="row-label">PITCH</div>
            <div class="slots" id="slots-pitch"></div>
        </div>
        <div class="row">
            <div class="row-label">FILTER</div>
            <div class="slots" id="slots-filter"></div>
        </div>
        <div class="row">
            <div class="row-label">SPEED</div>
            <div class="slots" id="slots-speed"></div>
        </div>
    </div>'''

new_html = '''    <div class="mode-selector">
        <button id="btn-gyro" class="mode-btn active" onclick="setMode('gyro')">GYRO</button>
        <button id="btn-xypad" class="mode-btn" onclick="setMode('xypad')">XY PAD</button>
        <button id="btn-16pad" class="mode-btn" onclick="setMode('16pad')">16 PAD</button>
    </div>

    <div id="panel-gyro" class="mode-panel active">
        <div class="matrix">
            <div class="row">
                <div class="row-label">PITCH</div>
                <div class="slots" id="slots-pitch"></div>
            </div>
            <div class="row">
                <div class="row-label">FILTER</div>
                <div class="slots" id="slots-filter"></div>
            </div>
            <div class="row">
                <div class="row-label">SPEED</div>
                <div class="slots" id="slots-speed"></div>
            </div>
        </div>
    </div>

    <div id="panel-xypad" class="mode-panel" style="display:none;">
        <div class="xy-controls">
            <select id="xy-x-param">
                <option value="filter">X: FILTER</option>
                <option value="pitch">X: PITCH</option>
                <option value="speed">X: SPEED</option>
            </select>
            <select id="xy-y-param">
                <option value="pitch">Y: PITCH</option>
                <option value="filter">Y: FILTER</option>
                <option value="speed">Y: SPEED</option>
            </select>
        </div>
        <div class="xy-pad" id="xyPad">
            <div class="xy-cursor" id="xyCursor"></div>
        </div>
    </div>

    <div id="panel-16pad" class="mode-panel" style="display:none;">
        <div class="pad-grid" id="padGrid"></div>
    </div>'''

content = content.replace(old_html, new_html)

# 2. Add CSS
css_additions = '''
        /* MODE SELECTOR & PANELS */
        .mode-selector {
            display: flex; gap: 8px; margin-bottom: 8px; z-index: 10; flex-shrink: 0;
        }
        .mode-btn {
            flex: 1; padding: 8px 0; font-size: 0.65rem; font-weight: bold; letter-spacing: 0.1em;
            background: var(--surface); border: 1px solid var(--border); border-radius: 4px;
            cursor: pointer; box-shadow: 0 2px 0 var(--border); transition: all 0.05s;
        }
        .mode-btn.active {
            background: var(--text); color: var(--bg); border-color: var(--text); box-shadow: 0 2px 0 #000;
        }
        .mode-panel {
            display: none; flex: 2; flex-direction: column; margin-bottom: 12px; z-index: 10; min-height: 0;
        }
        .mode-panel.active { display: flex; }

        /* XY PAD */
        .xy-controls {
            display: flex; gap: 8px; margin-bottom: 8px;
        }
        .xy-controls select {
            flex: 1; padding: 6px; font-size: 0.65rem; font-family: inherit;
            background: var(--surface); border: 1px solid var(--border); border-radius: 4px;
        }
        .xy-pad {
            flex: 1; background: #222; border: 2px solid var(--border); border-radius: 6px;
            position: relative; touch-action: none; overflow: hidden;
            background-image:
                linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 20px 20px;
            background-position: center;
        }
        .xy-cursor {
            position: absolute; width: 16px; height: 16px; background: var(--accent-cyan);
            border-radius: 50%; transform: translate(-50%, -50%); pointer-events: none;
            box-shadow: 0 0 8px var(--accent-cyan);
            top: 50%; left: 50%;
        }
        .xy-cursor::before {
            content: ''; position: absolute; top: 8px; left: -1000px; right: -1000px; height: 1px; background: rgba(0, 163, 224, 0.5);
        }
        .xy-cursor::after {
            content: ''; position: absolute; left: 8px; top: -1000px; bottom: -1000px; width: 1px; background: rgba(0, 163, 224, 0.5);
        }

        /* 16 PAD */
        .pad-grid {
            flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(4, 1fr);
            gap: 6px;
        }
        .pad-btn {
            background: var(--surface); border: 1px solid var(--border); border-radius: 4px;
            box-shadow: 0 3px 0 var(--border); cursor: pointer; display: flex; align-items: center; justify-content: center;
            font-size: 0.8rem; font-weight: bold; transition: all 0.05s; touch-action: none;
        }
        .pad-btn:active, .pad-btn.active {
            transform: translateY(2px); box-shadow: 0 1px 0 var(--border);
            background: var(--accent-orange); color: #fff; border-color: var(--accent-orange);
        }
'''
content = content.replace('    </style>', css_additions + '    </style>')

# 3. Update Variables
old_vars = '''        const sensors = { NONE: 0.5, T_X: 0.5, T_Y: 0.5, A_X: 0.5, A_Y: 0.5, A_Z: 0.5 };
        const mapping = { pitch: "A_Y", filter: "T_X", speed: "NONE" };'''

new_vars = '''        const sensors = { NONE: 0.5, A_X: 0.5, A_Y: 0.5, A_Z: 0.5 };
        const mapping = { pitch: "A_Y", filter: "A_X", speed: "NONE" };
        let currentMode = 'gyro';
        let xyValues = { x: 0.5, y: 0.5 };
        let activePadPitch = null;'''

content = content.replace(old_vars, new_vars)

# 4. Update Icons
old_icons = '''        const icons = {
            NONE: '<svg viewBox="0 0 24 24" stroke-width="2.5"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>',
            T_X: '<svg viewBox="0 0 24 24" stroke-width="2.5"><line x1="4" y1="12" x2="20" y2="12"/><polyline points="16,8 20,12 16,16"/><polyline points="8,8 4,12 8,16"/></svg>',
            T_Y: '<svg viewBox="0 0 24 24" stroke-width="2.5"><line x1="12" y1="4" x2="12" y2="20"/><polyline points="8,16 12,20 16,16"/><polyline points="8,8 12,4 16,8"/></svg>',
            A_X: '<svg viewBox="0 0 24 24" stroke-width="2.5"><rect x="4" y="4" width="16" height="16" rx="2"/><line x1="9" y1="4" x2="9" y2="20"/></svg>',
            A_Y: '<svg viewBox="0 0 24 24" stroke-width="2.5"><rect x="4" y="4" width="16" height="16" rx="2"/><line x1="4" y1="9" x2="20" y2="9"/></svg>',
            A_Z: '<svg viewBox="0 0 24 24" stroke-width="2.5"><circle cx="12" cy="12" r="5"/></svg>'
        };'''

new_icons = '''        const icons = {
            NONE: '<svg viewBox="0 0 24 24" stroke-width="2.5"><line x1="6" y1="6" x2="18" y2="18"/><line x1="18" y1="6" x2="6" y2="18"/></svg>',
            A_X: '<svg viewBox="0 0 24 24" stroke-width="2.5"><rect x="4" y="4" width="16" height="16" rx="2"/><line x1="9" y1="4" x2="9" y2="20"/></svg>',
            A_Y: '<svg viewBox="0 0 24 24" stroke-width="2.5"><rect x="4" y="4" width="16" height="16" rx="2"/><line x1="4" y1="9" x2="20" y2="9"/></svg>',
            A_Z: '<svg viewBox="0 0 24 24" stroke-width="2.5"><circle cx="12" cy="12" r="5"/></svg>'
        };'''

content = content.replace(old_icons, new_icons)

# 5. Update draw() function
old_draw = '''            if (isRun) {
                const now = Tone.now();
                const pVal = sensors[mapping.pitch];
                const fVal = sensors[mapping.filter];
                const sVal = sensors[mapping.speed];

                if (mapping.pitch === "NONE") {
                    sourceNode.detune = 0;
                } else {
                    sourceNode.detune = (pVal - 0.5) * appSettings.pitchRange;
                }

                if (mapping.filter === "NONE") {
                    filterNode.frequency.value = 20000;
                } else {
                    filterNode.frequency.rampTo(100 + Math.pow(fVal, 2) * appSettings.filterMax, 0.1);
                }

                if (mapping.speed === "NONE") {
                    sourceNode.playbackRate = 1.0;
                } else {
                    const maxSpeedLog = Math.log10(appSettings.speedMax);
                    sourceNode.playbackRate = Math.pow(10, sVal * 2 * maxSpeedLog - maxSpeedLog);
                }

                gainNode.gain.rampTo(normalizationGain, 0.1);
            }'''

new_draw = '''            if (isRun) {
                const now = Tone.now();

                let pVal = 0.5, fVal = 0.5, sVal = 0.5;
                let activePitchMap = mapping.pitch;
                let activeFilterMap = mapping.filter;
                let activeSpeedMap = mapping.speed;

                if (currentMode === 'gyro') {
                    pVal = sensors[mapping.pitch];
                    fVal = sensors[mapping.filter];
                    sVal = sensors[mapping.speed];
                } else if (currentMode === 'xypad') {
                    const xp = document.getElementById('xy-x-param').value;
                    const yp = document.getElementById('xy-y-param').value;
                    if (xp === 'pitch') { pVal = xyValues.x; activePitchMap = 'XY'; } else if (yp === 'pitch') { pVal = 1.0 - xyValues.y; activePitchMap = 'XY'; }
                    if (xp === 'filter') { fVal = xyValues.x; activeFilterMap = 'XY'; } else if (yp === 'filter') { fVal = 1.0 - xyValues.y; activeFilterMap = 'XY'; }
                    if (xp === 'speed') { sVal = xyValues.x; activeSpeedMap = 'XY'; } else if (yp === 'speed') { sVal = 1.0 - xyValues.y; activeSpeedMap = 'XY'; }
                } else if (currentMode === '16pad') {
                    activePitchMap = '16PAD';
                    activeFilterMap = 'NONE';
                    activeSpeedMap = 'NONE';
                }

                if (currentMode === '16pad' && activePadPitch !== null) {
                    sourceNode.detune = activePadPitch;
                } else if (activePitchMap === "NONE") {
                    sourceNode.detune = 0;
                } else {
                    sourceNode.detune = (pVal - 0.5) * appSettings.pitchRange;
                }

                if (activeFilterMap === "NONE") {
                    filterNode.frequency.value = 20000;
                } else {
                    filterNode.frequency.rampTo(100 + Math.pow(fVal, 2) * appSettings.filterMax, 0.1);
                }

                if (activeSpeedMap === "NONE") {
                    sourceNode.playbackRate = 1.0;
                } else {
                    const maxSpeedLog = Math.log10(appSettings.speedMax);
                    sourceNode.playbackRate = Math.pow(10, sVal * 2 * maxSpeedLog - maxSpeedLog);
                }

                gainNode.gain.rampTo(normalizationGain, 0.1);
            }'''

content = content.replace(old_draw, new_draw)

# 6. Remove onpointermove for T_X, T_Y
old_pointermove = '''        window.onpointermove = (e) => {
            sensors.T_X = e.clientX / window.innerWidth;
            sensors.T_Y = e.clientY / window.innerHeight;
        };'''

content = content.replace(old_pointermove, '')

# 7. Add Mode Setup Scripts
js_additions = '''
        function setMode(mode) {
            currentMode = mode;
            ['gyro', 'xypad', '16pad'].forEach(m => {
                document.getElementById(`btn-${m}`).classList.toggle('active', m === mode);
                document.getElementById(`panel-${m}`).classList.toggle('active', m === mode);
            });
            if (mode === '16pad') activePadPitch = null; // reset on enter
        }

        // XY Pad logic
        const xyPad = document.getElementById('xyPad');
        const xyCursor = document.getElementById('xyCursor');
        let isXYDrag = false;

        function updateXY(e) {
            const rect = xyPad.getBoundingClientRect();
            let x = (e.clientX - rect.left) / rect.width;
            let y = (e.clientY - rect.top) / rect.height;
            x = Math.max(0, Math.min(1, x));
            y = Math.max(0, Math.min(1, y));
            xyValues.x = x;
            xyValues.y = y;
            xyCursor.style.left = `${x * 100}%`;
            xyCursor.style.top = `${y * 100}%`;
        }

        xyPad.addEventListener('pointerdown', e => { isXYDrag = true; updateXY(e); xyPad.setPointerCapture(e.pointerId); });
        xyPad.addEventListener('pointermove', e => { if (isXYDrag) updateXY(e); });
        xyPad.addEventListener('pointerup', e => { isXYDrag = false; xyPad.releasePointerCapture(e.pointerId); });
        xyPad.addEventListener('pointercancel', e => { isXYDrag = false; });

        // 16 Pad logic
        const padGrid = document.getElementById('padGrid');
        const padLabels = ['C','D','E','F', '8','9','A','B', '4','5','6','7', '0','1','2','3'];
        // Let's make 0 at bottom left, F at top right.
        // We assign pitch detune in cents.
        const baseDetune = -800; // start
        const stepDetune = 100; // semitone per pad

        for (let i = 0; i < 16; i++) {
            const btn = document.createElement('button');
            btn.className = 'pad-btn';
            btn.innerText = padLabels[i];

            // Map index from layout logic:
            // The visual grid is:
            // C D E F (idx 0-3, pitch 12-15)
            // 8 9 A B (idx 4-7, pitch 8-11)
            // 4 5 6 7 (idx 8-11, pitch 4-7)
            // 0 1 2 3 (idx 12-15, pitch 0-3)

            let row = Math.floor(i / 4);
            let col = i % 4;
            let pitchIndex = (3 - row) * 4 + col; // 0 for bottom-left, 15 for top-right
            let pitchValue = pitchIndex * stepDetune; // 0 to 1500 cents relative

            // Event listeners
            btn.addEventListener('pointerdown', (e) => {
                e.preventDefault();
                btn.setPointerCapture(e.pointerId);
                btn.classList.add('active');
                activePadPitch = pitchValue;
            });
            const releasePad = () => {
                btn.classList.remove('active');
            };
            btn.addEventListener('pointerup', releasePad);
            btn.addEventListener('pointercancel', releasePad);
            btn.addEventListener('pointerout', releasePad);

            padGrid.appendChild(btn);
        }
'''

content = content.replace('    </script>', js_additions + '    </script>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
