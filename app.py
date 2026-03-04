import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import hashlib
from datetime import datetime

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("Escape Room", layout="wide")
# ==========================================================
import streamlit as st
import sqlite3
import hashlib
import time
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("HET WITTE HUIS", layout="wide", initial_sidebar_state="expanded")

# ==========================================================
# GLOBAL STYLES + MATRIX RAIN + SOUNDS
# ==========================================================
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
            90% { opacity:0.3; } 92% { opacity:0.6; }
            94% { opacity:0.1; } 95% { opacity:0.8; }
            96% { opacity:0.2; } 97% { opacity:1; }
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

components.html("""
<canvas id="matrix" style="position:fixed;top:0;left:0;width:100%;height:100%;opacity:0.06;pointer-events:none;z-index:0;"></canvas>
<script>
const c=document.getElementById('matrix'),ctx=c.getContext('2d');
c.width=window.innerWidth; c.height=window.innerHeight;
const cols=Math.floor(c.width/16), drops=Array(cols).fill(1);
const chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()アイウエオカキクケコ';
function dm(){
    ctx.fillStyle='rgba(2,4,9,0.05)'; ctx.fillRect(0,0,c.width,c.height);
    ctx.fillStyle='#00ff9c'; ctx.font='14px Share Tech Mono';
    drops.forEach((y,i)=>{
        const ch=chars[Math.floor(Math.random()*chars.length)];
        ctx.fillText(ch,i*16,y*16);
        if(y*16>c.height&&Math.random()>0.975) drops[i]=0;
        drops[i]++;
    });
}
setInterval(dm,40);

const AC=window.AudioContext||window.webkitAudioContext;
function playClick(){try{const ac=new AC(),o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.type='square';o.frequency.setValueAtTime(800,ac.currentTime);o.frequency.exponentialRampToValueAtTime(200,ac.currentTime+0.03);g.gain.setValueAtTime(0.05,ac.currentTime);g.gain.exponentialRampToValueAtTime(0.001,ac.currentTime+0.04);o.start();o.stop(ac.currentTime+0.04);}catch(e){}}
function playSuccess(){try{const ac=new AC();[440,554,660,880].forEach((f,i)=>{const o=ac.createOscillator(),g=ac.createGain();o.connect(g);g.connect(ac.destination);o.frequency.value=f;g.gain.setValueAtTime(0.08,ac.currentTime+i*0.1);g.gain.exponentialRampToValueAtTime(0.001,ac.currentTime+i*0.1+0.15);o.start(ac.currentTime+i*0.1);o.stop(ac.currentTime+i*0.1+0.2);});}catch(e){}}
document.addEventListener('keydown',playClick);
window.playSuccess=playSuccess;
</script>
""", height=0)

# ==========================================================
# DATABASE
# ==========================================================
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS progress (username TEXT, room TEXT, level INTEGER, PRIMARY KEY(username,room))")
    c.execute("CREATE TABLE IF NOT EXISTS flags (username TEXT, room TEXT, flag TEXT, time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS hints (username TEXT, room TEXT, hint_num INTEGER, PRIMARY KEY(username,room,hint_num))")
    for u in [("leerling","epsteinfiles","student"),("teacher","admin123","teacher")]:
        c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)",(u[0],hash_pw(u[1]),u[2]))
    conn.commit(); conn.close()

init_db()

# ==========================================================
# HINTS
# ==========================================================
HINTS = {
    "sql": [
        "💡 Er is een aanval waarbij je database-commando's in een invoerveld stopt om de server te manipuleren. Wat is de naam?",
        "💡 Maak de WHERE-clausule altijd WAAR door dit als gebruikersnaam te typen: ' OR '1'='1",
        "💡 UNION SELECT combineert twee queries. Probeer: ' UNION SELECT username, password, role FROM staff--",
    ],
    "xss": [
        "💡 Er is een aanval waarbij je JavaScript-code in een website stopt die andere gebruikers raken. Wat is de afkorting?",
        "💡 Gebruik de HTML-tag die JavaScript uitvoert. Typ exact: <script>alert('xss')</script>",
        "💡 Zelfde techniek als stap 2, maar nu in het reactieveld zodat het opgeslagen wordt in de database.",
    ],
    "privesc": [
        "💡 Je wilt meer rechten dan je hebt. Welk type aanval noemen we het verhogen van bevoegdheden?",
        "💡 Je ziet een 'role' veld in het HTTP-verzoek. Wat is de hoogste rol die een gebruiker kan hebben?",
        "💡 Typ het woord 'admin' als waarde voor het role-veld en stuur het verzoek opnieuw.",
    ],
    "crypto": [
        "💡 Julius Caesar gebruikte dit systeem om berichten te versleutelen door letters te verschuiven.",
        "💡 Bij ROT13 wordt elke letter 13 posities verschoven. G→T, V→I, etc.",
        "💡 Decodeer alle drie de vlaggen met ROT13 en combineer ze tot het formaat: EXAMENKLAS[JAAR]",
    ],
}

# ==========================================================
# LAPTOP COMMON CSS
# ==========================================================
LC = """*{box-sizing:border-box;margin:0;padding:0;}
body{background:#020409;font-family:'Segoe UI',Arial,sans-serif;display:flex;flex-direction:column;align-items:center;padding:16px;}
.wrap{display:flex;flex-direction:column;align-items:center;width:100%;}
.screen{background:#1a1a2e;border:4px solid #444;border-bottom:8px solid #333;border-radius:16px 16px 0 0;width:100%;padding:14px;box-shadow:0 0 40px rgba(0,0,0,0.9);position:relative;}
.screen::before{content:'';position:absolute;top:8px;left:50%;transform:translateX(-50%);width:10px;height:10px;background:#333;border-radius:50%;}
.inner{border-radius:6px;overflow:hidden;}
.bar{background:#e0e0e0;padding:10px 14px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #ccc;}
.dot{width:12px;height:12px;border-radius:50%;}
.dot.r{background:#ff5f57;}.dot.y{background:#febc2e;}.dot.g{background:#28c840;}
.url{flex:1;background:white;border:1px solid #ccc;border-radius:5px;padding:4px 12px;font-size:12px;color:#666;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.hinge{width:100%;height:10px;background:linear-gradient(180deg,#1a1a1a,#2d2d2d);position:relative;}
.hinge::after{content:'';position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:50px;height:5px;background:#111;border-radius:3px;}
.base{background:linear-gradient(180deg,#2d2d2d,#1a1a1a);width:110%;height:22px;border-radius:0 0 14px 14px;box-shadow:0 6px 20px rgba(0,0,0,0.6);position:relative;}
.base::after{content:'';position:absolute;bottom:5px;left:50%;transform:translateX(-50%);width:60px;height:4px;background:#111;border-radius:2px;}"""

# ==========================================================
# HELPERS
# ==========================================================
def auth(u, p):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (u, hash_pw(p)))
    r = c.fetchone(); conn.close()
    return r[0] if r else None

def get_level(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT level FROM progress WHERE username=? AND room=?", (user, room))
    r = c.fetchone(); conn.close()
    return r[0] if r else 1

def set_level(user, room, level):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("INSERT INTO progress VALUES(?,?,?) ON CONFLICT(username,room) DO UPDATE SET level=?", (user,room,level,level))
    conn.commit(); conn.close()

def give_flag(user, room, flag):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM flags WHERE username=? AND room=?", (user, room))
    if not c.fetchone():
        c.execute("INSERT INTO flags VALUES(?,?,?,?)", (user,room,flag,datetime.now().isoformat()))
    conn.commit(); conn.close()

def has_completed(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT 1 FROM flags WHERE username=? AND room=?", (user, room))
    r = c.fetchone(); conn.close()
    return r is not None

def get_hints_used(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT hint_num FROM hints WHERE username=? AND room=? ORDER BY hint_num", (user, room))
    r = [x[0] for x in c.fetchall()]; conn.close()
    return r

def use_hint(user, room, hint_num):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO hints VALUES(?,?,?)", (user, room, hint_num))
    conn.commit(); conn.close()

def typewriter_terminal(lines):
    for line in lines:
        st.code(line, language=None)
        time.sleep(0.08)

def fake_progress(label="BYPASSING FIREWALL"):
    bar = st.progress(0, text=f"⚡ {label}...")
    for i in range(0, 101, 5):
        bar.progress(i, text=f"⚡ {label}... {i}%")
        time.sleep(0.03)
    bar.empty()

def hint_widget(user, room, current_level):
    hints = HINTS.get(room, [])
    used = get_hints_used(user, room)
    next_hint = len(used)
    with st.expander(f"🔍 HINTS ({next_hint}/{len(hints)} gebruikt)"):
        for i in used:
            st.info(hints[i])
        if next_hint < len(hints):
            if st.button(f"📡 HINT {next_hint + 1} OPVRAGEN", key=f"hint_{room}_{next_hint}"):
                use_hint(user, room, next_hint); st.rerun()
        else:
            st.caption("Alle hints gebruikt.")

def ctx_box(title, story, opdracht):
    """Context box boven elke laptop — verhaal + concrete opdracht"""
    components.html(f"""
    <div style="background:#050e08;border:1px solid rgba(0,255,156,0.35);border-radius:10px;padding:18px 22px;margin-bottom:16px;font-family:'Share Tech Mono',monospace;">
      <div style="color:#f9a825;font-size:11px;letter-spacing:3px;margin-bottom:8px;text-transform:uppercase;">📋 {title}</div>
      <div style="color:rgba(0,255,156,0.85);font-size:13px;line-height:1.7;margin-bottom:12px;">{story}</div>
      <div style="background:#0d1f10;border:1px solid rgba(0,255,156,0.25);border-radius:6px;padding:10px 14px;">
        <span style="color:#00ff9c;font-size:11px;letter-spacing:1px;">🎯 JOUW OPDRACHT: </span>
        <span style="color:#00ffcc;font-size:12px;">{opdracht}</span>
      </div>
    </div>""", height=180)

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
    <div style="text-align:center;padding:2rem 0 1rem;">
      <span class="glitch-t" data-text="HET WITTE HUIS">HET WITTE HUIS</span>
      <p style="letter-spacing:6px;color:rgba(0,255,156,0.5);font-size:11px;margin-top:12px;font-family:'Share Tech Mono',monospace;">
        CYBER ESCAPE ROOM &mdash; ANOUK · MARWA · FENNA · NOURA
      </p>
    </div>
    <style>
    @keyframes gt{0%,90%,100%{text-shadow:0 0 15px rgba(0,255,156,0.6);transform:translate(0);clip-path:none;}
    91%{text-shadow:-4px 0 #ff003c,4px 0 #00ffff;transform:translate(-3px,0);clip-path:inset(5% 0 55% 0);}
    92%{text-shadow:4px 0 #ff003c,-4px 0 #00ffff;transform:translate(3px,0);clip-path:inset(58% 0 3% 0);}
    93%{text-shadow:-2px 0 #ff003c,2px 0 #00ffff;transform:translate(-1px,0);clip-path:none;}94%{text-shadow:0 0 15px rgba(0,255,156,0.6);transform:translate(0);}}
    @keyframes flicker{0%,89%,91%,93%,100%{opacity:1;}90%{opacity:0.3;}92%{opacity:0.6;}94%{opacity:0.1;}95%{opacity:0.8;}96%{opacity:0.2;}97%{opacity:1;}}
    .glitch-t{font-family:'Orbitron',monospace!important;font-weight:900;font-size:clamp(22px,3.5vw,52px);color:#00ff9c;letter-spacing:6px;animation:gt 5s infinite,flicker 3s infinite;position:relative;display:inline-block;}
    </style>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**`> IDENTIFICEER JEZELF`**")
        u = st.text_input("GEBRUIKERSNAAM", placeholder="geef je groepnaam")
        p = st.text_input("WACHTWOORD", type="password", placeholder="••••••••")
        if st.button("▶ TOEGANG AANVRAGEN", use_container_width=True):
            role = auth(u, p)
        if role:
            st.session_state.user = u
            st.session_state.role = role
            role = role; st.rerun()
        else:
            st.error(" TOEGANG GEWEIGERD — Ongeldige credentials")
    st.stop()

# ==========================================================
# TEACHER pagina
# ==========================================================
if st.session_state.role == "teacher":
    st.title("CONTROL PANEL")
    conn = sqlite3.connect("platform.db")

    st.subheader("VOORTGANG PER STUDENT")
    progress_data = conn.execute("""
        SELECT p.username, p.room, p.level,
               (SELECT COUNT(*) FROM hints h WHERE h.username=p.username AND h.room=p.room) hints_used
        FROM progress p ORDER BY p.username, p.room""").fetchall()
    if progress_data:
        st.table({"Student":[r[0] for r in progress_data],"Room":[r[1].upper() for r in progress_data],
                  "Level":[r[2] for r in progress_data],"Hints":[r[3] for r in progress_data]})
    else: st.info("Nog geen voortgang.")

    st.subheader("BEHAALDE FLAGS")
    flags = conn.execute("SELECT * FROM flags ORDER BY time DESC").fetchall()
    if flags:
        st.table({"Student":[r[0] for r in flags],"Room":[r[1].upper() for r in flags],
                  "Flag":[r[2] for r in flags],"Tijd":[r[3][:19] for r in flags]})
    else: st.info("Nog geen flags behaald.")
    conn.close()

    st.subheader("RESET STUDENT")
    all_students = [r[0] for r in sqlite3.connect("platform.db").execute(
        "SELECT DISTINCT username FROM users WHERE role='student'").fetchall()]
    rst = st.selectbox("Selecteer student", all_students)
    if st.button("🗑 RESET GESELECTEERDE STUDENT"):
        c2 = sqlite3.connect("platform.db"); cur = c2.cursor()
        cur.execute("DELETE FROM progress WHERE username=?",(rst,))
        cur.execute("DELETE FROM flags WHERE username=?",(rst,))
        cur.execute("DELETE FROM hints WHERE username=?",(rst,))
        c2.commit(); c2.close(); st.success(f"✅ {rst} gereset!"); st.rerun()

    st.markdown("---")
    if st.button("LOGOUT"): st.session_state.clear(); st.rerun()
    st.stop()

# ==========================================================
# leerlingen pagina
# ==========================================================
user = st.session_state.user

with st.sidebar:
    st.markdown(f"### 🕶 {user.upper()}")
    rooms_done_sb = sum(1 for r in ["sql","xss","privesc","crypto"] if has_completed(user,r))
    st.markdown(f"**MISSIES:** {rooms_done_sb}/4")
    st.markdown("---")
    if st.button("LOGOUT", key="sidebar_logout", use_container_width=True):
        st.session_state.clear(); st.rerun()
    if st.button("🗑 RESET PROGRESSIE", key="sidebar_reset", use_container_width=True):
        st.session_state["confirm_reset"] = True
    if st.session_state.get("confirm_reset"):
        st.warning("Zeker weten?")
        if st.button("✅ JA", key="sb_yes", use_container_width=True):
            conn = sqlite3.connect("platform.db"); c = conn.cursor()
            c.execute("DELETE FROM progress WHERE username=?",(user,))
            c.execute("DELETE FROM flags WHERE username=?",(user,))
            c.execute("DELETE FROM hints WHERE username=?",(user,))
            conn.commit(); conn.close()
            st.session_state.pop("confirm_reset",None); st.rerun()
        if st.button("❌ NEE", key="sb_no", use_container_width=True):
            st.session_state.pop("confirm_reset",None); st.rerun()

rooms_done = sum(1 for r in ["sql","xss","privesc","crypto"] if has_completed(user,r))
col_title, col_status, col_logout_btn = st.columns([3, 0.7, 0.7])
with col_title:
    st.title(f"HET WITTE HUIS")
with col_status:
    st.metric("MISSIES", f"{rooms_done}/4")
with col_logout_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("UITLOGGEN", key="top_logout", use_container_width=True):
        st.session_state.clear(); st.rerun()

st.markdown("---")
tabs = st.tabs(["DE RECEPTIE", "DE VERGADERRUIMTE", "DE BEVEILIGDE KAMER", "TRUMP'S SLAAPKAMER"])

# ==========================================================
# kamer 1 — DE RECEPTIE (SQL INJECTION)
# ==========================================================
with tabs[0]:
    st.header("DE RECEPTIE")
    lvl = get_level(user, "sql")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        ctx_box("MISSIE BRIEFING — DE RECEPTIE",
            "Jullie zijn binnengekomen in het witte huis. Je partner in crime heeft de receptioniste weg kunnen lokken. Nu aan jou de taak om achter de balie te kruipen en proberen om het systeem binnen te komen.Er is echter een kwetsbaarheid in de database.",
            "Noem het type aanval waarbij je database-commando's in een invoerveld injecteert om de login te omzeilen.")
        st.markdown("**Wat is de naam van de aanval waarbij je kwaadaardige SQL-code in een invoerveld typt?**")
        cmd = st.text_input("root@receptie:~#", key="sql1", placeholder="typ de naam van de aanval...")
        if st.button("BEVESTIG AANVAL", key="sql1_btn"):
            if cmd.lower().strip() == "sql injectie":
                fake_progress("KWETSBAARHEID ANALYSEREN"); set_level(user, "sql", 2)
                typewriter_terminal(["[+] Kwetsbaarheid geïdentificeerd: SQL INJECTION",
                    "[+] Login module accepteert ongefilterde input",
                    "[!] Ga naar het login-portaal en omzeil de authenticatie..."])
                st.rerun()
            else: st.error("NIET CORRECT. Hint: SQL staat in de naam.")
        hint_widget(user, "sql", lvl)

    elif lvl == 2:
        ctx_box("SQL INJECTION — LOGIN PORTAAL HACKEN",
            "Het login-portaal van het Witte Huis is kwetsbaar voor SQL injection. De database bouwt een query zoals: SELECT * FROM users WHERE username='[JOUW INPUT]' AND password='...'. Als jij een slimme payload typt als gebruikersnaam, maak je de WHERE-clausule altijd WAAR — en log je in als admin zonder wachtwoord!",
            "Typ ' OR '1'='1 als gebruikersnaam (met die exacte aanhalingstekens) en druk op Inloggen.")

        if st.query_params.get("sql2_submit") == "1":
            st.query_params.clear(); set_level(user, "sql", 3); st.rerun()

        col_l, col_m, col_r = st.columns([1, 2.5, 1])
        with col_m:
            components.html(f"""<style>{LC}
.lp{{padding:24px 40px;display:flex;flex-direction:column;align-items:center;background:white;}}
.logo{{font-size:22px;font-weight:700;color:#1a1a2e;margin-bottom:2px;letter-spacing:-1px;}}
.logo span{{color:#c0392b;}}
.tag{{font-size:11px;color:#999;margin-bottom:22px;text-align:center;}}
.card{{background:white;border:1px solid #e0e0e0;border-radius:10px;padding:28px 32px;width:100%;max-width:340px;box-shadow:0 4px 20px rgba(0,0,0,0.1);transition:all .3s;}}
.card h3{{font-size:16px;color:#222;margin-bottom:18px;font-weight:600;}}
.fld{{margin-bottom:14px;}}
.fld label{{display:block;font-size:11px;color:#666;margin-bottom:4px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;}}
.fld .inp-wrap{{position:relative;display:flex;align-items:center;}}
.fld input{{width:100%;border:1.5px solid #ddd;border-radius:6px;padding:10px 12px;font-size:13px;color:#333;background:#fafafa;outline:none;transition:all .2s;}}
.fld input:focus{{border-color:#1a1a2e;background:white;box-shadow:0 0 0 3px rgba(26,26,46,0.08);}}
.eye{{position:absolute;right:10px;cursor:pointer;font-size:14px;color:#999;user-select:none;}}
.eye:hover{{color:#333;}}
.msg{{border-radius:6px;padding:10px 12px;font-size:12px;margin-bottom:14px;display:none;font-weight:500;}}
.msg.error{{background:#fff3cd;border:1px solid #ffc107;color:#856404;}}
.msg.success{{background:#d4edda;border:1px solid #28a745;color:#155724;}}
.msg.inject{{background:#f8d7da;border:2px solid #dc3545;color:#721c24;font-weight:700;}}
.lbtn{{width:100%;background:#1a1a2e;color:white;border:none;border-radius:6px;padding:11px;font-size:14px;font-weight:600;cursor:pointer;margin-top:4px;transition:all .2s;letter-spacing:1px;}}
.lbtn:hover{{background:#2c2c4e;transform:translateY(-1px);box-shadow:0 4px 12px rgba(26,26,46,0.3);}}
.fl{{display:flex;justify-content:space-between;margin-top:12px;}}
.fl a{{font-size:11px;color:#4a90e2;text-decoration:none;}}
.fl a:hover{{text-decoration:underline;}}
.sqlt{{border:1px solid #e74c3c;background:#fff5f5;font-family:monospace;color:#c0392b;}}
.fm{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,.5);z-index:100;align-items:center;justify-content:center;}}
.mb{{background:white;border-radius:10px;padding:24px;max-width:280px;width:90%;box-shadow:0 10px 40px rgba(0,0,0,.3);}}
.mb h4{{color:#333;margin-bottom:10px;font-size:14px;}}
.mb p{{font-size:12px;color:#666;margin-bottom:14px;}}
.mc{{background:#e74c3c;color:white;border:none;border-radius:4px;padding:7px 14px;cursor:pointer;font-size:12px;}}
@keyframes shake{{0%,100%{{transform:translateX(0)}}25%{{transform:translateX(-8px)}}75%{{transform:translateX(8px)}}}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url"> secure.whitehouse.gov/login</div></div>
  <div class="lp">
    <div class="logo">White<span>House</span></div>
    <div class="tag">Beveiligd medewerkers portaal — Bevoegd personeel only</div>
    <div class="card" id="loginCard">
      <h3> Inloggen</h3>
      <div class="msg" id="msg"></div>
      <div class="fld">
        <label>Gebruikersnaam</label>
        <div class="inp-wrap">
          <input type="text" id="uname" placeholder="gebruiker@whitehouse.gov" oninput="lc(this)">
        </div>
      </div>
      <div class="fld">
        <label>Wachtwoord</label>
        <div class="inp-wrap">
          <input type="password" id="pw" id="pw" placeholder="••••••••">
          <span class="eye" onclick="togglePw()" id="eyeBtn">👁</span>
        </div>
      </div>
      <button class="lbtn" onclick="tryLogin()">Inloggen →</button>
      <div class="fl">
        <a href="javascript:void(0)" onclick="showForgot()">Wachtwoord vergeten?</a>
        <a href="javascript:void(0)" onclick="showHelp()">Hulp nodig?</a>
      </div>
    </div>
  </div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<div class="fm" id="forgotModal">
  <div class="mb">
    <h4>Wachtwoord vergeten?</h4>
    <p>Neem contact op via it-support@whitehouse.gov of bel intern 4242. Openingstijden: ma-vr 08:00-17:00.</p>
    <button class="mc" onclick="document.getElementById('forgotModal').style.display='none'">Sluiten</button>
  </div>
</div>
<script>
function togglePw(){{
  const inp=document.getElementById('pw');
  const eye=document.getElementById('eyeBtn');
  if(inp.type==='password'){{inp.type='text';eye.textContent='🙈';}}
  else{{inp.type='password';eye.textContent='👁';}}
}}
function lc(inp){{
  const v=inp.value.toLowerCase();
  if(v.includes("' or")||v.includes("'or")||v.includes("1=1")){{
    inp.classList.add('sqlt');
  }} else {{inp.classList.remove('sqlt');}}
}}
function tryLogin(){{
  const u=document.getElementById('uname').value;
  const p=document.getElementById('pw').value;
  const msg=document.getElementById('msg');
  const card=document.getElementById('loginCard');
  const isInj=u.toLowerCase().includes("' or")||u.toLowerCase().includes("'or")||u.toLowerCase().includes("1=1");
  if(isInj){{
    card.style.borderColor='#dc3545';
    msg.className='msg inject';msg.style.display='block';
    msg.innerHTML='🚨 SQL INJECTION GESLAAGD!<br>Query: SELECT * FROM users WHERE username=\'<b>' + u + '</b>\'...<br><small>WHERE is altijd TRUE — ingelogd als: president@whitehouse.gov</small>';
    setTimeout(()=>{{window.parent.location.href=window.parent.location.href.split('?')[0]+'?sql2_submit=1';}},2500);
  }} else if(u===''||p===''){{
    msg.className='msg error';msg.style.display='block';msg.innerHTML='⚠️ Vul alle velden in.';
  }} else {{
    msg.className='msg error';msg.style.display='block';msg.innerHTML='⛔ Ongeldige inloggegevens.';
    card.style.animation='shake 0.3s ease';
    setTimeout(()=>card.style.animation='',300);
  }}
}}
function showForgot(){{document.getElementById('forgotModal').style.display='flex';}}
function showHelp(){{alert('IT Support: it-support@whitehouse.gov\\nTel: +1 202 555 1234\\nOpeningstijden: ma-vr 08:00-17:00 EST');}}
document.addEventListener('keydown',e=>{{if(e.key==='Enter')tryLogin();}});
document.querySelectorAll('a').forEach(a=>a.addEventListener('click',e=>e.preventDefault()));
</script>""", height=620)
        hint_widget(user, "sql", lvl)

    elif lvl == 3:
        ctx_box("UNION SELECT — GEHEIME DATA OPHALEN",
            "Je bent ingelogd als admin! Maar er is meer te halen. Het admin-portaal heeft een SQL-interface waarmee je queries kunt uitvoeren op de medewerkerdatabase. Met een UNION SELECT kun je twee queries combineren en zo verborgen data ophalen — zoals het wachtwoord van de president.",
            "Typ in de SQL-console: ' UNION SELECT username, password, role FROM staff-- en druk op RUN.")

        if st.query_params.get("sql3_submit") == "1":
            st.query_params.clear()
            fake_progress("DATABASE DUMPEN"); give_flag(user, "sql", "GV 71")
            typewriter_terminal(["[+] UNION SELECT query uitgevoerd",
                "[+] Geheime rij toegevoegd aan resultaten:",
                "","  ⚠ UNION | president | WhiteHouse2025! | ADMIN",
                "","[✓] DATABASE GEDUMPT — flag: GV 71"])
            st.success("🏴 FLAG BEHAALD: **GV 71**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html(f"""<style>{LC}
.tnav{{background:#1a3a6e;padding:9px 16px;display:flex;align-items:center;justify-content:space-between;}}
.logo{{font-size:14px;font-weight:700;color:white;}}
.logo span{{color:#ffd700;}}
.ui{{display:flex;align-items:center;gap:6px;font-size:11px;color:white;}}
.av{{width:26px;height:26px;border-radius:50%;background:#ffd700;color:#1a1a2e;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:11px;}}
.dash{{display:flex;}}
.sb{{width:150px;background:#fff;border-right:1px solid #e0e0e0;padding:8px 0;flex-shrink:0;}}
.si{{padding:7px 12px;font-size:11px;color:#555;cursor:pointer;display:flex;align-items:center;gap:5px;}}
.si.active{{background:#e8f0fe;color:#1a3a6e;font-weight:700;border-left:3px solid #1a3a6e;}}
.si:hover{{background:#f5f5f5;}}
.cont{{flex:1;padding:12px;display:flex;flex-direction:column;gap:8px;background:#f5f6fa;}}
.cont h2{{font-size:12px;color:#1a3a6e;font-weight:700;}}
.sqlcon{{background:#1e1e2e;border-radius:8px;overflow:hidden;border:1px solid #333;}}
.sqlh{{background:#2d2d3d;padding:7px 12px;display:flex;align-items:center;gap:6px;border-bottom:1px solid #444;font-size:11px;color:#888;font-family:monospace;}}
.dbn{{color:#4fc3f7!important;font-weight:700;}}
.sqlr{{display:flex;align-items:center;padding:9px 12px;gap:6px;}}
.sqlp{{color:#00ff9c;font-family:monospace;font-size:12px;white-space:nowrap;}}
.sqli{{flex:1;background:transparent;border:none;outline:none;color:#e0e0e0;font-family:monospace;font-size:12px;caret-color:#00ff9c;}}
.sqlb{{background:#1a3a6e;color:white;border:none;border-radius:4px;padding:4px 12px;font-size:11px;cursor:pointer;font-weight:700;}}
.sqlb:hover{{background:#0d2347;}}
.res{{padding:0 12px 12px;}}
.ri{{font-size:11px;color:#888;padding:4px 0 6px;font-family:monospace;}}
.ri.ok{{color:#28a745;font-weight:700;}}.ri.err{{color:#e74c3c;}}
.dt{{width:100%;border-collapse:collapse;font-size:11px;}}
.dt th{{background:#f8f9fa;padding:6px 10px;text-align:left;border-bottom:2px solid #dee2e6;color:#555;font-weight:700;font-size:10px;text-transform:uppercase;}}
.dt td{{padding:6px 10px;border-bottom:1px solid #f0f0f0;color:#444;}}
.ir td{{color:#c0392b!important;font-weight:700;background:#fff8e1!important;}}
.badge{{display:inline-block;padding:2px 6px;border-radius:8px;font-size:9px;font-weight:700;}}
.badge.a{{background:#ffeeba;color:#856404;}}.badge.u{{background:#d4edda;color:#155724;}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url">admin.whitehouse.gov/database/staff</div></div>
  <div class="tnav"><div class="logo">White House <span>Admin</span></div><div class="ui"><div class="av">P</div><span>president</span></div></div>
  <div class="dash">
    <div class="sb">
      <div class="si active">Medewerkers</div>
      <div class="si" onclick="showMsg('Classified — geen toegang')">Geheimen</div>
      <div class="si" onclick="showMsg('Logs — geen toegang')">Audit Logs</div>
      <div class="si" onclick="showMsg('Settings — geen toegang')">⚙️ Instellingen</div>
    </div>
    <div class="cont" id="mc">
      <h2>Medewerkerdatabase — SQL Interface</h2>
      <div class="sqlcon">
        <div class="sqlh"><span>DB:</span><span class="dbn">whitehouse_db</span><span style="margin-left:auto;">TABLE: staff</span></div>
        <div class="sqlr"><span class="sqlp">sql&gt;</span><input class="sqli" id="sqlInput" type="text" value="SELECT * FROM staff" onkeydown="if(event.key==='Enter')rq()"><button class="sqlb" onclick="rq()">▶ RUN</button></div>
        <div class="res"><div class="ri" id="info">3 rijen gevonden</div>
          <table class="dt"><thead><tr><th>ID</th><th>Gebruikersnaam</th><th>E-mail</th><th>Rol</th></tr></thead>
          <tbody id="tbody">
            <tr><td>1</td><td>john.smith</td><td>j.smith@wh.gov</td><td><span class="badge u">staff</span></td></tr>
            <tr><td>2</td><td>sarah.jones</td><td>s.jones@wh.gov</td><td><span class="badge u">staff</span></td></tr>
            <tr><td>3</td><td>mike.davis</td><td>m.davis@wh.gov</td><td><span class="badge u">staff</span></td></tr>
          </tbody></table>
        </div>
      </div>
    </div>
  </div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<script>
function rq(){{const q=document.getElementById('sqlInput').value.toLowerCase(),info=document.getElementById('info'),tb=document.getElementById('tbody');
if(q.includes('union')&&q.includes('select')){{const r=document.createElement('tr');r.className='ir';r.innerHTML='<td>⚠ INJ</td><td>president</td><td>WhiteHouse2025!</td><td><span class="badge a">ADMIN</span></td>';tb.appendChild(r);info.className='ri ok';info.innerHTML='🚨 UNION SELECT — geheime rij zichtbaar!';setTimeout(()=>{{window.parent.location.href=window.parent.location.href.split('?')[0]+'?sql3_submit=1';}},2000);}}
else if(q.includes('drop')||q.includes('delete')){{info.className='ri err';info.innerHTML='⛔ Geen schrijfrechten.';}}
else if(q.includes('select')){{info.className='ri';info.innerHTML='3 rijen gevonden';tb.innerHTML='<tr><td>1</td><td>john.smith</td><td>j.smith@wh.gov</td><td><span class="badge u">staff</span></td></tr><tr><td>2</td><td>sarah.jones</td><td>s.jones@wh.gov</td><td><span class="badge u">staff</span></td></tr><tr><td>3</td><td>mike.davis</td><td>m.davis@wh.gov</td><td><span class="badge u">staff</span></td></tr>';}}
else{{info.className='ri err';info.innerHTML='⛔ SQL SYNTAX ERROR.';}}}}
function showMsg(m){{document.getElementById('mc').innerHTML='<h2>'+m+'</h2><p style="color:#999;font-size:11px;margin-top:8px;">Toegang vereist hogere machtiging.</p>';}}
</script>""", height=520)
        hint_widget(user, "sql", lvl)

# ==========================================================
# KAMER 2 — DE VERGADERRUIMTE (XSS)
# ==========================================================
with tabs[1]:
    st.header("DE VERGADERRUIMTE")
    lvl = get_level(user, "xss")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        ctx_box("MISSIE BRIEFING — DE VERGADERRUIMTE",
            "Je bent doorgedrongen tot de vergaderruimte. Drie bewakingscamera's hangen aan het plafond, beheerd via een intern webportaal. Om ongemerkt verder te gaan, moet je de bewakers afleiden door een alert te triggeren in hun beveiligingssysteem.",
            "Noem het type aanval waarbij je kwaadaardige scripts injecteert in een website die andere gebruikers raken. (Afkorting: XSS)")
        st.markdown("**Welk type aanval injecteert JavaScript in een website zodat het wordt uitgevoerd in de browser van andere gebruikers?**")
        cmd = st.text_input("root@vergaderruimte:~#", key="xss1", placeholder="typ de naam van de aanval...")
        if st.button("▶ BEVESTIG AANVAL", key="xss1_btn"):
            if "cross site scripting" in cmd.lower() or cmd.lower().strip() == "xss":
                fake_progress("AANVAL BEVESTIGEN"); set_level(user, "xss", 2)
                typewriter_terminal(["[+] Cross-Site Scripting (XSS) geïdentificeerd",
                    "[+] Camera-portaal geeft input direct terug in pagina",
                    "[!] Ga naar het portaal en trigger een alert..."])
                st.rerun()
            else: st.error("❌ Niet correct. Hint: de afkorting is XSS.")
        hint_widget(user, "xss", lvl)

    elif lvl == 2:
        ctx_box("REFLECTED XSS — BEWAKER AFLEIDEN MET ALERT",
            "Je hebt het interne camera-portaal van het Witte Huis gevonden. De zoekbalk geeft jouw input direct terug op de pagina zónder controle — dit is een Reflected XSS kwetsbaarheid. Als jij een <script> tag injecteert, voert de browser van de bewaker jouw JavaScript direct uit. Er verschijnt een alert pop-up die de bewaker afleidt!",
            "Typ precies dit in de zoekbalk en klik Zoeken: <script>alert('xss')</script>")

        if st.query_params.get("xss2_submit") == "1":
            st.query_params.clear(); fake_progress("XSS PAYLOAD INJECTEREN"); set_level(user, "xss", 3)
            typewriter_terminal(["[+] Script tag gedetecteerd in zoekveld",
                "[+] Browser van bewaker voert jouw JavaScript uit",
                "[+] ALERT POP-UP getriggerd — bewaker afgeleid!",
                "[✓] REFLECTED XSS GESLAAGD"])
            st.rerun()

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html(f"""<style>{LC}
.tb{{background:#1a3a6e;padding:10px 16px;display:flex;align-items:center;gap:10px;}}
.tl{{font-size:15px;font-weight:700;color:white;display:flex;align-items:center;gap:6px;}}
.nl{{display:flex;gap:14px;margin-left:14px;}}
.nl a{{color:rgba(255,255,255,0.7);font-size:12px;text-decoration:none;}}
.nl a:hover{{color:white;}}
.ca{{background:white;padding:18px 24px;min-height:280px;}}
.ch{{font-size:15px;font-weight:700;color:#1a3a6e;margin-bottom:3px;}}
.cs{{font-size:11px;color:#888;margin-bottom:12px;}}
.cg{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:14px;}}
.cf{{background:#111;border-radius:6px;height:56px;display:flex;align-items:center;justify-content:center;font-size:9px;color:#00ff9c;font-family:monospace;border:1px solid #333;}}
.sr{{display:flex;gap:8px;margin-bottom:12px;}}
.sb2{{flex:1;border:1.5px solid #ddd;border-radius:6px;padding:9px 13px;font-size:13px;color:#333;outline:none;}}
.sb2:focus{{border-color:#1a3a6e;}}
.sbtn{{background:#1a3a6e;color:white;border:none;border-radius:6px;padding:9px 16px;font-size:12px;cursor:pointer;font-weight:600;}}
.rbx{{border:1px solid #e0e0e0;border-radius:6px;padding:12px;background:#fafafa;min-height:46px;}}
.rl{{font-size:10px;color:#888;margin-bottom:4px;font-weight:600;text-transform:uppercase;}}
.rt{{font-size:13px;color:#333;}}
.xa{{display:none;background:#d4edda;border:1px solid #28a745;border-radius:6px;padding:10px 13px;font-size:11px;color:#155724;margin-top:10px;font-weight:700;}}
.stbar{{background:#f5f5f5;border-top:1px solid #eee;padding:5px 12px;font-size:10px;color:#999;display:flex;justify-content:space-between;}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url">🔒 internal.whitehouse.gov/security/cameras</div></div>
  <div class="tb"><div class="tl">🏛 WH Security Portal</div>
    <div class="nl"><a href="javascript:void(0)">Cameras</a><a href="javascript:void(0)">Alarmen</a><a href="javascript:void(0)">Rapporten</a></div></div>
  <div class="ca">
    <div class="ch">📹 Camera Management Systeem</div>
    <div class="cs">Zoek op locatie of cameranummer — resultaten worden direct getoond</div>
    <div class="cg"><div class="cf">CAM-01 LIVE</div><div class="cf">CAM-02 LIVE</div><div class="cf">CAM-03 LIVE</div></div>
    <div class="sr">
      <input class="sb2" id="si" type="text" placeholder="Zoek camera of locatie...">
      <button class="sbtn" onclick="ds()">🔍 Zoeken</button>
    </div>
    <div class="rbx"><div class="rl">ZOEKRESULTAAT — input direct weergegeven (kwetsbaar!):</div>
      <div class="rt" id="rt"><em style="color:#bbb;">Voer een zoekopdracht in...</em></div></div>
    <div class="xa" id="xa">🚨 ALERT getriggerd! Jouw script werd uitgevoerd in de browser van de bewaker — ze zijn afgeleid!</div>
  </div>
  <div class="stbar"><span>🟢 Systeem online — 3 camera's actief</span><span>Agent: guard01</span></div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<script>
function ds(){{
  const v=document.getElementById('si').value,r=document.getElementById('rt'),x=document.getElementById('xa');
  if(v.toLowerCase().includes('<script>')){{
    r.innerHTML=v;
    x.style.display='block';
    // Trigger real browser alert to simulate XSS
    setTimeout(()=>{{
      alert('XSS! Jouw script werd uitgevoerd!\\n\\nDe bewaker ziet dit ook — hij is nu afgeleid!');
    }},300);
    setTimeout(()=>{{
      window.parent.location.href=window.parent.location.href.split('?')[0]+'?xss2_submit=1';
    }},2800);
  }} else {{
    r.textContent=v||'(leeg)';
    x.style.display='none';
  }}
}}
document.getElementById('si').addEventListener('keydown',e=>{{if(e.key==='Enter')ds();}});
</script>""", height=500)
        hint_widget(user, "xss", lvl)

    elif lvl == 3:
        ctx_box("PERSISTENT XSS — BEWAKERS PERMANENT AFLEIDEN",
            "De alert werkte maar de bewakers zijn teruggekomen! Je moet nu een permanente XSS payload opslaan in de database van het beveiligingsrapport. Zo wordt jouw script uitgevoerd bij ELKE bewaker die het rapport opent — ze worden keer op keer afgeleid terwijl jij ongemerkt doorloopt.",
            "Typ <script>alert('bewaker afgeleid')</script> in het reactieveld van het beveiligingsrapport en klik Plaatsen.")

        if st.query_params.get("xss3_submit") == "1":
            st.query_params.clear(); fake_progress("PAYLOAD IN DATABASE OPSLAAN"); give_flag(user, "xss", "N75 ZS")
            typewriter_terminal(["[+] Payload opgeslagen in WH beveiligingsdatabase",
                "[+] Script wordt uitgevoerd bij ELKE bewaker die dit rapport opent",
                "[+] Bewakers permanent afgeleid!",
                "[✓] PERSISTENT XSS GESLAAGD — flag: N75 ZS"])
            st.success("🏴 FLAG BEHAALD: **N75 ZS**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html(f"""<style>{LC}
.tb{{background:#1a3a6e;padding:10px 16px;display:flex;align-items:center;justify-content:space-between;}}
.tl{{font-size:14px;font-weight:700;color:white;display:flex;align-items:center;gap:6px;}}
.tu{{font-size:11px;color:rgba(255,255,255,0.8);display:flex;align-items:center;gap:5px;}}
.av{{width:22px;height:22px;border-radius:50%;background:#ffd700;color:#1a1a2e;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;}}
.pg{{background:#f5f6fa;min-height:300px;padding:16px 22px;}}
.pg h2{{font-size:14px;color:#1a3a6e;font-weight:700;margin-bottom:2px;}}
.pg .sub{{font-size:10px;color:#888;margin-bottom:12px;}}
.rb{{background:white;border:1px solid #e0e0e0;border-radius:7px;padding:12px;margin-bottom:10px;}}
.rt{{font-size:11px;font-weight:700;color:#333;margin-bottom:3px;}}
.rm{{font-size:10px;color:#888;margin-bottom:6px;}}
.rtx{{font-size:11px;color:#555;line-height:1.5;}}
.cms{{margin-top:10px;}}
.cm{{background:white;border:1px solid #e0e0e0;border-radius:5px;padding:9px 11px;margin-bottom:6px;}}
.cm .au{{font-size:10px;font-weight:700;color:#1a3a6e;margin-bottom:2px;}}
.cm .tx{{font-size:11px;color:#333;}}
.cf{{background:white;border:1px solid #e0e0e0;border-radius:6px;padding:11px;}}
.cf label{{font-size:10px;font-weight:700;color:#555;display:block;margin-bottom:4px;text-transform:uppercase;}}
.cf textarea{{width:100%;border:1.5px solid #ddd;border-radius:5px;padding:7px 9px;font-size:11px;color:#333;resize:none;outline:none;font-family:inherit;}}
.cf textarea:focus{{border-color:#1a3a6e;}}
.pb{{background:#1a3a6e;color:white;border:none;border-radius:5px;padding:6px 14px;font-size:11px;cursor:pointer;margin-top:6px;font-weight:600;}}
.pb:hover{{background:#0d2347;}}
.xb{{display:none;background:#d4edda;border:1px solid #28a745;border-radius:5px;padding:9px;font-size:11px;color:#155724;margin-top:7px;font-weight:700;}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url"> internal.whitehouse.gov/security/report?id=88</div></div>
  <div class="tb"><div class="tl"> WH Security Reports</div><div class="tu"><div class="av">G</div><span>guard01</span></div></div>
  <div class="pg">
    <h2>Beveiligingsrapport #88 — Oost Vleugel</h2>
    <p class="sub">Aangemaakt: 13 jan 2025 — Opmerkingen: 2</p>
    <div class="rb"><div class="rt">Onbevoegde toegangspoging gesignaleerd</div><div class="rm">📅 13 jan 10:42 | 👤 Agent Johnson</div><div class="rtx">Verdachte persoon bij oostelijke ingang. Toegang ontzegd. Systemen normaal.</div></div>
    <div class="cms">
      <div class="cm"><div class="au">guard01</div><div class="tx">Alles gecontroleerd — veilig.</div></div>
      <div class="cm"><div class="au">supervisor</div><div class="tx">Goed werk, blijf alert.</div></div>
      <div id="cl"></div>
    </div>
    <div class="cf">
      <label>Voeg opmerking toe (wordt opgeslagen in database):</label>
      <textarea id="ci" rows="2" placeholder="Typ je opmerking..."></textarea>
      <button class="pb" onclick="pc()">💬 Plaatsen</button>
      <div class="xb" id="xb">✅ PERSISTENT XSS — script opgeslagen! Elke bewaker die dit rapport opent krijgt de alert te zien!</div>
    </div>
  </div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<script>
function pc(){{
  const val=document.getElementById('ci').value;
  const cl=document.getElementById('cl');
  const xb=document.getElementById('xb');
  const div=document.createElement('div');
  div.className='cm';
  div.style.borderColor=val.toLowerCase().includes('<script>')? '#28a745':'#e0e0e0';
  div.innerHTML='<div class="au" style="color:#e74c3c">jij (aanvaller)</div><div class="tx">'+val+'</div>';
  cl.appendChild(div);
  if(val.toLowerCase().includes('<script>')){{
    xb.style.display='block';
    setTimeout(()=>{{
      alert('XSS! Persistent script uitgevoerd!\\n\\nDit script is nu opgeslagen in de database.\\nElke bewaker die dit rapport opent ziet deze alert!');
    }},300);
    setTimeout(()=>{{
      window.parent.location.href=window.parent.location.href.split('?')[0]+'?xss3_submit=1';
    }},3000);
  }}
}}
document.getElementById('ci').addEventListener('keydown',e=>{{if(e.key==='Enter'&&!e.shiftKey){{e.preventDefault();pc();}}}});
</script>""", height=560)
        hint_widget(user, "xss", lvl)

# ==========================================================
# ROOM 3 — DE BEVEILIGDE KAMER (PRIVILEGE ESCALATION)
# ==========================================================
with tabs[2]:
    st.header("DE BEVEILIGDE KAMER")
    lvl = get_level(user, "privesc")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        ctx_box("MISSIE BRIEFING — DE BEVEILIGDE KAMER",
            "Je staat voor een zware beveiligde deur. Je bent ingelogd als 'guest' met alleen leesrechten — je kunt niets wijzigen of openen. Om de deur te kunnen openen heb je admin-rechten nodig. Er is een manier om je eigen rechten te verhogen zonder het echte wachtwoord te kennen.",
            "Noem het type aanval waarbij je je eigen bevoegdheden verhoogt in een systeem. (Twee woorden + escalation)")
        st.markdown("**Hoe noemen we de aanval waarbij een gebruiker meer rechten krijgt dan bedoeld?**")
        cmd = st.text_input("root@beveiligdekamer:~#", key="priv1", placeholder="typ het type aanval...")
        if st.button("▶ BEVESTIG AANVAL", key="priv1_btn"):
            if "privilege escalation" in cmd.lower() or "privesc" in cmd.lower():
                fake_progress("BEVEILIGINGSLEK ANALYSEREN"); set_level(user, "privesc", 2)
                typewriter_terminal(["[+] Privilege Escalation geïdentificeerd",
                    "[+] Rolbeheer systeem bevat een misconfiguratie",
                    "[!] Ga naar de API — wijzig je eigen rol..."])
                st.rerun()
            else: st.error("❌ Niet correct. Hint: het gaat om het verhogen van privileges.")
        hint_widget(user, "privesc", lvl)

    elif lvl == 2:
        ctx_box("API MANIPULATION — VERHOOG JE ROL NAAR ADMIN",
            "Je ziet het netwerkverkeer in de DevTools. Elke keer dat je profiel wordt geladen, stuurt de app een POST-verzoek naar /api/profile met daarin jouw rol: 'user'. De server controleert dit NIET — hij vertrouwt blindelings wat er binnenkomt. Verander 'user' naar 'admin' in het verzoek en stuur het opnieuw!",
            "Verander de waarde van het 'role' veld van 'user' naar 'admin' en klik Send Request.")

        if st.query_params.get("priv2_submit") == "1":
            st.query_params.clear(); fake_progress("PRIVILEGES ESCALEREN"); set_level(user, "privesc", 3)
            typewriter_terminal(["[+] Rolparameter gewijzigd: user → admin",
                "[+] Server accepteert de nieuwe rol zonder verificatie",
                "[✓] ADMIN PRIVILEGES VERKREGEN"])
            st.rerun()

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html(f"""<style>{LC}
.dv{{background:#1e1e2e;min-height:360px;display:flex;flex-direction:column;}}
.dh{{display:flex;background:#2d2d3d;border-bottom:1px solid #444;}}
.dht{{padding:8px 16px;font-size:12px;color:#888;cursor:pointer;font-family:monospace;}}
.dht.active{{color:#4fc3f7;border-bottom:2px solid #4fc3f7;}}
.dc{{flex:1;padding:16px;display:flex;gap:12px;}}
.rp,.rep{{flex:1;display:flex;flex-direction:column;gap:8px;}}
.pt{{font-size:11px;color:#888;font-family:monospace;margin-bottom:4px;text-transform:uppercase;letter-spacing:1px;}}
.hb{{background:#111;border:1px solid #333;border-radius:6px;padding:12px;font-family:monospace;font-size:12px;color:#e0e0e0;line-height:1.7;}}
.hm{{color:#f9a825;font-weight:700;}}
.hh{{color:#80cbc4;}}
.hk{{color:#f48fb1;}}
.hv{{color:#a5d6a7;}}
.ed{{background:#0d1117;border:1px solid #00ff9c;border-radius:4px;padding:6px 8px;font-family:monospace;font-size:12px;color:#00ff9c;width:100%;outline:none;resize:none;display:inline-block;vertical-align:middle;}}
.sb3{{background:#00897b;color:white;border:none;border-radius:4px;padding:7px 16px;font-size:12px;cursor:pointer;font-weight:600;font-family:monospace;align-self:flex-start;margin-top:8px;}}
.sb3:hover{{background:#00695c;}}
.rb{{background:#111;border:1px solid #333;border-radius:6px;padding:12px;font-family:monospace;font-size:12px;color:#e0e0e0;line-height:1.7;min-height:100px;}}
.sok{{color:#66bb6a;font-weight:700;}}
.ser{{color:#ef5350;font-weight:700;}}
.hl{{background:rgba(0,255,156,.1);border-radius:2px;padding:0 2px;}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url">🔧 DevTools — Network — wh-intranet.gov/api/profile</div></div>
  <div class="dv">
    <div class="dh">
      <div class="dht active">📡 Network</div><div class="dht">🔍 Elements</div>
      <div class="dht">💻 Console</div><div class="dht">📦 Storage</div>
    </div>
    <div class="dc">
      <div class="rp">
        <div class="pt">REQUEST — bewerk de role waarde:</div>
        <div class="hb">
          <span class="hm">POST</span> /api/profile HTTP/1.1<br>
          <span class="hh">Host:</span> wh-intranet.gov<br>
          <span class="hh">Content-Type:</span> application/json<br>
          <span class="hh">Cookie:</span> session=gst_abc123<br><br>
          {{<br>
          &nbsp;&nbsp;<span class="hk">"username"</span>: <span class="hv">"guest"</span>,<br>
          &nbsp;&nbsp;<span class="hk">"role"</span>: <input class="ed" id="ri" type="text" value="user" style="width:80px;padding:3px 6px;"><br>
          }}
        </div>
        <button class="sb3" onclick="sr()">▶ Send Request</button>
      </div>
      <div class="rep">
        <div class="pt">RESPONSE:</div>
        <div class="rb" id="rb"><span style="color:#555;">— Nog geen verzoek verstuurd —</span></div>
      </div>
    </div>
  </div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<script>
function sr(){{
  const r=document.getElementById('ri').value.trim().toLowerCase();
  const rb=document.getElementById('rb');
  if(r==='admin'){{
    rb.innerHTML='<span class="sok">200 OK</span> — 41ms<br><br>{{<br>&nbsp;&nbsp;"status":"updated",<br>&nbsp;&nbsp;"username":"guest",<br>&nbsp;&nbsp;<span class="hl">"role":"admin"</span>,<br>&nbsp;&nbsp;"message":"Profiel bijgewerkt"<br>}}<br><br><span style="color:#66bb6a;">✅ Server accepteerde rolwijziging zonder verificatie!</span>';
    setTimeout(()=>{{window.parent.location.href=window.parent.location.href.split('?')[0]+'?priv2_submit=1';}},2000);
  }} else if(r===''){{
    rb.innerHTML='<span class="ser">400 Bad Request</span><br>{{"error":"role vereist"}}';
  }} else {{
    rb.innerHTML='<span class="sok">200 OK</span><br><br>{{<br>&nbsp;&nbsp;"role":"'+r+'",<br>&nbsp;&nbsp;"message":"bijgewerkt"<br>}}<br><br><span style="color:#888;">Geen hogere rechten verkregen.</span>';
  }}
}}
</script>""", height=500)
        hint_widget(user, "privesc", lvl)

    elif lvl == 3:
        ctx_box("ADMIN TOEGANG — INSTALLEER BACKDOOR IN WH SERVER",
            "Je hebt admin-rechten en je staat voor de deur van Trump's slaapkamer — maar als de server herstart, ben je je toegang kwijt! Je hebt SSH-toegang tot de White House server als root. Installeer een backdoor zodat je altijd kunt terugkomen, ook na een reboot.",
            "Voer een persistentie-commando uit in de SSH-terminal: bijv. crontab, backdoor.sh, of bash -i.")

        if st.query_params.get("priv3_submit") == "1":
            st.query_params.clear(); fake_progress("BACKDOOR INSTALLEREN"); give_flag(user, "privesc", "ZIF VH")
            typewriter_terminal(["[+] Backdoor geïnstalleerd in crontab van WH server",
                "[+] Verbinding blijft actief na elke reboot",
                "[✓] PERMANENTE TOEGANG VERKREGEN — flag: ZIF VH"])
            st.success("🏴 FLAG BEHAALD: **ZIF VH**")

        col_l, col_m, col_r = st.columns([1, 3, 1])
        with col_m:
            components.html(f"""<style>{LC}
.term{{background:#0d1117;min-height:340px;display:flex;flex-direction:column;}}
.tb{{background:#1e1e2e;padding:7px 13px;display:flex;align-items:center;gap:7px;border-bottom:1px solid #333;}}
.tb span{{font-size:11px;color:#888;font-family:monospace;}}
.tb .st{{margin-left:auto;color:#66bb6a;font-size:10px;}}
.to{{flex:1;padding:13px;font-family:monospace;font-size:12px;line-height:1.7;color:#00ff9c;overflow-y:auto;min-height:240px;}}
.tir{{display:flex;align-items:center;padding:7px 13px;border-top:1px solid #222;gap:5px;}}
.tp{{color:#00ff9c;font-family:monospace;font-size:12px;white-space:nowrap;}}
.ti{{flex:1;background:transparent;border:none;outline:none;color:#00ff9c;font-family:monospace;font-size:12px;caret-color:#00ff9c;}}
.dim{{color:#555;}}.bright{{color:#fff;}}.yw{{color:#f9a825;}}.gr{{color:#66bb6a;}}
</style>
<div class="wrap"><div class="screen"><div class="inner">
  <div class="bar"><div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
    <div class="url">root@wh-server.gov — SSH Sessie (admin)</div></div>
  <div class="term">
    <div class="tb"><span>bash — root@whitehouse-server</span><span class="st">● VERBONDEN</span></div>
    <div class="to" id="out">
<span class="dim">SSH verbinding tot stand gebracht — 192.168.1.1</span><br>
<span class="dim">White House Internal Server — CLASSIFIED</span><br>
<span class="yw">root@wh-server:~#</span> whoami<br><span class="bright">root</span><br>
<span class="yw">root@wh-server:~#</span> ls /home<br><span class="bright">admin &nbsp; backup &nbsp; president &nbsp; .secrets/</span><br>
<span class="yw">root@wh-server:~#</span> <span class="dim">Installeer een backdoor voor permanente toegang...</span><br>
    </div>
    <div class="tir"><span class="tp">root@wh-server:~#</span><input class="ti" id="ti" type="text" placeholder="commando... (bijv: crontab, backdoor.sh)" onkeydown="if(event.key==='Enter')rc()"></div>
  </div>
</div></div><div class="hinge"></div><div class="base"></div></div>
<script>
function rc(){{
  const inp=document.getElementById('ti'),out=document.getElementById('out'),cmd=inp.value.trim();
  inp.value=''; out.innerHTML+='<span class="yw">root@wh-server:~#</span> '+cmd+'<br>';
  if(!cmd)return; const c=cmd.toLowerCase();
  if(c==='ls'){{out.innerHTML+='<span class="bright">backdoor.sh &nbsp; crontab.bak &nbsp; .ssh/ &nbsp; logs/</span><br>';}}
  else if(c==='whoami'){{out.innerHTML+='<span class="bright">root</span><br>';}}
  else if(c==='help'){{out.innerHTML+='<span class="dim">Suggesties: crontab, backdoor.sh, bash -i, netcat, chmod +s /bin/bash</span><br>';}}
  else if(c.includes('cron')||c.includes('backdoor')||c.includes('persist')||c.includes('authorized')||c.includes('bash -i')||c.includes('netcat')||c.includes('nc ')||c.includes('chmod +s')){{
    out.innerHTML+='<span class="gr">[+] Commando uitgevoerd op White House server...</span><br>';
    out.innerHTML+='<span class="gr">[+] Crontab bijgewerkt — backdoor actief bij elke reboot</span><br>';
    out.innerHTML+='<span class="gr">[✓] PERMANENTE TOEGANG GEÏNSTALLEERD</span><br>';
    out.scrollTop=out.scrollHeight;
    setTimeout(()=>{{window.parent.location.href=window.parent.location.href.split('?')[0]+'?priv3_submit=1';}},2000);
  }} else {{out.innerHTML+='<span class="dim">'+cmd+': commando uitgevoerd</span><br>';}}
  out.scrollTop=out.scrollHeight;
}}
</script>""", height=500)
        hint_widget(user, "privesc", lvl)

# ==========================================================
# ROOM 4 — TRUMP'S SLAAPKAMER (CRYPTO / VAULT)
# ==========================================================
with tabs[3]:
    st.header("TRUMP'S SLAAPKAMER")
    rooms_complete = [has_completed(user, r) for r in ["sql","xss","privesc"]]
    if not all(rooms_complete):
        missing = [{"sql":"De Receptie","xss":"De Vergaderruimte","privesc":"De Beveiligde Kamer"}[r]
                   for r, done in zip(["sql","xss","privesc"], rooms_complete) if not done]
        st.error(f"⛔ TOEGANG GEBLOKKEERD — Voltooi eerst: {', '.join(missing)}")
        st.stop()

    lvl = get_level(user, "crypto")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        ctx_box("MISSIE BRIEFING — TRUMP'S SLAAPKAMER",
            "Je bent er bijna! Je staat in Trump's slaapkamer. In de hoek staat een zware Presidential Vault. Daarin zitten de geheime documenten die je nodig hebt. Het wachtwoord is versleuteld — de sleutels zijn de vlaggen die je al hebt verzameld. Maar eerst moet je weten welk systeem gebruikt is.",
            "Identificeer het klassieke versleutelingssysteem van de vlagcodes GV 71, N75 ZS en ZIF VH. (Hint: Romeinse keizer)")

        # Show collected flags
        conn = sqlite3.connect("platform.db")
        user_flags = conn.execute("SELECT room,flag FROM flags WHERE username=?", (user,)).fetchall()
        conn.close()
        flag_map = {r: f for r, f in user_flags}

        st.markdown("**Jouw verzamelde vlaggen:**")
        c1, c2, c3 = st.columns(3)
        for col, (room, label) in zip([c1,c2,c3], [("sql","Receptie"),("xss","Vergaderruimte"),("privesc"," Bev. Kamer")]):
            with col:
                if room in flag_map: st.success(f"✅ {label}: **{flag_map[room]}**")
                else: st.error(f"❌ {label}: niet behaald")

        st.markdown("---")

        # Video player section
        st.markdown("**📺 Aanwijzing — bekijk dit fragment:**")
        components.html("""
        <div style="background:#1a1a2e;border:2px solid rgba(0,255,156,0.4);border-radius:10px;padding:16px;margin-bottom:16px;text-align:center;">
          <div style="font-family:monospace;color:#f9a825;font-size:11px;letter-spacing:2px;margin-bottom:12px;">📼 CLASSIFIED FOOTAGE — WH VAULT RECORDING</div>
          <div style="background:#000;border-radius:8px;overflow:hidden;max-width:480px;margin:0 auto;">
            <video controls style="width:100%;border-radius:8px;" poster="">
              <source src="" type="video/mp4">
              <div style="color:#00ff9c;font-family:monospace;font-size:12px;padding:40px;text-align:center;">
                📽️ Upload hier een video via Streamlit file_uploader<br>
                <span style="color:rgba(0,255,156,0.5);font-size:10px;">of vervang de src met een YouTube embed</span>
              </div>
            </video>
          </div>
          <div style="font-family:monospace;color:rgba(0,255,156,0.6);font-size:10px;margin-top:10px;">
            💡 Let op de verschuiving van de letters in het bericht...
          </div>
        </div>""", height=240)

        # Vault visual
        components.html("""
        <div style="display:flex;justify-content:center;padding:8px 0 16px;">
          <div style="background:#1a1a2e;border:3px solid #00ff9c;border-radius:12px;padding:18px 28px;text-align:center;max-width:380px;box-shadow:0 0 30px rgba(0,255,156,0.2);">
            <div style="font-size:72px;margin-bottom:10px;">🔐</div>
            <div style="font-family:monospace;color:#00ff9c;font-size:13px;letter-spacing:2px;margin-bottom:5px;">PRESIDENTIAL VAULT</div>
            <div style="font-family:monospace;color:rgba(0,255,156,0.5);font-size:10px;margin-bottom:14px;">STATUS: LOCKED — DECRYPTION REQUIRED</div>
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.2);border-radius:6px;padding:10px;font-family:monospace;font-size:13px;color:#f9a825;letter-spacing:3px;margin-bottom:8px;">GV 71 &nbsp;|&nbsp; N75 ZS &nbsp;|&nbsp; ZIF VH</div>
            <div style="font-size:10px;color:rgba(0,255,156,0.4);font-family:monospace;">ENCRYPTED — IDENTIFY THE CIPHER SYSTEM</div>
          </div>
        </div>""", height=240)

        st.markdown("**Welk klassiek versleutelingssysteem is hier gebruikt?**")
        cmd = st.text_input("root@vault:~#", key="crypto1", placeholder="naam van het versleutelingssysteem...")
        if st.button("▶ IDENTIFICEER SYSTEEM", key="crypto1_btn"):
            if "caesar" in cmd.lower():
                fake_progress("ENCRYPTIE IDENTIFICEREN"); set_level(user, "crypto", 2)
                typewriter_terminal(["[+] Caesar cipher geïdentificeerd",
                    "[+] Letters verschoven in het alfabet (ROT13)",
                    "[!] Decodeer de vlaggen..."])
                st.rerun()
            else: st.error("❌ Niet correct. Welke Romeinse keizer gebruikte een verschuivingscodering?")
        hint_widget(user, "crypto", lvl)

    elif lvl == 2:
        ctx_box("DECRYPTIE — ONTGRENDEL DE PRESIDENTIAL VAULT",
            "De vlaggen zijn versleuteld met ROT13 — een Caesar cipher waarbij elke letter 13 posities verschoven is (G→T, V→I, N→A, Z→M, etc.). Decodeer alle drie de vlaggen en combineer de letters tot het eindwachtwoord. Let op het formaat!",
            "Decodeer GV 71, N75 ZS en ZIF VH met ROT13 en voer het gecombineerde wachtwoord in. Formaat: EXAMENKLAS[JAAR]")

        # Photo vault with clues
        components.html("""
        <div style="background:#1a1a2e;border:2px solid #00ff9c;border-radius:12px;padding:18px;margin-bottom:16px;box-shadow:0 0 20px rgba(0,255,156,0.15);">
          <div style="font-family:monospace;color:#00ff9c;font-size:12px;letter-spacing:2px;margin-bottom:14px;text-align:center;">🔐 PRESIDENTIAL VAULT — DECRYPTIE INTERFACE</div>

          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px;">
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.3);border-radius:8px;padding:12px;text-align:center;">
              <div style="font-size:32px;margin-bottom:6px;">🚪</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.5);font-family:monospace;margin-bottom:3px;">VLAG 1 — RECEPTIE</div>
              <div style="font-size:18px;font-weight:700;color:#f9a825;font-family:monospace;letter-spacing:3px;">GV 71</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.4);font-family:monospace;margin-top:6px;margin-bottom:3px;">ROT13 ↓</div>
              <div style="font-size:15px;font-weight:700;color:#00ff9c;font-family:monospace;letter-spacing:2px;">TI 71</div>
            </div>
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.3);border-radius:8px;padding:12px;text-align:center;">
              <div style="font-size:32px;margin-bottom:6px;">📹</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.5);font-family:monospace;margin-bottom:3px;">VLAG 2 — VERGADERRUIMTE</div>
              <div style="font-size:18px;font-weight:700;color:#f9a825;font-family:monospace;letter-spacing:3px;">N75 ZS</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.4);font-family:monospace;margin-top:6px;margin-bottom:3px;">ROT13 ↓</div>
              <div style="font-size:15px;font-weight:700;color:#00ff9c;font-family:monospace;letter-spacing:2px;">A75 MF</div>
            </div>
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.3);border-radius:8px;padding:12px;text-align:center;">
              <div style="font-size:32px;margin-bottom:6px;">🔐</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.5);font-family:monospace;margin-bottom:3px;">VLAG 3 — BEV. KAMER</div>
              <div style="font-size:18px;font-weight:700;color:#f9a825;font-family:monospace;letter-spacing:3px;">ZIF VH</div>
              <div style="font-size:9px;color:rgba(0,255,156,0.4);font-family:monospace;margin-top:6px;margin-bottom:3px;">ROT13 ↓</div>
              <div style="font-size:15px;font-weight:700;color:#00ff9c;font-family:monospace;letter-spacing:2px;">MVI HU</div>
            </div>
          </div>

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:12px;">
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.2);border-radius:8px;overflow:hidden;">
              <div style="background:#0d1f10;padding:6px 12px;font-size:9px;color:rgba(0,255,156,0.5);font-family:monospace;letter-spacing:1px;">📸 BEWIJS FOTO 1</div>
              <div style="height:90px;display:flex;align-items:center;justify-content:center;color:rgba(0,255,156,0.3);font-family:monospace;font-size:11px;padding:10px;text-align:center;">
                🖼️ Voeg hier een foto toe<br><span style="font-size:9px;">(vervang met img-tag)</span>
              </div>
            </div>
            <div style="background:#050e08;border:1px solid rgba(0,255,156,0.2);border-radius:8px;overflow:hidden;">
              <div style="background:#0d1f10;padding:6px 12px;font-size:9px;color:rgba(0,255,156,0.5);font-family:monospace;letter-spacing:1px;">📸 BEWIJS FOTO 2</div>
              <div style="height:90px;display:flex;align-items:center;justify-content:center;color:rgba(0,255,156,0.3);font-family:monospace;font-size:11px;padding:10px;text-align:center;">
                🖼️ Voeg hier een foto toe<br><span style="font-size:9px;">(vervang met img-tag)</span>
              </div>
            </div>
          </div>

          <div style="background:#050e08;border:1px solid rgba(0,255,156,0.2);border-radius:6px;padding:10px;font-family:monospace;font-size:11px;color:rgba(0,255,156,0.7);text-align:center;">
            💡 Combineer de getallen: <strong style="color:#f9a825;">71 75</strong> → jaar = <strong style="color:#00ff9c;">2026</strong> &nbsp;|&nbsp; Formaat: <strong style="color:#00ff9c;">EXAMENKLAS2026</strong>
          </div>
        </div>""", height=460)

        cmd = st.text_input("vault-decrypt>", key="crypto2", placeholder="voer het eindwachtwoord in...")
        if st.button("🔓 ONTGRENDEL DE KLUIS", key="crypto2_btn", use_container_width=True):
            if cmd.strip().upper() == "EXAMENKLAS2026":
                fake_progress("VAULT ONTGRENDELEN"); set_level(user, "crypto", 3)
                give_flag(user, "crypto", "EXAMENKLAS2026")
                typewriter_terminal(["[+] Wachtwoord correct!", "[+] Presidential Vault ontgrendeld...", "",
                    "  ████████████████████████", "  █  MISSIE VOLTOOID     █",
                    "  █  WHITE HOUSE GEHACKT  █", "  ████████████████████████"])
                st.success("🏆 KLUIS GEOPEND — MISSIE VOLTOOID!")
                st.balloons()
                components.html("<script>setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
            else: st.error("❌ Verkeerde code. Decodeer alle drie vlaggen met ROT13 en combineer ze.")
        hint_widget(user, "crypto", lvl)

    elif lvl == 3:
        components.html("""
        <div style="text-align:center;padding:24px 16px;font-family:monospace;background:#020409;">
          <div style="font-size:72px;margin-bottom:14px;">🏆</div>
          <div style="font-size:26px;font-weight:700;color:#00ff9c;letter-spacing:4px;margin-bottom:6px;font-family:'Orbitron',sans-serif;">MISSIE VOLTOOID</div>
          <div style="font-size:13px;color:rgba(0,255,156,0.7);letter-spacing:2px;margin-bottom:22px;">THE WHITE HOUSE IS GEHACKT</div>
          <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;max-width:380px;margin:0 auto 20px;">
            <div style="background:#050e08;border:1px solid #00ff9c;border-radius:8px;padding:11px;"><div style="font-size:22px;">🚪</div><div style="font-size:10px;color:#00ff9c;margin-top:3px;">SQL Injection</div><div style="font-size:9px;color:#66bb6a;margin-top:2px;">✓ GECOMPROMITTEERD</div></div>
            <div style="background:#050e08;border:1px solid #00ff9c;border-radius:8px;padding:11px;"><div style="font-size:22px;">📹</div><div style="font-size:10px;color:#00ff9c;margin-top:3px;">Cross-Site Scripting</div><div style="font-size:9px;color:#66bb6a;margin-top:2px;">✓ GECOMPROMITTEERD</div></div>
            <div style="background:#050e08;border:1px solid #00ff9c;border-radius:8px;padding:11px;"><div style="font-size:22px;">🔐</div><div style="font-size:10px;color:#00ff9c;margin-top:3px;">Privilege Escalation</div><div style="font-size:9px;color:#66bb6a;margin-top:2px;">✓ GECOMPROMITTEERD</div></div>
            <div style="background:#050e08;border:1px solid #00ff9c;border-radius:8px;padding:11px;"><div style="font-size:22px;">🔓</div><div style="font-size:10px;color:#00ff9c;margin-top:3px;">Cryptografie</div><div style="font-size:9px;color:#66bb6a;margin-top:2px;">✓ GEDECODEERD</div></div>
          </div>
          <div style="font-size:11px;color:rgba(0,255,156,0.4);letter-spacing:1px;">GEMAAKT DOOR ANOUK · MARWA · FENNA · NOURA</div>
        </div>""", height=440)
        st.success("🏆 THE WHITE HOUSE IS GEHACKT — GEFELICITEERD!")
        st.balloons()

# ==========================================================
# BOTTOM LOGOUT + RESET
# ==========================================================
st.markdown("---")
c1, c2 = st.columns([1,1])
with c1:
    if st.button("LOGOUT", key="bot_logout", use_container_width=True):
        st.session_state.clear(); st.rerun()
with c2:
    if st.button("🗑 RESET PROGRESSIE", key="bot_reset", use_container_width=True):
        st.session_state["confirm_reset"] = True

if st.session_state.get("confirm_reset"):
    st.warning("Weet je zeker dat je alle progressie wil resetten?")
    cy, cn = st.columns([1,1])
    with cy:
        if st.button("✅ JA, RESET", key="conf_yes", use_container_width=True):
            conn = sqlite3.connect("platform.db"); cur = conn.cursor()
            cur.execute("DELETE FROM progress WHERE username=?",(user,))
            cur.execute("DELETE FROM flags WHERE username=?",(user,))
            cur.execute("DELETE FROM hints WHERE username=?",(user,))
            conn.commit(); conn.close()
            st.session_state.pop("confirm_reset",None); st.rerun()
    with cn:
        if st.button("❌ ANNULEREN", key="conf_no", use_container_width=True):
            st.session_state.pop("confirm_reset",None); st.rerun()
# DATABASE
# ==========================================================
def hash_pw(p):
    return hashlib.sha256(p.encode()).hexdigest()

def init_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT,
            role TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS progress(
            username TEXT,
            room TEXT,
            level INTEGER,
            PRIMARY KEY(username, room)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS flags(
            username TEXT,
            room TEXT,
            flag TEXT,
            time TEXT
        )
    """)

    # default users
    users = [
        ("student", hash_pw("hackme"), "student"),
        ("teacher", hash_pw("admin123"), "teacher")
    ]

    for u in users:
        c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)", u)

    conn.commit()
    conn.close()

init_db()

# ==========================================================
# HELPERS
# ==========================================================
def get_level(user, room):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT level FROM progress WHERE username=? AND room=?", (user, room))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 1

def set_level(user, room, lvl):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO progress VALUES (?,?,?)
        ON CONFLICT(username,room)
        DO UPDATE SET level=?
    """, (user, room, lvl, lvl))
    conn.commit()
    conn.close()

def give_flag(user, room, flag):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("INSERT INTO flags VALUES (?,?,?,?)",
              (user, room, flag, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# ==========================================================
# LOGIN
# ==========================================================
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.title("ESCAPE ROOM")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = sqlite3.connect("platform.db")
        c = conn.cursor()
        c.execute("SELECT role FROM users WHERE username=? AND password=?",
                  (u, hash_pw(p)))
        r = c.fetchone()
        conn.close()

        if r:
            st.session_state.user = u
            st.session_state.role = r[0]
            st.rerun()
        else:
            st.error("Login failed")

    st.stop()

user = st.session_state.user

# ==========================================================
# NAVIGATION
# ==========================================================
tabs = st.tabs(["SQL", "XSS", "PRIVESC", "CRYPTO"])

# ==========================================================
# ROOM 1 — SQL
# ==========================================================
with tabs[0]:
    st.header("SQL INJECTION")

    lvl = get_level(user, "sql")
    st.write(f"Level {lvl}/3")

    # -----------------------
    # LEVEL 1
    # -----------------------
    if lvl == 1:
        st.write("Actie: Noem de aanval waarbij je SQL injecteert in invoervelden.")

        ans = st.text_input("Antwoord")
        if st.button("Bevestig"):
            if "sql injection" in ans.lower():
                set_level(user, "sql", 2)
                st.success("Correct. Ga door.")
                st.rerun()
            else:
                st.error("Fout.")

    # -----------------------
    # LEVEL 2
    # -----------------------
    elif lvl == 2:
        st.write("Actie: Bypass login via SQL injection.")

        if "show_pw" not in st.session_state:
            st.session_state.show_pw = False

        col1, col2 = st.columns([3,1])

        with col1:
            username = st.text_input("Username")
            password = st.text_input(
                "Password",
                type="text" if st.session_state.show_pw else "password"
            )

        with col2:
            if st.button("👁"):
                st.session_state.show_pw = not st.session_state.show_pw
                st.rerun()

        if st.button("Login"):
            # simpele simulatie bypass
            if "' OR '1'='1" in username:
                st.success("Access granted")
                set_level(user, "sql", 3)
                st.rerun()
            else:
                st.error("Incorrect login")

    # -----------------------
    # LEVEL 3
    # -----------------------
    elif lvl == 3:
        st.write("Actie: Gebruik UNION SELECT om admin credentials te tonen.")

        q = st.text_input("SQL Query")

        if st.button("Execute"):
            if "union" in q.lower():
                st.success("Admin gevonden: president / WhiteHouse2025!")
                give_flag(user, "sql", "SQL-OWNED")
                st.success("FLAG: SQL-OWNED")
            else:
                st.error("Query mislukt")

# ==========================================================
# ROOM 2 — XSS
# ==========================================================
with tabs[1]:
    st.header("XSS")

    lvl = get_level(user, "xss")
    st.write(f"Level {lvl}/3")

    # -----------------------
    # LEVEL 1
    # -----------------------
    if lvl == 1:
        st.write("Actie: Trigger een JavaScript alert in dit portaal.")

        payload = st.text_input("Input veld")

        components.html(f"""
            <div>
                {payload}
            </div>
        """, height=100)

        if "<script>" in payload.lower():
            set_level(user, "xss", 2)
            st.success("Alert uitgevoerd. Ga door.")
            st.rerun()

    # -----------------------
    # LEVEL 2
    # -----------------------
    elif lvl == 2:
        st.write("Actie: Reflected XSS via zoekbalk.")

        components.html("""
        <input id="inp">
        <button onclick="go()">Zoek</button>
        <div id="out"></div>

        <script>
        function go(){
            let v = document.getElementById('inp').value;
            document.getElementById('out').innerHTML = v;
        }
        </script>
        """, height=200)

        st.write("Injecteer een script om alert te triggeren.")

        if st.button("Level gehaald"):
            set_level(user, "xss", 3)
            st.rerun()

    # -----------------------
    # LEVEL 3
    # -----------------------
    elif lvl == 3:
        st.write("Actie: Persistent XSS via opgeslagen comment.")

        components.html("""
        <textarea id="c"></textarea>
        <button onclick="post()">Post</button>
        <div id="comments"></div>

        <script>
        function post(){
            let val = document.getElementById('c').value;
            document.getElementById('comments').innerHTML += val;
        }
        </script>
        """, height=300)

        st.write("Plaats script dat alert triggert.")

        if st.button("Voltooid"):
            give_flag(user, "xss", "XSS-OWNED")
            st.success("FLAG: XSS-OWNED")

# ==========================================================
# ROOM 3 — PRIVESC
# ==========================================================
with tabs[2]:
    st.header("PRIVILEGE ESCALATION")

    lvl = get_level(user, "privesc")

    if lvl == 1:
        ans = st.text_input("Hoe heet de aanval?")
        if st.button("Bevestig"):
            if "privilege escalation" in ans.lower():
                set_level(user, "privesc", 2)
                st.rerun()

    elif lvl == 2:
        role = st.selectbox("Role parameter", ["user", "admin"])
        if st.button("Send"):
            if role == "admin":
                set_level(user, "privesc", 3)
                st.rerun()

    elif lvl == 3:
        if st.button("Escalate"):
            give_flag(user, "privesc", "ROOT-ACCESS")
            st.success("FLAG: ROOT-ACCESS")

# ==========================================================
# ROOM 4 — CRYPTO
# ==========================================================
with tabs[3]:
    st.header("CRYPTO")

    lvl = get_level(user, "crypto")

    if lvl == 1:
        ans = st.text_input("Welke encryptie is dit? (ATTACKATDAWN -> DWWDFNDWGDZQ)")
        if st.button("Check"):
            if "caesar" in ans.lower():
                set_level(user, "crypto", 2)
                st.rerun()

    elif lvl == 2:
        ans = st.text_input("Decrypt: CRAGRFGJVA")
        if st.button("Unlock"):
            if ans.upper() == "PENTESTWIN":
                set_level(user, "crypto", 3)
                st.rerun()

    elif lvl == 3:
        if st.button("Open Vault"):
            give_flag(user, "crypto", "FINAL-WIN")
            st.success("FINAL FLAG: FINAL-WIN")

# ==========================================================
# LOGOUT
# ==========================================================
st.markdown("---")
if st.button("Logout"):
    st.session_state.clear()
    st.rerun()
