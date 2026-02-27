import streamlit as st
import sqlite3
import hashlib
import time
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("💀 THE WHITE HOUSE", layout="wide", initial_sidebar_state="expanded")

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
        [data-testid="stSidebar"] {
            background-color: #050e08 !important;
            border-right: 1px solid #00ff9c !important;
        }
        [data-testid="stSidebar"] * {
            color: #00ff9c !important;
            font-family: 'Share Tech Mono', monospace !important;
        }
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
        h1 { animation: flicker 3s infinite; }
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
            <span class="glitch-t" data-text="THE WHITE HOUSE">THE WHITE HOUSE</span>
        </div>
        <p style="letter-spacing:6px;color:rgba(0,255,156,0.5);font-size:11px;margin-top:12px;font-family:'Share Tech Mono',monospace;">
            ESCAPEROOM &mdash; GEMAAKT DOOR: ANOUK, MARWA, FENNA EN NOURA
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
    @keyframes flicker {
        0%,89%,91%,93%,100% { opacity:1; }
        90% { opacity:0.3; }
        92% { opacity:0.6; }
        94% { opacity:0.1; }
        95% { opacity:0.8; }
        96% { opacity:0.2; }
        97% { opacity:1; }
    }
    .glitch-t {
        font-family:'Orbitron',monospace !important;
        font-weight:900;
        font-size:clamp(22px,3.5vw,52px);
        color:#00ff9c;
        letter-spacing:6px;
        animation:gt 5s infinite, flicker 3s infinite;
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
        u = st.text_input("GEBRUIKERSNAAM", placeholder="operative_id")
        p = st.text_input("WACHTWOORD", type="password", placeholder="••••••••")
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

# Sidebar met logout en reset
with st.sidebar:
    st.markdown(f"### 🕶 {user.upper()}")
    rooms_done_sb = sum(1 for r in ["sql","xss","privesc","crypto"] if has_completed(user, r))
    st.markdown(f"**MISSIES:** {rooms_done_sb}/4")
    st.markdown("---")
    if st.button("🔓 LOGOUT", key="sidebar_logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    if st.button("🗑 RESET PROGRESSIE", key="sidebar_reset", use_container_width=True):
        st.session_state["confirm_reset"] = True
    if st.session_state.get("confirm_reset"):
        st.warning("Zeker weten?")
        if st.button("✅ JA", key="sb_yes", use_container_width=True):
            conn = sqlite3.connect("platform.db")
            c = conn.cursor()
            c.execute("DELETE FROM progress WHERE username=?", (user,))
            c.execute("DELETE FROM flags WHERE username=?", (user,))
            c.execute("DELETE FROM hints WHERE username=?", (user,))
            conn.commit(); conn.close()
            st.session_state.pop("confirm_reset", None)
            st.rerun()
        if st.button("❌ NEE", key="sb_no", use_container_width=True):
            st.session_state.pop("confirm_reset", None)
            st.rerun()

# Header
rooms_done = sum(1 for r in ["sql","xss","privesc","crypto"] if has_completed(user, r))
col_title, col_status, col_logout_btn = st.columns([3, 0.7, 0.7])
with col_title:
    st.title(f"🕶 OPERATIVE: {user.upper()}")
with col_status:
    st.metric("MISSIES", f"{rooms_done}/4")
with col_logout_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔓 LOGOUT", key="top_logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

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
        components.html("""
        <style>
        *{box-sizing:border-box;margin:0;padding:0;}
        body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:20px;}
        .laptop-wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
        .screen-outer{
            background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;
            border-radius:16px 16px 0 0;width:100%;padding:16px;
            box-shadow:0 0 40px rgba(0,0,0,0.9),inset 0 0 15px rgba(0,0,0,0.5);position:relative;
        }
        .screen-outer::before{
            content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);
            width:10px;height:10px;background:#333;border-radius:50%;
        }
        .screen-inner{background:#f0f2f5;border-radius:6px;overflow:hidden;}
        .browser-bar{
            background:#e8e8e8;padding:10px 14px;display:flex;align-items:center;
            gap:10px;border-bottom:1px solid #ccc;
        }
        .dot{width:12px;height:12px;border-radius:50%;}
        .dot.r{background:#ff5f57;} .dot.y{background:#febc2e;} .dot.g{background:#28c840;}
        .url-bar{
            flex:1;background:white;border:1px solid #ccc;border-radius:5px;
            padding:4px 12px;font-size:12px;color:#666;display:flex;align-items:center;gap:5px;
        }
        .login-page{padding:30px 50px;display:flex;flex-direction:column;align-items:center;}
        .company-logo{font-size:26px;font-weight:700;color:#1a1a2e;margin-bottom:4px;letter-spacing:-1px;}
        .company-logo span{color:#e74c3c;}
        .tagline{font-size:12px;color:#999;margin-bottom:28px;}
        .login-card{
            background:white;border:1px solid #e0e0e0;border-radius:10px;
            padding:32px 36px;width:100%;max-width:360px;
            box-shadow:0 4px 20px rgba(0,0,0,0.1);transition:all 0.3s;
        }
        .login-card h3{font-size:18px;color:#333;margin-bottom:22px;font-weight:600;}
        .field{margin-bottom:16px;}
        .field label{display:block;font-size:12px;color:#666;margin-bottom:5px;font-weight:500;}
        .field input{
            width:100%;border:1.5px solid #ddd;border-radius:6px;padding:10px 14px;
            font-size:14px;color:#333;background:#fafafa;outline:none;transition:all 0.2s;
        }
        .field input:focus{border-color:#4a90e2;background:white;box-shadow:0 0 0 3px rgba(74,144,226,0.1);}
        .login-btn{
            width:100%;background:#4a90e2;color:white;border:none;border-radius:6px;
            padding:12px;font-size:14px;font-weight:600;cursor:pointer;margin-top:8px;transition:all 0.2s;
        }
        .login-btn:hover{background:#357abd;transform:translateY(-1px);box-shadow:0 4px 12px rgba(74,144,226,0.4);}
        .login-btn:active{transform:translateY(0);}
        .footer-links{display:flex;justify-content:space-between;margin-top:14px;}
        .footer-links a{font-size:11px;color:#4a90e2;text-decoration:none;}
        .footer-links a:hover{text-decoration:underline;}
        .msg{border-radius:6px;padding:10px 14px;font-size:12px;margin-bottom:16px;display:none;}
        .msg.error{background:#fff3cd;border:1px solid #ffc107;color:#856404;}
        .msg.success{background:#d4edda;border:1px solid #28a745;color:#155724;}
        .hinge{
            width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;
        }
        .hinge::after{
            content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
            width:50px;height:5px;background:#111;border-radius:3px;
        }
        .base{
            background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;
            border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;
        }
        .base::after{
            content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);
            width:60px;height:4px;background:#111;border-radius:2px;
        }
        .forgot-modal{
            display:none;position:fixed;top:0;left:0;right:0;bottom:0;
            background:rgba(0,0,0,0.5);z-index:100;align-items:center;justify-content:center;
        }
        .modal-box{
            background:white;border-radius:10px;padding:28px;max-width:300px;width:90%;
            box-shadow:0 10px 40px rgba(0,0,0,0.3);
        }
        .modal-box h4{color:#333;margin-bottom:12px;}
        .modal-box p{font-size:12px;color:#666;margin-bottom:16px;}
        .modal-close{
            background:#e74c3c;color:white;border:none;border-radius:4px;
            padding:8px 16px;cursor:pointer;font-size:12px;
        }
        </style>

        <div class="laptop-wrap">
          <div class="screen-outer">
            <div class="screen-inner">
              <div class="browser-bar">
                <div class="dot r" onclick="alert('Sluiten? Dan verlies je je payload!')"></div>
                <div class="dot y" onclick="document.body.style.opacity='0.5';setTimeout(()=>document.body.style.opacity='1',500)"></div>
                <div class="dot g" onclick="document.body.style.transform='scale(1.02)';setTimeout(()=>document.body.style.transform='scale(1)',300)"></div>
                <div class="url-bar">🔒 auth.target.local/login</div>
              </div>
              <div class="login-page">
                <div class="company-logo">Corp<span>Sec</span></div>
                <div class="tagline">Enterprise Security Portal — Authorized Personnel Only</div>
                <div class="login-card" id="loginCard">
                  <h3>Inloggen</h3>
                  <div class="msg" id="msg"></div>
                  <div class="field">
                    <label>Gebruikersnaam</label>
                    <input type="text" id="uname" placeholder="gebruiker@corp.nl" oninput="liveCheck(this)">
                  </div>
                  <div class="field">
                    <label>Wachtwoord</label>
                    <input type="password" id="pw" placeholder="••••••••">
                  </div>
                  <button class="login-btn" onclick="tryLogin()">Inloggen</button>
                  <div class="footer-links">
                    <a href="javascript:void(0)" onclick="showForgot()">Wachtwoord vergeten?</a>
                    <a href="javascript:void(0)" onclick="showHelp()">Hulp nodig?</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="hinge"></div>
          <div class="base"></div>
        </div>

        <div class="forgot-modal" id="forgotModal">
          <div class="modal-box">
            <h4>Wachtwoord vergeten?</h4>
            <p>Neem contact op met de systeembeheerder op it-support@corp.nl of bel intern 4242.</p>
            <button class="modal-close" onclick="document.getElementById('forgotModal').style.display='none'">Sluiten</button>
          </div>
        </div>

        <script>
        function liveCheck(inp) {
            const v = inp.value.toLowerCase();
            if (v.includes("' or") || v.includes("'or") || v.includes("1=1")) {
                inp.style.borderColor = '#e74c3c';
                inp.style.background = '#fff5f5';
            } else {
                inp.style.borderColor = '';
                inp.style.background = '';
            }
        }
        function tryLogin() {
            const u = document.getElementById('uname').value;
            const p = document.getElementById('pw').value;
            const msg = document.getElementById('msg');
            const card = document.getElementById('loginCard');
            const isInjection = u.toLowerCase().includes("' or") || u.toLowerCase().includes("'or") || u.toLowerCase().includes("1=1");
            if (isInjection) {
                card.style.borderColor = '#28a745';
                card.style.background = '#f0fff4';
                msg.className = 'msg success';
                msg.style.display = 'block';
                msg.innerHTML = '✅ SQL INJECTION GESLAAGD — Ingelogd als: <strong>admin</strong><br><small>Doorsturen naar admin panel...</small>';
                // Trigger Streamlit to advance level via URL param after short delay
                setTimeout(() => {
                    window.parent.location.href = window.parent.location.href.split('?')[0] + '?sql2_submit=1';
                }, 1500);
            } else if (u === 'admin' && p === 'admin') {
                msg.className = 'msg success';
                msg.style.display = 'block';
                msg.innerHTML = '✅ Welkom terug, admin!';
            } else if (u === '' || p === '') {
                msg.className = 'msg error';
                msg.style.display = 'block';
                msg.innerHTML = '⚠️ Vul alle velden in.';
            } else {
                msg.className = 'msg error';
                msg.style.display = 'block';
                msg.innerHTML = '⛔ Ongeldige inloggegevens. Probeer opnieuw.';
                card.style.animation = 'shake 0.3s ease';
                setTimeout(() => card.style.animation = '', 300);
            }
        }
        function showForgot() {
            document.getElementById('forgotModal').style.display = 'flex';
        }
        // Prevent any link from navigating away
        document.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', e => { e.preventDefault(); });
        });
        function showHelp() {
            alert('Helpdesk: it-support@corp.nl | Tel: +31 20 555 4242\nOpeningstijden: ma-vr 08:00-17:00');
        }
        document.addEventListener('keydown', e => { if(e.key === 'Enter') tryLogin(); });

        const style = document.createElement('style');
        style.textContent = '@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-8px)} 75%{transform:translateX(8px)} }';
        document.head.appendChild(style);
        </script>
        """, height=700)

        # Check if injection was submitted via laptop UI
        if st.session_state.get("sql2_injected"):
            fake_progress("AUTHENTICATIE BYPASSEN")
            set_level(user, "sql", 3)
            st.session_state.pop("sql2_injected", None)
            typewriter_terminal([
                "[+] SQL query gemanipuleerd",
                "[+] WHERE clause: TRUE voor alle rijen",
                "[+] Ingelogd als eerste gebruiker in database",
                "[✓] AUTHENTICATIE BYPASSED"
            ])
            st.rerun()

        # Hidden form that laptop JS can trigger via URL param
        if st.query_params.get("sql2_submit") == "1":
            st.query_params.clear()
            set_level(user, "sql", 3)
            st.rerun()

        hint_widget(user, "sql", lvl)

    elif lvl == 3:
        # Handle SQL3 submission from laptop UI
        if st.query_params.get("sql3_submit") == "1":
            st.query_params.clear()
            fake_progress("DATABASE DUMPEN")
            give_flag(user, "sql", "GV 71")
            typewriter_terminal([
                "[+] UNION query uitgevoerd",
                "[+] Resultaten gecombineerd:",
                "",
                "  ID     | username | password     | role",
                "  -------|----------|--------------|------",
                "  UNION  | admin    | SuperSecret! | ADMIN",
                "",
                "[✓] DATA GEËXTRAHEERD"
            ])
            st.success("🏴 FLAG BEHAALD: **GV 71**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html("""
            <style>
            *{box-sizing:border-box;margin:0;padding:0;}
            body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
            .laptop-wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
            .screen-outer{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
            .screen-outer::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
            .screen-inner{background:#f5f6fa;border-radius:6px;overflow:hidden;}
            .browser-bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
            .dot{width:12px;height:12px;border-radius:50%;cursor:pointer;}
            .dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
            .url-bar{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;}
            .topnav{background:#1a73e8;color:white;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;}
            .topnav .logo{font-size:16px;font-weight:700;}
            .topnav .logo span{color:#ffd700;}
            .topnav .user-info{display:flex;align-items:center;gap:8px;font-size:12px;}
            .avatar{width:30px;height:30px;border-radius:50%;background:#ffd700;color:#1a1a2e;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:13px;}
            .dashboard{display:flex;}
            .sidebar{width:165px;background:#fff;border-right:1px solid #e0e0e0;padding:12px 0;flex-shrink:0;}
            .sidebar-item{padding:9px 16px;font-size:12px;color:#555;cursor:pointer;display:flex;align-items:center;gap:8px;}
            .sidebar-item.active{background:#e8f0fe;color:#1a73e8;font-weight:600;border-left:3px solid #1a73e8;}
            .sidebar-item:hover{background:#f5f5f5;}
            .content{flex:1;padding:16px;display:flex;flex-direction:column;gap:10px;}
            .content h2{font-size:14px;color:#333;font-weight:600;}
            .sql-console{background:#1e1e2e;border-radius:8px;overflow:hidden;border:1px solid #333;}
            .sql-header{background:#2d2d3d;padding:8px 14px;display:flex;align-items:center;gap:8px;border-bottom:1px solid #444;}
            .sql-header span{font-size:11px;color:#888;font-family:monospace;}
            .db-name{color:#4fc3f7 !important;font-weight:600;}
            .sql-input-row{display:flex;align-items:center;padding:10px 14px;gap:8px;}
            .sql-prompt{color:#00ff9c;font-family:monospace;font-size:13px;white-space:nowrap;}
            .sql-input{flex:1;background:transparent;border:none;outline:none;color:#e0e0e0;font-family:monospace;font-size:13px;caret-color:#00ff9c;}
            .sql-btn{background:#1a73e8;color:white;border:none;border-radius:4px;padding:5px 14px;font-size:12px;cursor:pointer;font-weight:600;}
            .sql-btn:hover{background:#1557b0;}
            .results{padding:0 14px 14px;}
            .result-info{font-size:11px;color:#888;padding:6px 0 8px;font-family:monospace;}
            .result-info.ok{color:#28a745;}
            .result-info.err{color:#e74c3c;}
            .data-table{width:100%;border-collapse:collapse;font-size:12px;}
            .data-table th{background:#f8f9fa;padding:8px 12px;text-align:left;border-bottom:2px solid #dee2e6;color:#666;font-weight:600;font-size:11px;}
            .data-table td{padding:8px 12px;border-bottom:1px solid #f0f0f0;color:#444;}
            .inject-row td{color:#e74c3c !important;font-weight:700;background:#fff8e1 !important;}
            .badge{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;}
            .badge.admin{background:#ffeeba;color:#856404;}
            .badge.user{background:#d4edda;color:#155724;}
            .hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
            .hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
            .base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
            .base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}
            </style>

            <div class="laptop-wrap">
              <div class="screen-outer">
                <div class="screen-inner">
                  <div class="browser-bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url-bar">🔒 auth.target.local/admin/users</div>
                  </div>
                  <div class="topnav">
                    <div class="logo">Corp<span>Sec</span> Admin</div>
                    <div class="user-info"><div class="avatar">A</div><span>admin</span></div>
                  </div>
                  <div class="dashboard">
                    <div class="sidebar">
                      <div class="sidebar-item active">👥 Gebruikers</div>
                      <div class="sidebar-item" onclick="showMsg('Dashboard — geen rechten')">📊 Dashboard</div>
                      <div class="sidebar-item" onclick="showMsg('Instellingen — geen rechten')">⚙️ Instellingen</div>
                      <div class="sidebar-item" onclick="showMsg('Logs — geen rechten')">📋 Logs</div>
                      <div class="sidebar-item" onclick="showMsg('Beveiliging — geen rechten')">🔒 Beveiliging</div>
                    </div>
                    <div class="content">
                      <h2>Gebruikersbeheer — SQL Query Interface</h2>
                      <div class="sql-console">
                        <div class="sql-header">
                          <span>DB:</span><span class="db-name">corpsec_db</span>
                          <span style="margin-left:auto;">TABLE: users</span>
                        </div>
                        <div class="sql-input-row">
                          <span class="sql-prompt">sql&gt;</span>
                          <input class="sql-input" id="sqlInput" type="text"
                            value="SELECT * FROM users"
                            onkeydown="if(event.key==='Enter')runQuery()">
                          <button class="sql-btn" onclick="runQuery()">▶ RUN</button>
                        </div>
                        <div class="results">
                          <div class="result-info" id="info">3 rijen gevonden</div>
                          <table class="data-table">
                            <thead><tr><th>ID</th><th>Gebruikersnaam</th><th>E-mail / Wachtwoord</th><th>Rol</th></tr></thead>
                            <tbody id="tbody">
                              <tr><td>1</td><td>jan.de.vries</td><td>jan@corp.nl</td><td><span class="badge user">user</span></td></tr>
                              <tr><td>2</td><td>lisa.bakker</td><td>lisa@corp.nl</td><td><span class="badge user">user</span></td></tr>
                              <tr><td>3</td><td>mark.smit</td><td>mark@corp.nl</td><td><span class="badge user">user</span></td></tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>

            <script>
            function runQuery() {
                const q = document.getElementById('sqlInput').value.toLowerCase();
                const info = document.getElementById('info');
                const tbody = document.getElementById('tbody');
                if (q.includes('union') && q.includes('select')) {
                    const row = document.createElement('tr');
                    row.className = 'inject-row';
                    row.innerHTML = '<td>UNION</td><td>admin</td><td>SuperSecret!</td><td><span class="badge admin">ADMIN</span></td>';
                    tbody.appendChild(row);
                    info.className = 'result-info ok';
                    info.innerHTML = '⚠️ 4 rijen gevonden — 1 geïnjecteerde rij via UNION SELECT!';
                    setTimeout(() => {
                        const url = window.parent.location.href.split("?")[0] + "?sql3_submit=1";
                        window.parent.location.href = url;
                    }, 2000);
                } else if (q.includes('drop')||q.includes('delete')||q.includes('truncate')) {
                    info.className = 'result-info err';
                    info.innerHTML = '⛔ ERROR: Schrijfrechten geweigerd.';
                } else if (q.includes('select') && q.includes('where')) {
                    info.className = 'result-info';
                    info.innerHTML = '1 rij gevonden';
                    tbody.innerHTML = '<tr><td>1</td><td>jan.de.vries</td><td>jan@corp.nl</td><td><span class="badge user">user</span></td></tr>';
                } else if (q.includes('select')) {
                    info.className = 'result-info';
                    info.innerHTML = '3 rijen gevonden';
                    tbody.innerHTML = `<tr><td>1</td><td>jan.de.vries</td><td>jan@corp.nl</td><td><span class="badge user">user</span></td></tr><tr><td>2</td><td>lisa.bakker</td><td>lisa@corp.nl</td><td><span class="badge user">user</span></td></tr><tr><td>3</td><td>mark.smit</td><td>mark@corp.nl</td><td><span class="badge user">user</span></td></tr>`;
                } else {
                    info.className = 'result-info err';
                    info.innerHTML = '⛔ SQL SYNTAX ERROR.';
                }
            }
            function showMsg(m) {
                document.querySelector('.content').innerHTML = '<h2>' + m + '</h2><p style="color:#999;font-size:12px;margin-top:12px;">Geen toegang via SQL-interface.</p>';
            }
            </script>
            """, height=560)
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
        if st.query_params.get("xss2_submit") == "1":
            st.query_params.clear()
            fake_progress("PAYLOAD INJECTEREN")
            set_level(user, "xss", 3)
            typewriter_terminal([
                "[+] Script tag gedetecteerd in input",
                "[+] Browser voert JavaScript uit in context van slachtoffer",
                "[✓] REFLECTED XSS GESLAAGD"
            ])
            st.rerun()

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html("""
            <style>
            *{box-sizing:border-box;margin:0;padding:0;}
body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
.wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
.screen{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
.screen::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
.inner{border-radius:6px;overflow:hidden;}
.bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
.dot{width:12px;height:12px;border-radius:50%;}
.dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
.url{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;}
.hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
.hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
.base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
.base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}
            .topbar{background:#3c4043;padding:8px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #5f6368;}
            .site-logo{font-size:20px;font-weight:700;color:white;letter-spacing:-1px;}
            .site-logo span{color:#ea4335;}
            .nav-links{display:flex;gap:20px;margin-left:20px;}
            .nav-links a{color:#bdc1c6;font-size:13px;text-decoration:none;}
            .nav-links a:hover{color:white;}
            .content-area{background:white;padding:24px 32px;min-height:320px;}
            .page-title{font-size:20px;font-weight:600;color:#202124;margin-bottom:6px;}
            .page-sub{font-size:13px;color:#5f6368;margin-bottom:20px;}
            .search-row{display:flex;gap:8px;margin-bottom:20px;}
            .search-box{flex:1;border:1.5px solid #dfe1e5;border-radius:24px;padding:10px 18px;font-size:14px;color:#202124;outline:none;transition:all 0.2s;}
            .search-box:focus{border-color:#4285f4;box-shadow:0 0 0 3px rgba(66,133,244,0.15);}
            .search-btn{background:#4285f4;color:white;border:none;border-radius:20px;padding:10px 20px;font-size:13px;cursor:pointer;font-weight:500;}
            .search-btn:hover{background:#3367d6;}
            .result-area{border:1px solid #e0e0e0;border-radius:8px;padding:16px;min-height:80px;background:#fafafa;}
            .result-label{font-size:11px;color:#5f6368;margin-bottom:8px;font-weight:500;}
            .result-text{font-size:14px;color:#202124;}
            .alert-box{display:none;background:#fff3cd;border:1px solid #ffc107;border-radius:6px;padding:10px 14px;font-size:12px;color:#856404;margin-top:10px;}
            .alert-box.xss{background:#d4edda;border-color:#28a745;color:#155724;}
            </style>
            <div class="wrap">
              <div class="screen">
                <div class="inner">
                  <div class="bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url">🔒 portal.target.local/feedback?search=...</div>
                  </div>
                  <div class="topbar">
                    <div class="site-logo">Corp<span>Search</span></div>
                    <div class="nav-links">
                      <a href="javascript:void(0)">Home</a>
                      <a href="javascript:void(0)">Nieuws</a>
                      <a href="javascript:void(0)">Contact</a>
                    </div>
                  </div>
                  <div class="content-area">
                    <div class="page-title">Zoek in ons kennisportaal</div>
                    <div class="page-sub">Voer een zoekterm in — resultaten worden direct getoond op de pagina.</div>
                    <div class="search-row">
                      <input class="search-box" id="searchInput" type="text" placeholder="Zoekterm...">
                      <button class="search-btn" onclick="doSearch()">🔍 Zoeken</button>
                    </div>
                    <div class="result-area">
                      <div class="result-label">ZOEKRESULTAAT — input wordt direct weergegeven:</div>
                      <div class="result-text" id="resultText"><em style="color:#bbb;">Voer een zoekterm in...</em></div>
                    </div>
                    <div class="alert-box" id="alertBox"></div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>
            <script>
            function doSearch() {
                const val = document.getElementById('searchInput').value;
                const result = document.getElementById('resultText');
                const alert = document.getElementById('alertBox');
                if (val.toLowerCase().includes('<script>')) {
                    result.innerHTML = val; // deliberately vulnerable
                    alert.className = 'alert-box xss';
                    alert.style.display = 'block';
                    alert.innerHTML = '✅ XSS GESLAAGD — script tag uitgevoerd in browser context!';
                    setTimeout(() => {
                        window.parent.location.href = window.parent.location.href.split('?')[0] + '?xss2_submit=1';
                    }, 1800);
                } else {
                    result.textContent = val || '(leeg)';
                    alert.className = 'alert-box';
                    alert.style.display = val ? 'block' : 'none';
                    alert.innerHTML = '⚠️ Input weergegeven maar geen script gedetecteerd.';
                }
            }
            document.getElementById('searchInput').addEventListener('keydown', e => {
                if (e.key === 'Enter') doSearch();
            });
            </script>
            """, height=520)
        hint_widget(user, "xss", lvl)

    elif lvl == 3:
        if st.query_params.get("xss3_submit") == "1":
            st.query_params.clear()
            fake_progress("PAYLOAD OPSLAAN IN DATABASE")
            give_flag(user, "xss", "N75 ZS")
            typewriter_terminal([
                "[+] Payload opgeslagen in database",
                "[+] Script wordt uitgevoerd bij elke paginabezoek",
                "[✓] PERSISTENT XSS GESLAAGD"
            ])
            st.success("🏴 FLAG BEHAALD: **N75 ZS**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html("""
            <style>
            *{box-sizing:border-box;margin:0;padding:0;}
body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
.wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
.screen{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
.screen::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
.inner{border-radius:6px;overflow:hidden;}
.bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
.dot{width:12px;height:12px;border-radius:50%;}
.dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
.url{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;}
.hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
.hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
.base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
.base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}
            .topbar{background:#1a73e8;padding:10px 20px;display:flex;align-items:center;justify-content:space-between;}
            .topbar .logo{font-size:16px;font-weight:700;color:white;}
            .topbar .logo span{color:#ffd700;}
            .topbar .user{font-size:12px;color:rgba(255,255,255,0.8);display:flex;align-items:center;gap:8px;}
            .av{width:26px;height:26px;border-radius:50%;background:#ffd700;color:#1a1a2e;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;}
            .page{background:#f5f6fa;min-height:340px;padding:20px 28px;}
            .page h2{font-size:16px;color:#333;font-weight:600;margin-bottom:4px;}
            .page p.sub{font-size:12px;color:#888;margin-bottom:16px;}
            .comments{display:flex;flex-direction:column;gap:10px;margin-bottom:16px;}
            .comment{background:white;border:1px solid #e0e0e0;border-radius:8px;padding:12px 14px;}
            .comment .author{font-size:11px;font-weight:600;color:#1a73e8;margin-bottom:4px;}
            .comment .text{font-size:13px;color:#333;}
            .comment-form{background:white;border:1px solid #e0e0e0;border-radius:8px;padding:14px;}
            .comment-form label{font-size:11px;font-weight:600;color:#555;display:block;margin-bottom:6px;}
            .comment-form textarea{width:100%;border:1.5px solid #ddd;border-radius:6px;padding:8px 12px;font-size:13px;color:#333;resize:none;outline:none;font-family:inherit;}
            .comment-form textarea:focus{border-color:#1a73e8;}
            .post-btn{background:#1a73e8;color:white;border:none;border-radius:6px;padding:8px 20px;font-size:13px;cursor:pointer;margin-top:8px;font-weight:500;}
            .post-btn:hover{background:#1557b0;}
            .xss-banner{display:none;background:#d4edda;border:1px solid #28a745;border-radius:6px;padding:10px;font-size:12px;color:#155724;margin-top:10px;}
            </style>
            <div class="wrap">
              <div class="screen">
                <div class="inner">
                  <div class="bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url">🔒 portal.target.local/news/article?id=42#comments</div>
                  </div>
                  <div class="topbar">
                    <div class="logo">Corp<span>News</span></div>
                    <div class="user"><div class="av">G</div><span>guest</span></div>
                  </div>
                  <div class="page">
                    <h2>Nieuwsartikel: Beveiligingsupdate Q4</h2>
                    <p class="sub">Geplaatst op 12 jan 2025 — 3 reacties</p>
                    <div class="comments" id="comments">
                      <div class="comment"><div class="author">jan.de.vries</div><div class="text">Goed artikel, eindelijk een update!</div></div>
                      <div class="comment"><div class="author">lisa.bakker</div><div class="text">Wanneer wordt dit uitgerold naar productie?</div></div>
                    </div>
                    <div class="comment-form">
                      <label>Plaats een reactie:</label>
                      <textarea id="commentInput" rows="3" placeholder="Schrijf je reactie..."></textarea>
                      <button class="post-btn" onclick="postComment()">💬 Plaatsen</button>
                      <div class="xss-banner" id="xssBanner">✅ PERSISTENT XSS — script opgeslagen in database en uitgevoerd bij elk paginabezoek!</div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>
            <script>
            function postComment() {
                const val = document.getElementById('commentInput').value;
                const comments = document.getElementById('comments');
                const banner = document.getElementById('xssBanner');
                const div = document.createElement('div');
                div.className = 'comment';
                div.style.borderColor = val.toLowerCase().includes('<script>') ? '#28a745' : '#e0e0e0';
                div.innerHTML = '<div class="author" style="color:#e74c3c">jij (aanvaller)</div><div class="text">' + val + '</div>';
                comments.appendChild(div);
                if (val.toLowerCase().includes('<script>')) {
                    banner.style.display = 'block';
                    setTimeout(() => {
                        window.parent.location.href = window.parent.location.href.split('?')[0] + '?xss3_submit=1';
                    }, 2000);
                }
            }
            document.getElementById('commentInput').addEventListener('keydown', e => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); postComment(); }
            });
            </script>
            """, height=560)
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
        if st.query_params.get("priv2_submit") == "1":
            st.query_params.clear()
            fake_progress("PRIVILEGES ESCALEREN")
            set_level(user, "privesc", 3)
            typewriter_terminal([
                "[+] Rolparameter gewijzigd: user → admin",
                "[+] Server accepteert nieuwe rol zonder verificatie",
                "[✓] ADMIN PRIVILEGES VERKREGEN"
            ])
            st.rerun()

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html("""
            <style>
            *{box-sizing:border-box;margin:0;padding:0;}
body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
.wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
.screen{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
.screen::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
.inner{border-radius:6px;overflow:hidden;}
.bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
.dot{width:12px;height:12px;border-radius:50%;}
.dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
.url{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;}
.hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
.hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
.base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
.base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}
            .devtools{background:#1e1e2e;min-height:360px;display:flex;flex-direction:column;}
            .dt-tabs{display:flex;background:#2d2d3d;border-bottom:1px solid #444;}
            .dt-tab{padding:8px 16px;font-size:12px;color:#888;cursor:pointer;font-family:monospace;}
            .dt-tab.active{color:#4fc3f7;border-bottom:2px solid #4fc3f7;}
            .dt-content{flex:1;padding:16px;display:flex;gap:12px;}
            .req-panel,.res-panel{flex:1;display:flex;flex-direction:column;gap:8px;}
            .panel-title{font-size:11px;color:#888;font-family:monospace;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;}
            .http-block{background:#111;border:1px solid #333;border-radius:6px;padding:12px;font-family:monospace;font-size:12px;color:#e0e0e0;line-height:1.6;}
            .http-method{color:#f9a825;font-weight:700;}
            .http-header{color:#80cbc4;}
            .http-key{color:#f48fb1;}
            .http-val{color:#a5d6a7;}
            .editable{background:#0d1117;border:1px solid #00ff9c;border-radius:4px;padding:8px;font-family:monospace;font-size:12px;color:#00ff9c;width:100%;outline:none;resize:none;}
            .send-btn{background:#00897b;color:white;border:none;border-radius:4px;padding:7px 16px;font-size:12px;cursor:pointer;font-weight:600;font-family:monospace;align-self:flex-start;}
            .send-btn:hover{background:#00695c;}
            .response-block{background:#111;border:1px solid #333;border-radius:6px;padding:12px;font-family:monospace;font-size:12px;color:#e0e0e0;line-height:1.6;min-height:100px;}
            .status-ok{color:#66bb6a;font-weight:700;}
            .status-err{color:#ef5350;font-weight:700;}
            .highlight{background:rgba(0,255,156,0.1);border-radius:2px;padding:0 2px;}
            </style>
            <div class="wrap">
              <div class="screen">
                <div class="inner">
                  <div class="bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url">🔧 DevTools — Network — auth.target.local/api/profile</div>
                  </div>
                  <div class="devtools">
                    <div class="dt-tabs">
                      <div class="dt-tab active">📡 Network</div>
                      <div class="dt-tab">🔍 Elements</div>
                      <div class="dt-tab">💻 Console</div>
                      <div class="dt-tab">📦 Storage</div>
                    </div>
                    <div class="dt-content">
                      <div class="req-panel">
                        <div class="panel-title">REQUEST — bewerk de role parameter:</div>
                        <div class="http-block">
                          <span class="http-method">POST</span> /api/profile HTTP/1.1<br>
                          <span class="http-header">Host:</span> auth.target.local<br>
                          <span class="http-header">Content-Type:</span> application/json<br>
                          <span class="http-header">Cookie:</span> session=abc123<br>
                          <br>
                          {<br>
                          &nbsp;&nbsp;<span class="http-key">"username"</span>: <span class="http-val">"guest"</span>,<br>
                          &nbsp;&nbsp;<span class="http-key">"role"</span>: <textarea class="editable" id="roleInput" rows="1">user</textarea><br>
                          }
                        </div>
                        <button class="send-btn" onclick="sendRequest()">▶ Send Request</button>
                      </div>
                      <div class="res-panel">
                        <div class="panel-title">RESPONSE:</div>
                        <div class="response-block" id="responseBlock">
                          <span style="color:#666;">— Nog geen verzoek verstuurd —</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>
            <script>
            function sendRequest() {
                const role = document.getElementById('roleInput').value.trim().toLowerCase();
                const resp = document.getElementById('responseBlock');
                if (role === 'admin') {
                    resp.innerHTML = '<span class="status-ok">200 OK</span> — 38ms<br><br>{<br>&nbsp;&nbsp;"status": "updated",<br>&nbsp;&nbsp;"username": "guest",<br>&nbsp;&nbsp;<span class="highlight">"role": "admin"</span>,<br>&nbsp;&nbsp;"message": "Profiel bijgewerkt"<br>}<br><br><span style="color:#66bb6a;">✅ Server accepteerde rolwijziging zonder verificatie!</span>';
                    setTimeout(() => {
                        window.parent.location.href = window.parent.location.href.split('?')[0] + '?priv2_submit=1';
                    }, 2000);
                } else if (role === '') {
                    resp.innerHTML = '<span class="status-err">400 Bad Request</span><br><br>{"error": "role mag niet leeg zijn"}';
                } else {
                    resp.innerHTML = '<span class="status-ok">200 OK</span> — 22ms<br><br>{<br>&nbsp;&nbsp;"status": "updated",<br>&nbsp;&nbsp;"username": "guest",<br>&nbsp;&nbsp;"role": "' + role + '",<br>&nbsp;&nbsp;"message": "Profiel bijgewerkt"<br>}<br><br><span style="color:#888;">Geen admin rechten verkregen.</span>';
                }
            }
            </script>
            """, height=520)
        hint_widget(user, "privesc", lvl)

    elif lvl == 3:
        if st.query_params.get("priv3_submit") == "1":
            st.query_params.clear()
            fake_progress("BACKDOOR INSTALLEREN")
            give_flag(user, "privesc", "ZIF VH")
            typewriter_terminal([
                "[+] Admin token opgeslagen",
                "[+] Backdoor geïnstalleerd",
                "[✓] PERMANENTE TOEGANG VERKREGEN"
            ])
            st.success("🏴 FLAG BEHAALD: **ZIF VH**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html("""
            <style>
            *{box-sizing:border-box;margin:0;padding:0;}
body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
.wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
.screen{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
.screen::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
.inner{border-radius:6px;overflow:hidden;}
.bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
.dot{width:12px;height:12px;border-radius:50%;}
.dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
.url{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;}
.hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
.hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
.base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
.base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}
            .terminal{background:#0d1117;min-height:360px;padding:0;display:flex;flex-direction:column;}
            .term-bar{background:#1e1e2e;padding:8px 14px;display:flex;align-items:center;gap:8px;border-bottom:1px solid #333;}
            .term-bar span{font-size:12px;color:#888;font-family:monospace;}
            .term-output{flex:1;padding:16px;font-family:monospace;font-size:13px;line-height:1.7;color:#00ff9c;overflow-y:auto;min-height:260px;}
            .term-input-row{display:flex;align-items:center;padding:8px 16px;border-top:1px solid #222;gap:6px;}
            .term-prompt{color:#00ff9c;font-family:monospace;font-size:13px;white-space:nowrap;}
            .term-input{flex:1;background:transparent;border:none;outline:none;color:#00ff9c;font-family:monospace;font-size:13px;caret-color:#00ff9c;}
            .dim{color:#666;}
            .bright{color:#fff;}
            .yellow{color:#f9a825;}
            .green{color:#66bb6a;}
            .red{color:#ef5350;}
            </style>
            <div class="wrap">
              <div class="screen">
                <div class="inner">
                  <div class="bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url">root@auth.target.local:~# — SSH Session</div>
                  </div>
                  <div class="terminal">
                    <div class="term-bar"><span>bash — root@auth.target.local</span></div>
                    <div class="term-output" id="output">
<span class="dim">Last login: Mon Jan 13 09:14:22 2025 from 192.168.1.42</span><br>
<span class="yellow">root@auth:~#</span> whoami<br>
<span class="bright">root</span><br>
<span class="yellow">root@auth:~#</span> cat /etc/passwd | grep admin<br>
<span class="bright">admin:x:1001:1001::/home/admin:/bin/bash</span><br>
<span class="yellow">root@auth:~#</span> <span class="dim">Typ een commando om toegang te persisteren...</span><br>
                    </div>
                    <div class="term-input-row">
                      <span class="term-prompt">root@auth:~#</span>
                      <input class="term-input" id="termInput" type="text" placeholder="commando..." onkeydown="if(event.key==='Enter')runCmd()">
                    </div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>
            <script>
            const validCmds = ['backdoor', 'install backdoor', 'persist', 'crontab', 'ssh-keygen', 'echo >> authorized_keys', 'netcat', 'nc -lvp', 'chmod +s /bin/bash'];
            function runCmd() {
                const inp = document.getElementById('termInput');
                const out = document.getElementById('output');
                const cmd = inp.value.trim();
                inp.value = '';
                const isValid = validCmds.some(v => cmd.toLowerCase().includes(v.split(' ')[0]));
                out.innerHTML += '<span class="yellow">root@auth:~#</span> ' + cmd + '<br>';
                if (cmd === '') return;
                if (cmd.toLowerCase() === 'ls') {
                    out.innerHTML += '<span class="bright">backdoor.sh &nbsp; config.conf &nbsp; logs/ &nbsp; .ssh/</span><br>';
                } else if (cmd.toLowerCase() === 'whoami') {
                    out.innerHTML += '<span class="bright">root</span><br>';
                } else if (cmd.toLowerCase().includes('cat')) {
                    out.innerHTML += '<span class="bright">admin:x:1001:1001::/home/admin:/bin/bash</span><br>';
                } else if (cmd.toLowerCase().includes('help')) {
                    out.innerHTML += '<span class="dim">Suggesties: backdoor.sh, crontab, ssh-keygen, netcat...</span><br>';
                } else if (isValid || cmd.toLowerCase().includes('backdoor') || cmd.toLowerCase().includes('persist') || cmd.toLowerCase().includes('cron') || cmd.toLowerCase().includes('authorized') || cmd.toLowerCase().includes('bash -i')) {
                    out.innerHTML += '<span class="green">[+] Commando uitgevoerd...</span><br>';
                    out.innerHTML += '<span class="green">[+] Persistente toegang geïnstalleerd</span><br>';
                    out.innerHTML += '<span class="green">[✓] BACKDOOR ACTIEF — verbinding blijft behouden na reboot</span><br>';
                    out.scrollTop = out.scrollHeight;
                    setTimeout(() => {
                        window.parent.location.href = window.parent.location.href.split('?')[0] + '?priv3_submit=1';
                    }, 2000);
                } else {
                    out.innerHTML += '<span class="dim">bash: ' + cmd + ': command executed</span><br>';
                }
                out.scrollTop = out.scrollHeight;
            }
            </script>
            """, height=520)
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
