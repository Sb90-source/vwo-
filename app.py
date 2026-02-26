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
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
<style>
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
#MainMenu, footer, header {visibility: hidden;}
.block-container { padding-top: 1rem !important; }

/* SCANLINES */
body::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent, transparent 2px,
        rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* GLITCH TITLE ANIMATION — targets our custom div, not h1 */
@keyframes glitch {
    0%,90%,100% { text-shadow: 0 0 15px rgba(0,255,156,0.5); transform: translate(0); clip-path: none; }
    91% { text-shadow: -3px 0 #ff003c, 3px 0 #00ffff; transform: translate(-2px, 0); }
    92% { text-shadow: 3px 0 #ff003c, -3px 0 #00ffff; transform: translate(2px, 0); clip-path: inset(10% 0 60% 0); }
    93% { text-shadow: -3px 0 #ff003c, 3px 0 #00ffff; transform: translate(-1px, 0); clip-path: inset(50% 0 20% 0); }
    94% { text-shadow: 0 0 15px rgba(0,255,156,0.5); transform: translate(0); clip-path: none; }
}
@keyframes glitch2 {
    0%,88%,100% { opacity: 0; }
    89% { opacity: 0.8; transform: translate(4px, -2px); filter: hue-rotate(90deg); }
    91% { opacity: 0; }
}
.glitch-title {
    font-family: 'Orbitron', monospace !important;
    color: #00ff9c;
    font-size: clamp(18px, 3vw, 36px);
    font-weight: 900;
    letter-spacing: 6px;
    text-align: center;
    animation: glitch 4s infinite;
    position: relative;
    display: inline-block;
}
.glitch-title::before {
    content: attr(data-text);
    position: absolute;
    left: 0; top: 0;
    color: #ff003c;
    animation: glitch2 4s infinite;
    pointer-events: none;
}
.glitch-wrapper { text-align: center; padding: 1rem 0 0.5rem; }

@keyframes flicker {
    0%,95%,100% { opacity:1; }
    96% { opacity:0.5; }
    97% { opacity:1; }
    98% { opacity:0.3; }
}
body { animation: flicker 8s infinite; }

/* PROGRESS BAR OVERRIDE */
.stProgress > div > div {
    background: linear-gradient(90deg, #00ff9c, #00ffcc) !important;
}
</style>
""", unsafe_allow_html=True)

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
    return get_level(user, room) >= 3

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
    components.html("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
    <style>
    @keyframes glitch {
        0%,88%,100% { text-shadow: 0 0 15px rgba(0,255,156,0.6); transform: translate(0); }
        89% { text-shadow: -4px 0 #ff003c, 4px 0 #00ffff; transform: translate(-3px,0); clip-path: inset(10% 0 50% 0); }
        90% { text-shadow: 4px 0 #ff003c, -4px 0 #00ffff; transform: translate(3px,0); clip-path: inset(60% 0 5% 0); }
        91% { text-shadow: -2px 0 #ff003c, 2px 0 #00ffff; transform: translate(-1px,0); clip-path: none; }
        92% { text-shadow: 0 0 15px rgba(0,255,156,0.6); transform: translate(0); }
    }
    @keyframes glitch2 {
        0%,88%,100% { opacity:0; }
        89% { opacity:0.6; transform:translate(6px,-3px); filter:hue-rotate(120deg) saturate(2); }
        91% { opacity:0; }
    }
    body { margin:0; background:#020409; text-align:center; padding-top: 30px; }
    .title {
        font-family: 'Orbitron', monospace;
        font-weight: 900;
        font-size: clamp(20px, 4vw, 48px);
        color: #00ff9c;
        letter-spacing: 6px;
        animation: glitch 5s infinite;
        position: relative;
        display: inline-block;
    }
    .title::before {
        content: 'CYBER BREACH SIMULATOR';
        position: absolute; left:0; top:0;
        color: #ff003c;
        animation: glitch2 5s infinite;
        pointer-events: none;
    }
    .sub {
        font-family: 'Share Tech Mono', monospace;
        color: rgba(0,255,156,0.5);
        font-size: 11px;
        letter-spacing: 5px;
        margin-top: 12px;
    }
    .line { color: rgba(0,255,156,0.2); font-family: monospace; margin-top:8px; }
    </style>
    <div class="title">CYBER BREACH SIMULATOR</div>
    <div class="sub">SIMULATOR v2.0 &mdash; AUTHORIZED TRAINING ONLY</div>
    <div class="line">&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;&#9472;</div>
    """, height=130)

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

    # Progress indicator
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
        st.markdown("""
```
[EXPLOIT FASE]
Target: http://auth.target.local/login
Username field: [ _________________ ]
Password field: [ _________________ ]

Bypass de authenticatie via SQL injectie.
```
        """)
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
        st.markdown("""
```
[DATA EXTRACTION]
Verbonden als: admin
Toegang: DATABASE READ
Taak: Extraheer admin credentials via UNION attack
```
        """)
        cmd = st.text_input("root@db:~#", key="sql3", placeholder="SELECT ... UNION ...")
        if st.button("▶ QUERY", key="sql3_btn"):
            if "union" in cmd.lower() and "select" in cmd.lower():
                fake_progress("DATABASE DUMPEN")
                give_flag(user, "sql", "GV 71")
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
                components.html("<script>window.parent.postMessage('success','*'); setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
            elif "union" in cmd.lower():
                st.warning("⚠ Je hebt UNION — maar je mist nog iets...")
            else:
                st.error("❌ Gebruik UNION om data te combineren.")
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
# LOGOUT
# ==========================================================
st.markdown("---")
if st.button("🔓 LOGOUT", key="logout"):
    st.session_state.clear()
    st.rerun()
