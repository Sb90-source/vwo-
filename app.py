import streamlit as st
import sqlite3
import hashlib
import time
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("💀 CYBER BREACH SIMULATOR", layout="wide", initial_sidebar_state="collapsed")

# ==========================================================
# VIBE — MATRIX RAIN + SCANLINES + SOUNDS + FONTS
# ==========================================================
# Inject CSS via JS into parent document — prevents Streamlit from leaking style tags as text
components.html("""
<script>
(function() {
    const css = `
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap');
        html, body, [class*="css"] {
            background-color: #020409 !important;
            color: #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        h1,h2,h3,h4 {
            font-family: 'Orbitron', monospace !important;
            color: #00ff9c !important;
            text-shadow: 0 0 15px rgba(0,255,156,0.5);
            letter-spacing: 3px;
        }
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            background-color: #000 !important;
            color: #00ff9c !important;
            border: 1px solid #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
            font-size: 14px !important;
            caret-color: #00ff9c;
        }
        .stButton > button {
            background-color: #000 !important;
            color: #00ff9c !important;
            border: 1px solid #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
            letter-spacing: 2px;
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background-color: #00ff9c !important;
            color: #000 !important;
            box-shadow: 0 0 20px rgba(0,255,156,0.6);
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Share Tech Mono', monospace !important;
            color: #00ff9c !important;
            background: #000 !important;
            border: 1px solid #00ff9c !important;
            margin-right: 4px;
            letter-spacing: 2px;
        }
        .stTabs [aria-selected="true"] {
            background: #00ff9c !important;
            color: #000 !important;
        }
        .stAlert {
            background: #000 !important;
            border: 1px solid #00ff9c !important;
            color: #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
        code, pre {
            background-color: #050e08 !important;
            color: #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
            border: 1px solid rgba(0,255,156,0.2) !important;
        }
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding-top: 1rem !important; }
        body::after {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px);
            pointer-events: none;
            z-index: 9999;
        }
        @keyframes flicker {
            0%,89%,91%,93%,100% { opacity:1; }
            90% { opacity:0.3; }
            92% { opacity:0.6; }
            94% { opacity:0.1; }
            95% { opacity:0.8; }
            96% { opacity:0.2; }
            97% { opacity:1; }
        }
        body { animation: flicker 2s infinite; }
        .stProgress > div > div {
            background: linear-gradient(90deg, #00ff9c, #00ffcc) !important;
        }
    `;
    const style = window.parent.document.createElement('style');
    style.textContent = css;
    window.parent.document.head.appendChild(style);
})();
</script>
""", height=0)

# Matrix rain + keyboard sounds
components.html("""
<canvas id="matrix" style="position:fixed;top:0;left:0;width:100%;height:100%;opacity:0.06;pointer-events:none;z-index:0;"></canvas>
<script>
// MATRIX RAIN
const c = document.getElementById('matrix');
const ctx = c.getContext('2d');
c.width = window.innerWidth;
c.height = window.innerHeight;
const cols = Math.floor(c.width / 16);
const drops = Array(cols).fill(1);
const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()アイウエオカキクケコ';
function drawMatrix() {
    ctx.fillStyle = 'rgba(2,4,9,0.05)';
    ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle = '#00ff9c';
    ctx.font = '14px Share Tech Mono';
    drops.forEach((y,i) => {
        const ch = chars[Math.floor(Math.random()*chars.length)];
        ctx.fillText(ch, i*16, y*16);
        if(y*16 > c.height && Math.random() > 0.975) drops[i] = 0;
        drops[i]++;
    });
}
setInterval(drawMatrix, 40);

// KEYBOARD CLICK SOUND
const AudioCtx = window.AudioContext || window.webkitAudioContext;
function playClick() {
    try {
        const ac = new AudioCtx();
        const osc = ac.createOscillator();
        const gain = ac.createGain();
        osc.connect(gain); gain.connect(ac.destination);
        osc.type = 'square';
        osc.frequency.setValueAtTime(800, ac.currentTime);
        osc.frequency.exponentialRampToValueAtTime(200, ac.currentTime + 0.03);
        gain.gain.setValueAtTime(0.05, ac.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.04);
        osc.start(); osc.stop(ac.currentTime + 0.04);
    } catch(e) {}
}
function playSuccess() {
    try {
        const ac = new AudioCtx();
        [440,554,660,880].forEach((f,i) => {
            const osc = ac.createOscillator();
            const gain = ac.createGain();
            osc.connect(gain); gain.connect(ac.destination);
            osc.frequency.value = f;
            gain.gain.setValueAtTime(0.08, ac.currentTime + i*0.1);
            gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + i*0.1 + 0.15);
            osc.start(ac.currentTime + i*0.1);
            osc.stop(ac.currentTime + i*0.1 + 0.2);
        });
    } catch(e) {}
}
document.addEventListener('keydown', playClick);
window.playSuccess = playSuccess;
</script>
""", height=0)

# ==========================================================
# DATABASE
# ==========================================================
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY, password TEXT, role TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        username TEXT, room TEXT, level INTEGER,
        PRIMARY KEY(username, room))""")

    c.execute("""CREATE TABLE IF NOT EXISTS flags (
        username TEXT, room TEXT, flag TEXT, time TEXT)""")

    c.execute("""CREATE TABLE IF NOT EXISTS hints (
        username TEXT, room TEXT, hint_num INTEGER,
        PRIMARY KEY(username, room, hint_num))""")

    for u in [("student", hash_pw("hackme"), "student"),
              ("teacher", hash_pw("admin123"), "teacher")]:
        c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", u)

    conn.commit()
    conn.close()

init_db()

# ==========================================================
# HINTS DATA
# ==========================================================
HINTS = {
    "sql": [
        "💡 Welk type aanval misbruikt database queries door code in een invoerveld te stoppen?",
        "💡 Maak de WHERE-clausule altijd TRUE. Probeer: ' OR '1'='1 als gebruikersnaam.",
        "💡 Gebruik UNION SELECT om een tweede query mee te combineren. Bijv: ' UNION SELECT username, password, role FROM users--",
    ],
    "xss": [
        "💡 Welk type aanval injecteert kwaadaardige scripts in een webpagina die andere gebruikers zien?",
        "💡 Gebruik de HTML tag die JavaScript uitvoert. Typ letterlijk: <script>alert('xss')</script>",
        "💡 Zelfde als stap 2 maar nu wordt je script opgeslagen in de database. Gebruik weer een <script> tag.",
    ],
    "privesc": [
        "💡 Wat doe je als je meer rechten wil dan je hebt?",
        "💡 Wat is de hoogste gebruikersrol in een systeem?",
        "💡 Typ simpelweg de rol waar je toegang toe wil hebben.",
    ],
    "crypto": [
        "💡 Julius Caesar gebruikte dit systeem om berichten te versleutelen.",
        "💡 Elke letter wordt X posities verschoven in het alfabet.",
        "💡 Probeer ROT13 of verschuif letters met 3 posities terug.",
    ],
}

# ==========================================================
# HELPERS
# ==========================================================
def auth(u, p):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (u, hash_pw(p)))
    r = c.fetchone()
    conn.close()
    return r[0] if r else None

def get_level(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT level FROM progress WHERE username=? AND room=?", (user, room))
    r = c.fetchone()
    conn.close()
    return r[0] if r else 1

def set_level(user, room, level):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("""INSERT INTO progress VALUES (?,?,?)
        ON CONFLICT(username,room) DO UPDATE SET level=?""",
        (user, room, level, level))
    conn.commit()
    conn.close()

def give_flag(user, room, flag):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM flags WHERE username=? AND room=?", (user, room))
    if not c.fetchone():
        c.execute("INSERT INTO flags VALUES (?,?,?,?)",
                  (user, room, flag, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def has_completed(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM flags WHERE username=? AND room=?", (user, room))
    r = c.fetchone()
    conn.close()
    return r is not None

def get_hints_used(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT hint_num FROM hints WHERE username=? AND room=? ORDER BY hint_num",
              (user, room))
    r = [x[0] for x in c.fetchall()]
    conn.close()
    return r

def use_hint(user, room, hint_num):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO hints VALUES (?,?,?)", (user, room, hint_num))
    conn.commit()
    conn.close()

def typewriter_terminal(lines):
    """Show terminal output with fake typewriter feel using st.code"""
    for line in lines:
        st.code(line, language=None)
        time.sleep(0.08)

def fake_progress(label="BYPASSING FIREWALL"):
    """Show animated fake progress bar"""
    bar = st.progress(0, text=f"⚡ {label}...")
    for i in range(0, 101, 5):
        bar.progress(i, text=f"⚡ {label}... {i}%")
        time.sleep(0.03)
    bar.empty()

def hint_widget(user, room, current_level):
    """Render hint system for a room"""
    hints = HINTS.get(room, [])
    used = get_hints_used(user, room)
    next_hint = len(used)

    with st.expander(f"🔍 HINTS ({next_hint}/{len(hints)} gebruikt)"):
        # Show already used hints
        for i in used:
            st.info(hints[i])

        # Button for next hint
        if next_hint < len(hints):
            if st.button(f"📡 REQUEST HINT {next_hint + 1}", key=f"hint_{room}_{next_hint}"):
                use_hint(user, room, next_hint)
                st.rerun()
        else:
            st.caption("Alle hints gebruikt.")

# ==========================================================
# SESSION
# ==========================================================
for k, v in [("user", None), ("role", None)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================================
# LOGIN
# ==========================================================
if not st.session_state.user:
    st.markdown("""
    <div style="text-align:center; padding: 2rem 0 1rem;">
        <div class="glitch-wrapper2">
            <span class="glitch-t" data-text="CYBER BREACH SIMULATOR">CYBER BREACH SIMULATOR</span>
        </div>
        <p style="letter-spacing:6px;color:rgba(0,255,156,0.5);font-size:11px;margin-top:12px;font-family:'Share Tech Mono',monospace;">
            SIMULATOR v2.0 &mdash; AUTHORIZED TRAINING ONLY
        </p>
    </div>
    <style>
    @keyframes gt {
        0%,90%,100% { text-shadow:0 0 15px rgba(0,255,156,0.6); transform:translate(0); clip-path:none; }
        91% { text-shadow:-4px 0 #ff003c,4px 0 #00ffff; transform:translate(-3px,0); clip-path:inset(5% 0 55% 0); }
        92% { text-shadow:4px 0 #ff003c,-4px 0 #00ffff; transform:translate(3px,0); clip-path:inset(58% 0 3% 0); }
        93% { text-shadow:-2px 0 #ff003c,2px 0 #00ffff; transform:translate(-1px,0); clip-path:none; }
        94% { text-shadow:0 0 15px rgba(0,255,156,0.6); transform:translate(0); }
    }
    @keyframes gt2 {
        0%,90%,100% { opacity:0; }
        91% { opacity:0.7; transform:translate(6px,-3px); filter:hue-rotate(120deg); }
        93% { opacity:0; }
    }
    .glitch-t {
        font-family:'Orbitron',monospace !important;
        font-weight:900;
        font-size:clamp(22px,3.5vw,52px);
        color:#00ff9c;
        letter-spacing:6px;
        animation:gt 5s infinite;
        position:relative;
        display:inline-block;
    }
    .glitch-t::before {
        content:attr(data-text);
        position:absolute; left:0; top:0;
        color:#ff003c;
        animation:gt2 5s infinite;
        pointer-events:none;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**`> IDENTIFICEER JEZELF`**")
        u = st.text_input("USERNAME", placeholder="operative_id")
        p = st.text_input("PASSWORD", type="password", placeholder="••••••••")
        if st.button("▶ TOEGANG AANVRAGEN", use_container_width=True):
            role = auth(u, p)
            if role:
                fake_progress("IDENTITEIT VERIFIËREN")
                st.session_state.user = u
                st.session_state.role = role
                st.rerun()
            else:
                st.error("⛔ TOEGANG GEWEIGERD — Ongeldige credentials")
    st.stop()

# ==========================================================
# TEACHER VIEW
# ==========================================================
if st.session_state.role == "teacher":
    st.title("🧑‍🏫 CONTROL PANEL")

    conn = sqlite3.connect("platform.db")

    st.subheader("VOORTGANG PER STUDENT")
    progress_data = conn.execute("""
        SELECT p.username, p.room, p.level,
               (SELECT COUNT(*) FROM hints h WHERE h.username=p.username AND h.room=p.room) as hints_used
        FROM progress p ORDER BY p.username, p.room
    """).fetchall()

    if progress_data:
        st.table({
            "Student": [r[0] for r in progress_data],
            "Room": [r[1].upper() for r in progress_data],
            "Level": [r[2] for r in progress_data],
            "Hints gebruikt": [r[3] for r in progress_data],
        })
    else:
        st.info("Nog geen voortgang geregistreerd.")

    st.subheader("BEHAALDE FLAGS")
    flags = conn.execute("SELECT * FROM flags ORDER BY time DESC").fetchall()
    if flags:
        st.table({
            "Student": [r[0] for r in flags],
            "Room": [r[1].upper() for r in flags],
            "Flag": [r[2] for r in flags],
            "Tijd": [r[3][:19] for r in flags],
        })
    else:
        st.info("Nog geen flags behaald.")

    conn.close()

    st.subheader("RESET STUDENT")
    all_students = [r[0] for r in sqlite3.connect("platform.db").execute(
        "SELECT DISTINCT username FROM users WHERE role='student'"
    ).fetchall()]
    reset_target = st.selectbox("Selecteer student", all_students, key="reset_target")
    if st.button("🗑 RESET GESELECTEERDE STUDENT", key="teacher_reset"):
        conn2 = sqlite3.connect("platform.db")
        c2 = conn2.cursor()
        c2.execute("DELETE FROM progress WHERE username=?", (reset_target,))
        c2.execute("DELETE FROM flags WHERE username=?", (reset_target,))
        c2.execute("DELETE FROM hints WHERE username=?", (reset_target,))
        conn2.commit()
        conn2.close()
        st.success(f"✅ Progressie van {reset_target} gereset!")
        st.rerun()

    st.markdown("---")
    if st.button("🔓 LOGOUT"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# ==========================================================
# STUDENT VIEW
# ==========================================================
user = st.session_state.user

# Header met voortgang
rooms_done = sum(1 for r in ["sql","xss","privesc","crypto"] if has_completed(user, r))
col_title, col_status = st.columns([3,1])
with col_title:
    st.title(f"🕶 OPERATIVE: {user.upper()}")
with col_status:
    st.metric("MISSIES VOLTOOID", f"{rooms_done}/4")

st.markdown("---")

tabs = st.tabs(["💉 SQL", "🌐 XSS", "⬆ PRIVESC", "🔐 VAULT"])

# ==========================================================
# ROOM 1 — SQL INJECTION
# ==========================================================
with tabs[0]:
    st.header("FRONT DESK TERMINAL")
    st.markdown("*Infiltreer het authenticatiesysteem van het doelwit.*")
    lvl = get_level(user, "sql")

    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        st.markdown("""
```
[SYSTEEM LOG]
Verbinding gemaakt met auth.target.local:3306
Onbekende kwetsbaarheid gedetecteerd in login module...
Analyseer het systeem.
```
        """)
        st.markdown("**Wat voor type aanval is hier van toepassing?**")
        cmd = st.text_input("root@auth:~#", key="sql1", placeholder="typ je antwoord...")
        if st.button("▶ EXECUTE", key="sql1_btn"):
            if cmd.lower().strip() == "sql injection":
                fake_progress("KWETSBAARHEID ANALYSEREN")
                set_level(user, "sql", 2)
                typewriter_terminal([
                    "[+] Kwetsbaarheid geïdentificeerd: SQL INJECTION",
                    "[+] Login module accepteert ongefilterde input",
                    "[!] Proceeding to exploitation phase..."
                ])
                st.rerun()
            else:
                st.error("❌ Incorrect. Vraag een hint als je vastloopt.")
        hint_widget(user, "sql", lvl)

    elif lvl == 2:
        # LAPTOP UI
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            components.html("""
            <style>
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body { background: transparent; font-family: 'Segoe UI', Arial, sans-serif; }

            .laptop-wrap { display:flex; flex-direction:column; align-items:center; }

            /* SCREEN */
            .screen-outer {
                background: #1a1a2e;
                border: 3px solid #333;
                border-bottom: 6px solid #222;
                border-radius: 12px 12px 0 0;
                width: 100%;
                padding: 12px;
                box-shadow: 0 0 30px rgba(0,0,0,0.8), inset 0 0 10px rgba(0,0,0,0.5);
                position: relative;
            }
            .screen-outer::before {
                content: '';
                position: absolute;
                top: 6px; left: 50%; transform: translateX(-50%);
                width: 8px; height: 8px;
                background: #333;
                border-radius: 50%;
            }
            .screen-inner {
                background: #f0f2f5;
                border-radius: 4px;
                overflow: hidden;
                min-height: 320px;
            }

            /* BROWSER CHROME */
            .browser-bar {
                background: #e8e8e8;
                padding: 8px 12px;
                display: flex;
                align-items: center;
                gap: 8px;
                border-bottom: 1px solid #ccc;
            }
            .dot { width:10px; height:10px; border-radius:50%; }
            .dot.r { background:#ff5f57; }
            .dot.y { background:#febc2e; }
            .dot.g { background:#28c840; }
            .url-bar {
                flex: 1;
                background: white;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 3px 10px;
                font-size: 11px;
                color: #666;
                display: flex;
                align-items: center;
                gap: 4px;
            }
            .lock { color: #28c840; font-size: 10px; }

            /* LOGIN PAGE */
            .login-page {
                padding: 30px 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .company-logo {
                font-size: 22px;
                font-weight: 700;
                color: #1a1a2e;
                margin-bottom: 4px;
                letter-spacing: -1px;
            }
            .company-logo span { color: #e74c3c; }
            .tagline { font-size: 11px; color: #999; margin-bottom: 24px; }
            .login-card {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 28px 32px;
                width: 100%;
                box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            }
            .login-card h3 { font-size: 16px; color: #333; margin-bottom: 20px; font-weight: 600; }
            .field { margin-bottom: 14px; }
            .field label { display:block; font-size:11px; color:#666; margin-bottom:4px; font-weight:500; }
            .field input {
                width: 100%;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
                color: #333;
                background: #fafafa;
                outline: none;
            }
            .field input:focus { border-color: #4a90e2; background: white; }
            .login-btn {
                width: 100%;
                background: #4a90e2;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                margin-top: 6px;
            }
            .login-btn:hover { background: #357abd; }
            .footer-links { display:flex; justify-content:space-between; margin-top:12px; }
            .footer-links a { font-size:11px; color:#4a90e2; text-decoration:none; }

            /* INJECTED state */
            .injected input[name="username"] {
                color: #e74c3c !important;
                border-color: #e74c3c !important;
                background: #fff5f5 !important;
            }

            /* HINGE */
            .hinge {
                width: 100%;
                height: 8px;
                background: linear-gradient(180deg, #1a1a1a, #2d2d2d);
                border-radius: 0;
                position: relative;
            }
            .hinge::after {
                content:'';
                position:absolute;
                left:50%; top:50%;
                transform:translate(-50%,-50%);
                width:40px; height:4px;
                background:#111;
                border-radius:2px;
            }

            /* BASE */
            .base {
                background: linear-gradient(180deg, #2d2d2d, #222);
                width: 108%;
                height: 18px;
                border-radius: 0 0 12px 12px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.5);
                position: relative;
            }
            .base::after {
                content:'';
                position:absolute;
                bottom:4px; left:50%;
                transform:translateX(-50%);
                width:50px; height:3px;
                background:#1a1a1a;
                border-radius:2px;
            }

            .warning {
                background: #fff3cd;
                border: 1px solid #ffc107;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 11px;
                color: #856404;
                margin-bottom: 14px;
                display: none;
            }
            </style>

            <div class="laptop-wrap">
                <div class="screen-outer">
                    <div class="screen-inner">
                        <div class="browser-bar">
                            <div class="dot r"></div>
                            <div class="dot y"></div>
                            <div class="dot g"></div>
                            <div class="url-bar">
                                <span class="lock">🔒</span>
                                auth.target.local/login
                            </div>
                        </div>
                        <div class="login-page">
                            <div class="company-logo">Corp<span>Sec</span></div>
                            <div class="tagline">Enterprise Security Portal</div>
                            <div class="login-card" id="loginCard">
                                <h3>Inloggen</h3>
                                <div class="warning" id="warning">⚠️ Ongeldige inloggegevens</div>
                                <div class="field">
                                    <label>Gebruikersnaam</label>
                                    <input type="text" name="username" id="uname" placeholder="gebruiker@corp.nl">
                                </div>
                                <div class="field">
                                    <label>Wachtwoord</label>
                                    <input type="password" name="password" placeholder="••••••••">
                                </div>
                                <button class="login-btn" onclick="tryLogin()">Inloggen</button>
                                <div class="footer-links">
                                    <a href="#">Wachtwoord vergeten?</a>
                                    <a href="#">Hulp nodig?</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="hinge"></div>
                <div class="base"></div>
            </div>

            <script>
            function tryLogin() {
                const u = document.getElementById('uname').value;
                const w = document.getElementById('warning');
                if (u.includes("' or") || u.includes("' OR") || u.includes("'or") || u.toLowerCase().includes("1=1")) {
                    document.getElementById('loginCard').style.background = '#fff5f5';
                    document.getElementById('loginCard').style.borderColor = '#e74c3c';
                    w.style.display = 'block';
                    w.style.background = '#d4edda';
                    w.style.borderColor = '#28a745';
                    w.style.color = '#155724';
                    w.innerHTML = '✅ SQL INJECTION GEDETECTEERD — query altijd TRUE';
                } else {
                    w.style.display = 'block';
                    w.innerHTML = '⚠️ Ongeldige inloggegevens';
                    w.style.background = '#fff3cd';
                    w.style.borderColor = '#ffc107';
                    w.style.color = '#856404';
                }
            }
            </script>
            """, height=500)

        st.markdown("**Voer je SQL injectie payload in als gebruikersnaam:**")
        cmd = st.text_input("root@auth:~# username>", key="sql2", placeholder="voer payload in...")
        if st.button("▶ INJECT", key="sql2_btn"):
            if "' or '1'='1" in cmd.lower() or "' or 1=1" in cmd.lower():
                fake_progress("AUTHENTICATIE BYPASSEN")
                set_level(user, "sql", 3)
                typewriter_terminal([
                    "[+] SQL query gemanipuleerd",
                    "[+] WHERE clause: TRUE voor alle rijen",
                    "[+] Ingelogd als eerste gebruiker in database",
                    "[✓] AUTHENTICATIE BYPASSED"
                ])
                st.rerun()
            else:
                st.error("❌ Payload werkt niet. Probeer de login altijd TRUE te maken.")
        hint_widget(user, "sql", lvl)

    elif lvl == 3:
        col_l, col_m, col_r = st.columns([1, 2, 1])
        with col_m:
            components.html("""
            <style>
            * { box-sizing:border-box; margin:0; padding:0; }
            body { background:transparent; font-family:'Segoe UI',Arial,sans-serif; }
            .laptop-wrap { display:flex; flex-direction:column; align-items:center; }
            .screen-outer {
                background:#1a1a2e; border:3px solid #333; border-bottom:6px solid #222;
                border-radius:12px 12px 0 0; width:100%; padding:12px;
                box-shadow:0 0 30px rgba(0,0,0,0.8),inset 0 0 10px rgba(0,0,0,0.5); position:relative;
            }
            .screen-outer::before {
                content:''; position:absolute; top:6px; left:50%; transform:translateX(-50%);
                width:8px; height:8px; background:#333; border-radius:50%;
            }
            .screen-inner { background:#f5f6fa; border-radius:4px; overflow:hidden; min-height:420px; }
            .browser-bar {
                background:#e8e8e8; padding:8px 12px; display:flex; align-items:center;
                gap:8px; border-bottom:1px solid #ccc;
            }
            .dot { width:10px; height:10px; border-radius:50%; }
            .dot.r { background:#ff5f57; } .dot.y { background:#febc2e; } .dot.g { background:#28c840; }
            .url-bar {
                flex:1; background:white; border:1px solid #ccc; border-radius:4px;
                padding:3px 10px; font-size:11px; color:#666; display:flex; align-items:center; gap:4px;
            }

            /* TOP NAV */
            .topnav {
                background:#1a73e8; color:white; padding:10px 20px;
                display:flex; align-items:center; justify-content:space-between;
            }
            .topnav .logo { font-size:16px; font-weight:700; letter-spacing:-0.5px; }
            .topnav .logo span { color:#ffd700; }
            .topnav .user-info { display:flex; align-items:center; gap:8px; font-size:12px; }
            .avatar {
                width:28px; height:28px; border-radius:50%; background:#ffd700;
                color:#1a1a2e; display:flex; align-items:center; justify-content:center;
                font-weight:700; font-size:12px;
            }

            /* SIDEBAR + CONTENT */
            .dashboard { display:flex; min-height:360px; }
            .sidebar {
                width:160px; background:#fff; border-right:1px solid #e0e0e0;
                padding:12px 0; flex-shrink:0;
            }
            .sidebar-item {
                padding:8px 16px; font-size:12px; color:#555; cursor:pointer;
                display:flex; align-items:center; gap:8px;
            }
            .sidebar-item.active { background:#e8f0fe; color:#1a73e8; font-weight:600; border-left:3px solid #1a73e8; }
            .sidebar-item:hover { background:#f5f5f5; }

            .content { flex:1; padding:20px; }
            .content h2 { font-size:15px; color:#333; margin-bottom:16px; font-weight:600; }

            /* TABLE */
            .data-table { width:100%; border-collapse:collapse; font-size:12px; }
            .data-table th {
                background:#f8f9fa; padding:8px 12px; text-align:left;
                border-bottom:2px solid #dee2e6; color:#666; font-weight:600; font-size:11px;
            }
            .data-table td { padding:8px 12px; border-bottom:1px solid #f0f0f0; color:#444; }
            .data-table tr:hover { background:#f8f9fa; }
            .badge {
                display:inline-block; padding:2px 8px; border-radius:10px;
                font-size:10px; font-weight:600;
            }
            .badge.admin { background:#ffeeba; color:#856404; }
            .badge.user { background:#d4edda; color:#155724; }

            /* INJECTED overlay */
            .inject-overlay {
                display:none; position:absolute; top:0;left:0;right:0;bottom:0;
                background:rgba(231,76,60,0.08); pointer-events:none; border-radius:4px;
            }
            .inject-banner {
                display:none; background:#d4edda; border:1px solid #28a745;
                color:#155724; padding:8px 12px; font-size:11px; margin-bottom:12px;
                border-radius:4px;
            }

            /* HINGE + BASE */
            .hinge {
                width:100%; height:8px;
                background:linear-gradient(180deg,#1a1a1a,#2d2d2d); position:relative;
            }
            .hinge::after {
                content:''; position:absolute; left:50%; top:50%;
                transform:translate(-50%,-50%); width:40px; height:4px;
                background:#111; border-radius:2px;
            }
            .base {
                background:linear-gradient(180deg,#2d2d2d,#222); width:108%; height:18px;
                border-radius:0 0 12px 12px; box-shadow:0 4px 15px rgba(0,0,0,0.5); position:relative;
            }
            .base::after {
                content:''; position:absolute; bottom:4px; left:50%;
                transform:translateX(-50%); width:50px; height:3px;
                background:#1a1a1a; border-radius:2px;
            }
            </style>

            <div class="laptop-wrap">
                <div class="screen-outer">
                    <div class="screen-inner" style="position:relative;">
                        <div class="inject-overlay" id="overlay"></div>
                        <div class="browser-bar">
                            <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                            <div class="url-bar">
                                🔒 auth.target.local/admin/users
                            </div>
                        </div>
                        <div class="topnav">
                            <div class="logo">Corp<span>Sec</span> Admin</div>
                            <div class="user-info">
                                <div class="avatar">A</div>
                                <span>admin</span>
                            </div>
                        </div>
                        <div class="dashboard">
                            <div class="sidebar">
                                <div class="sidebar-item active">👥 Gebruikers</div>
                                <div class="sidebar-item">📊 Dashboard</div>
                                <div class="sidebar-item">⚙️ Instellingen</div>
                                <div class="sidebar-item">📋 Logs</div>
                                <div class="sidebar-item">🔒 Beveiliging</div>
                            </div>
                            <div class="content">
                                <h2>Gebruikersbeheer</h2>
                                <div class="inject-banner" id="injectBanner">
                                    ✅ UNION SELECT uitgevoerd — verborgen data zichtbaar in resultaten!
                                </div>
                                <table class="data-table" id="userTable">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Gebruikersnaam</th>
                                            <th>E-mail</th>
                                            <th>Rol</th>
                                        </tr>
                                    </thead>
                                    <tbody id="tableBody">
                                        <tr><td>1</td><td>jan.de.vries</td><td>jan@corp.nl</td><td><span class="badge user">user</span></td></tr>
                                        <tr><td>2</td><td>lisa.bakker</td><td>lisa@corp.nl</td><td><span class="badge user">user</span></td></tr>
                                        <tr><td>3</td><td>mark.smit</td><td>mark@corp.nl</td><td><span class="badge user">user</span></td></tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="hinge"></div>
                <div class="base"></div>
            </div>

            <script>
            function injectUnion() {
                document.getElementById('overlay').style.display = 'block';
                document.getElementById('injectBanner').style.display = 'block';
                const tbody = document.getElementById('tableBody');
                const injRow = document.createElement('tr');
                injRow.style.background = '#fff3cd';
                injRow.style.fontWeight = '600';
                injRow.innerHTML = `
                    <td style="color:#e74c3c">UNION</td>
                    <td style="color:#e74c3c">admin</td>
                    <td style="color:#e74c3c">SuperSecret!</td>
                    <td><span class="badge admin">ADMIN</span></td>
                `;
                tbody.appendChild(injRow);
            }
            window.addEventListener('message', e => { if(e.data === 'union') injectUnion(); });
            </script>
            """, height=520)

        st.markdown("**Voer je UNION SELECT query in:**")
        cmd = st.text_input("root@db:~#", key="sql3", placeholder="' UNION SELECT username, password, role FROM users--")
        if st.button("▶ QUERY", key="sql3_btn"):
            if "union" in cmd.lower() and "select" in cmd.lower():
                fake_progress("DATABASE DUMPEN")
                give_flag(user, "sql", "GV 71")
                components.html("<script>window.parent.frames[0] && window.parent.frames[0].postMessage('union','*'); setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
                typewriter_terminal([
                    "[+] UNION query uitgevoerd",
                    "[+] Resultaten gecombineerd:",
                    "",
                    "  username | password     | role",
                    "  ---------|--------------|------",
                    "  admin    | SuperSecret! | ADMIN",
                    "",
                    "[✓] DATA GEËXTRAHEERD"
                ])
                st.success("🏴 FLAG BEHAALD: **GV 71**")
            elif "union" in cmd.lower():
                st.warning("⚠ Je hebt UNION — maar je mist nog iets... voeg SELECT toe.")
            else:
                st.error("❌ Gebruik UNION SELECT om data uit andere tabellen te halen.")
        hint_widget(user, "sql", lvl)

# ==========================================================
# ROOM 2 — XSS
# ==========================================================
with tabs[1]:
    st.header("SECURITY PORTAL")
    st.markdown("*Injecteer kwaadaardige scripts in de webapplicatie.*")
    lvl = get_level(user, "xss")

    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        st.markdown("""
```
[ANALYSE FASE]
Target: http://portal.target.local/feedback
De applicatie geeft gebruikersinput terug op de pagina.
Welk type aanval is hier van toepassing?
```
        """)
        cmd = st.text_input("analysis>", key="xss1", placeholder="type aanvalstype...")
        if st.button("▶ ANALYSE", key="xss1_btn"):
            if "cross site scripting" in cmd.lower() or cmd.lower() == "xss":
                fake_progress("KWETSBAARHEID BEVESTIGEN")
                set_level(user, "xss", 2)
                typewriter_terminal([
                    "[+] Cross-Site Scripting (XSS) gedetecteerd",
                    "[+] Input wordt direct in HTML gereflecteerd",
                    "[!] Exploitatiefase gestart..."
                ])
                st.rerun()
            else:
                st.error("❌ Incorrect. Denk: welke aanval injecteert scripts?")
        hint_widget(user, "xss", lvl)

    elif lvl == 2:
        st.markdown("""
```
[REFLECTED XSS]
De searchbalk geeft jouw input direct terug.
Injecteer een script dat wordt uitgevoerd door de browser.
```
        """)
        cmd = st.text_input("payload>", key="xss2", placeholder="<...>")
        if st.button("▶ INJECT", key="xss2_btn"):
            if "<script>" in cmd.lower():
                fake_progress("PAYLOAD INJECTEREN")
                set_level(user, "xss", 3)
                typewriter_terminal([
                    "[+] Script tag gedetecteerd in input",
                    "[+] Browser voert JavaScript uit in context van slachtoffer",
                    "[✓] REFLECTED XSS GESLAAGD"
                ])
                st.rerun()
            else:
                st.error("❌ Geen script gedetecteerd. Welke HTML tag voert code uit?")
        hint_widget(user, "xss", lvl)

    elif lvl == 3:
        st.markdown("""
```
[PERSISTENT XSS]
Nu sla je een payload op in de database.
Elke bezoeker die de pagina laadt voert jouw script uit.
Injecteer een persistent payload.
```
        """)
        cmd = st.text_area("persistent payload>", key="xss3", placeholder="<script>...</script>")
        if st.button("▶ OPSLAAN & INJECTEREN", key="xss3_btn"):
            if "<script>" in cmd.lower():
                fake_progress("PAYLOAD OPSLAAN IN DATABASE")
                give_flag(user, "xss", "N75 ZS")
                typewriter_terminal([
                    "[+] Payload opgeslagen in database",
                    "[+] Script wordt uitgevoerd bij elke paginabezoek",
                    "[✓] PERSISTENT XSS GESLAAGD"
                ])
                st.success("🏴 FLAG BEHAALD: **N75 ZS**")
                components.html("<script>setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
            else:
                st.error("❌ Geen persistent script gedetecteerd.")
        hint_widget(user, "xss", lvl)

# ==========================================================
# ROOM 3 — PRIVILEGE ESCALATION
# ==========================================================
with tabs[2]:
    st.header("CONTROL ROOM")
    st.markdown("*Verhoog je privileges om admin toegang te krijgen.*")
    lvl = get_level(user, "privesc")

    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        st.markdown("""
```
[SYSTEEM ANALYSE]
Ingelogd als: guest
Privileges: READ_ONLY
Doel: Verkrijg admin rechten
Welk type aanval verschaft hogere privileges?
```
        """)
        cmd = st.text_input("analysis>", key="priv1", placeholder="type aanvalstype...")
        if st.button("▶ ANALYSE", key="priv1_btn"):
            if "privilege escalation" in cmd.lower() or "privesc" in cmd.lower():
                fake_progress("BEVEILIGINGSLEK ANALYSEREN")
                set_level(user, "privesc", 2)
                typewriter_terminal([
                    "[+] Privilege Escalation aanval geïdentificeerd",
                    "[+] Rolbeheer systeem bevat misconfiguratie",
                    "[!] Exploitatie mogelijk..."
                ])
                st.rerun()
            else:
                st.error("❌ Incorrect. Hoe noem je het verhogen van gebruikersrechten?")
        hint_widget(user, "privesc", lvl)

    elif lvl == 2:
        st.markdown("""
```
[EXPLOIT FASE]
Huidig gebruikersobject: { "username": "guest", "role": "user" }
Het systeem accepteert een directe rolwijziging.
Welke rol wil je claimen?
```
        """)
        cmd = st.text_input("role=user>", key="priv2", placeholder="nieuwe rol...")
        if st.button("▶ ESCALATE", key="priv2_btn"):
            if cmd.lower().strip() == "admin":
                fake_progress("PRIVILEGES ESCALEREN")
                set_level(user, "privesc", 3)
                typewriter_terminal([
                    "[+] Rolparameter gewijzigd: user → admin",
                    "[+] Server accepteert nieuwe rol zonder verificatie",
                    "[✓] ADMIN PRIVILEGES VERKREGEN"
                ])
                st.rerun()
            else:
                st.error("❌ Die rol geeft geen volledige toegang.")
        hint_widget(user, "privesc", lvl)

    elif lvl == 3:
        st.markdown("""
```
[PERSISTENTIE]
Je hebt admin toegang. Maak deze permanent.
Status: ADMIN — Druk op de knop om toegang te persisteren.
```
        """)
        if st.button("🔒 PERSISTEER TOEGANG", key="priv3_btn", use_container_width=True):
            fake_progress("BACKDOOR INSTALLEREN")
            give_flag(user, "privesc", "ZIF VH")
            typewriter_terminal([
                "[+] Admin token opgeslagen",
                "[+] Backdoor geïnstalleerd",
                "[✓] PERMANENTE TOEGANG VERKREGEN"
            ])
            st.success("🏴 FLAG BEHAALD: **ZIF VH**")
            components.html("<script>setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
        hint_widget(user, "privesc", lvl)

# ==========================================================
# ROOM 4 — VAULT (CRYPTO)
# ==========================================================
with tabs[3]:
    st.header("VAULT TOEGANG")
    st.markdown("*Decodeer het eindwachtwoord om de kluis te openen.*")

    rooms_complete = [has_completed(user, r) for r in ["sql", "xss", "privesc"]]
    if not all(rooms_complete):
        missing = [r.upper() for r, done in zip(["sql","xss","privesc"], rooms_complete) if not done]
        st.error(f"⛔ TOEGANG GEWEIGERD — Voltooi eerst: {', '.join(missing)}")
        st.stop()

    lvl = get_level(user, "crypto")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        st.markdown("""
```
[VAULT SYSTEEM]
Beveiligingsniveau: MAXIMUM
Versleuteld eindwachtwoord gedetecteerd.
Welk klassiek versleutelingssysteem is hier gebruikt?
```
        """)
        cmd = st.text_input("analysis>", key="crypto1", placeholder="naam van het systeem...")
        if st.button("▶ ANALYSEER", key="crypto1_btn"):
            if "caesar" in cmd.lower():
                fake_progress("ENCRYPTIE IDENTIFICEREN")
                set_level(user, "crypto", 2)
                typewriter_terminal([
                    "[+] Caesar cipher geïdentificeerd",
                    "[+] Klassieke verschuivingscodering",
                    "[!] Decryptie vereist..."
                ])
                st.rerun()
            else:
                st.error("❌ Incorrect. Welke Romeinse keizer stond bekend om zijn code?")
        hint_widget(user, "crypto", lvl)

    elif lvl == 2:
        st.markdown("**Decodeer de volgende versleutelde sleutels:**")
        st.code("GV 71   N75 ZS   ZIF VH", language=None)
        st.markdown("""
```
[HINT] De letters zijn verschoven. Combineer de gedecodeerde
       letters tot het eindwachtwoord.
       Formaat: EXAMENKLAS[JAAR]
```
        """)
        cmd = st.text_input("decrypt>", key="crypto2", placeholder="eindwachtwoord...")
        if st.button("▶ ONTSLEUTEL VAULT", key="crypto2_btn", use_container_width=True):
            if cmd.strip().upper() == "EXAMENKLAS2026":
                fake_progress("VAULT ONTGRENDELEN")
                set_level(user, "crypto", 3)
                typewriter_terminal([
                    "[+] Wachtwoord correct",
                    "[+] Vault ontgrendeld...",
                    "",
                    "  ████████████████████████████",
                    "  █  MISSIE VOLTOOID          █",
                    "  █  Alle systemen gecompromitteerd █",
                    "  ████████████████████████████",
                ])
                give_flag(user, "crypto", "EXAMENKLAS2026")
                st.success("🏆 **EINDCODE GEACCEPTEERD — MISSIE VOLTOOID!**")
                st.balloons()
                components.html("<script>setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
            else:
                st.error("❌ Verkeerde code. Decodeer alle vlaggen en combineer ze.")
        hint_widget(user, "crypto", lvl)

    elif lvl == 3:
        st.success("🏆 **VAULT GEOPEND — MISSIE VOLTOOID!**")
        typewriter_terminal([
            "[✓] SQL Injection     — GECOMPROMITTEERD",
            "[✓] XSS               — GECOMPROMITTEERD",
            "[✓] Privilege Esc.    — GECOMPROMITTEERD",
            "[✓] Cryptografie      — GEDECODEERD",
            "",
            "[✓] SYSTEEM VOLLEDIG OVERGENOMEN",
        ])

# ==========================================================
# LOGOUT + RESET
# ==========================================================
st.markdown("---")
col_logout, col_reset = st.columns([1, 1])

with col_logout:
    if st.button("🔓 LOGOUT", key="logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

with col_reset:
    if st.button("🗑 RESET PROGRESSIE", key="reset_btn", use_container_width=True):
        st.session_state["confirm_reset"] = True

if st.session_state.get("confirm_reset"):
    st.warning("⚠️ Weet je zeker dat je alle progressie wil resetten?")
    col_yes, col_no = st.columns([1, 1])
    with col_yes:
        if st.button("✅ JA, RESET ALLES", key="confirm_yes", use_container_width=True):
            conn = sqlite3.connect("platform.db")
            c = conn.cursor()
            c.execute("DELETE FROM progress WHERE username=?", (user,))
            c.execute("DELETE FROM flags WHERE username=?", (user,))
            c.execute("DELETE FROM hints WHERE username=?", (user,))
            conn.commit()
            conn.close()
            st.session_state.pop("confirm_reset", None)
            st.success("✅ Progressie gereset!")
            time.sleep(1)
            st.rerun()
    with col_no:
        if st.button("❌ ANNULEREN", key="confirm_no", use_container_width=True):
            st.session_state.pop("confirm_reset", None)
            st.rerun()
