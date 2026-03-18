import streamlit as st
import sqlite3
import hashlib
import time
from datetime import datetime
import streamlit.components.v1 as components

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("THE WHITE HOUSE", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)
# ==========================================================
# VIBE — MATRIX RAIN + SCANLINES + SOUNDS + FONTS
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

    for u in [("undercover", hash_pw("epsteinfiles"), "student"),
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
        "💡 Kijk op je cheat sheet, het type aanval staat in het rijtje! En heb je goed naar de sticky note gekeken?",
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
# VIDEO'S
# ==========================================================
# Videos die tussen de kamers door zich afspelen
#
VIDEOS = {
    # Video 1: voor kamer 1,  SQL(Level 1)
    "sql_1_before": {
        "source": "https://youtu.be/nD8rPj7Db5o?feature=shared",  # link video 1
        "title": "Wat is jullie opdracht?",
        "caption": "Bekijk deze video voordat je aan kamer 1 begint.",
        "autoplay": True
    },
    
    # Video 2: voor kamer 2, XSS  (Level 1)
    "xss_1_before": {
        "source": "https://youtu.be/_s4KIIH8U6E?si=QhbEE3LVcAF7EnMb",  # link video 2
        "title": "De volgende stap...",
        "caption": "Goed! Jullie zijn langs de receptie! Kijk nu deze video en begin daarna aan kamer 2.",
        "autoplay": True
    },
    
    # Video 3: voor PrivEsc  (Level 1)
    "privesc_1_before": {
        "source": "https://youtu.be/hDX17X3wbkg?si=jnUEtKS6Z5ztWefk",  # link video 3
        "title": "Goed bezig! Nog 2 kamers te gaan!",
        "caption": "Houd je ogen open en oren gespitst. Bekijk deze video en vergeet niet om goed op te letten",
        "autoplay": True
    },
    
    # Video 4: voor encryptie (Level 1)
    "crypto_1_before": {
        "source": "https://youtu.be/4HohWyqEV2E?si=BXnV3ZXNOJJVrQ7s",  # link video 4
        "title": "Jullie zijn er bijna, nog even en dan hebben jullie alle macht om de epsteinfiles te publiceren!",
        "caption": "SHHHH! Wees stil!",
        "autoplay": True
    },
    
    # Video 5: na encryptie kamer (Final Victory)
    "crypto_complete": {
        "source": "https://youtu.be/W8vu-yWcLsg?si=Zd0KmOoyg5sOjnzz",  # link video 5
        "title": "MISSIE GESLAAGD!",
        "caption": "Je hebt het White House succesvol gehackt!",
        "autoplay": True
    },
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

def show_video(video_source, title=None, caption=None, autoplay=True):
    """
    Display a video with cinematic styling
    video_source can be:
    - YouTube URL: "https://www.youtube.com/watch?v=..."
    - Local file path: "/mnt/user-data/uploads/video.mp4"
    - Embedded video URL: "https://example.com/video.mp4"
    """
    st.markdown("<br>", unsafe_allow_html=True)
    
    if title:
        st.markdown(f"<h3 style='text-align:center; color:#00ff9c; text-shadow: 0 0 15px rgba(0,255,156,0.5);'>🎬 {title}</h3>", unsafe_allow_html=True)
    
    if caption:
        st.markdown(f"<p style='text-align:center; color:#00ff9c; opacity:0.8; font-size:14px;'>{caption}</p>", unsafe_allow_html=True)
    
    # Check if it's a YouTube URL
    if "youtube.com" in video_source or "youtu.be" in video_source:
        # Extract video ID
        if "youtu.be/" in video_source:
            video_id = video_source.split("youtu.be/")[1].split("?")[0]
        else:
            video_id = video_source.split("v=")[1].split("&")[0]
        
        # Embed YouTube video with cinematic styling - FULL WIDTH LANDSCAPE
        autoplay_param = "?autoplay=1&mute=1" if autoplay else ""
        st.markdown(f"""
        <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; width: 100%; margin: 20px auto; background: #000; border: 2px solid #00ff9c; border-radius: 8px; box-shadow: 0 0 30px rgba(0,255,156,0.3);">
            <iframe 
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
                src="https://www.youtube.com/embed/{video_id}{autoplay_param}"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
            </iframe>
        </div>
        """, unsafe_allow_html=True)
    
    # Local or direct video file
    else:
        try:
            # Try to read as local file
            if video_source.startswith("/"):
                with open(video_source, 'rb') as video_file:
                    video_bytes = video_file.read()
                    st.video(video_bytes)
            else:
                # Direct URL
                st.video(video_source)
        except Exception as e:
            st.error(f"⚠️ Kon video niet laden: {video_source}")
            st.error(f"Error: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)

def check_and_show_video(room, level=None, position="before"):
    """
    Check if there's a video configured for this room/level and show it
    position: "before" or "after" the level
    Also supports "complete" for after completing all levels in a room
    """
    video_key = f"{room}_{level}_{position}"
    
    # Check for room completion video
    if position == "complete":
        video_key = f"{room}_complete"
    
    if video_key in VIDEOS:
        video_config = VIDEOS[video_key]
        show_video(
            video_source=video_config.get("source"),
            title=video_config.get("title"),
            caption=video_config.get("caption"),
            autoplay=video_config.get("autoplay", True)
        )
        return True
    return False

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

    with st.expander(f"HINTS ({next_hint}/{len(hints)} gebruikt)"):
        for i in used:
            st.info(hints[i])

        if next_hint < len(hints):
            if st.button(f"VRAAG OM HINT {next_hint + 1}", key=f"hint_{room}_{next_hint}"):
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
            CYBERSECURITY ESCAPEROOM &mdash; GEMAAKT DOOR: ANOUK, MARWA, FENNA EN NOURA
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
        u = st.text_input("GEBRUIKERSNAAM", placeholder="geef je gebruikersnaam")
        p = st.text_input("WACHTWOORD", type="password", placeholder="••••••••")
        if st.button("▶ TOEGANG AANVRAGEN", use_container_width=True):
            role = auth(u, p)
            if role:
                fake_progress("IDENTITEIT VERIFIËREN")
                st.session_state.user = u
                st.session_state.role = role
                st.rerun()
            else:
                st.error("TOEGANG GEWEIGERD — Ongeldige credentials")
    st.stop()

# ==========================================================
# TEACHER VIEW
# ==========================================================
if st.session_state.role == "teacher":
    st.title("CONTROL PANEL")

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
        st.success(f"Progressie van {reset_target} gereset!")
        st.rerun()

    st.markdown("---")
    if st.button("LOGOUT"):
        st.session_state.clear()
        st.rerun()
    st.stop()

# ==========================================================
# STUDENT VIEW
# ==========================================================
user = st.session_state.user




st.markdown("---")

tabs = st.tabs(["DE RECEPTIE", "DE VERGADERRUIMTE", "DE BEVEILIGDE KAMER", "TRUMP'S KAMER"])

# ==========================================================
# KAMER 1, RECEPTIE - SQL INJECTION
# ==========================================================
with tabs[0]:
    st.header("DE RECEPTIE")
    st.markdown("*Infiltreer het authenticatiesysteem van het Witte Huis.*")
    
    lvl = get_level(user, "sql")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        # Show intro video before SQL Level 1
        check_and_show_video("sql", 1, "before")
        
        st.info("Yes! Jullie zijn binnen. Je partner in crime heeft de receptioniste weggelokt. Nu aan jou de taak om achter haar computer te kruipen en te proberen om in het systeem te komen. Kijk goed om je heen!")
        st.markdown("""
```
[INFORMATIE]
Locatie: White House Reception Authentication System
Doelwit: auth.whitehouse.gov:3306
Bevinding: Login module accepteert ongefilterde gebruikersinput
Kwetsbaarheid: Database queries kunnen worden gemanipuleerd

ACTIE VEREIST: Identificeer het type aanval
```
        """)
        st.markdown("**Welk type aanval misbruikt de database queries door kwaadaardige code in de invoervelden te injecteren?**")
        cmd = st.text_input("Raadsel 1", key="sql1", placeholder="typ het type aanval...")
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
                st.error("Incorrect. Vraag een hint als je vastloopt.")
        hint_widget(user, "sql", lvl)

    elif lvl == 2:
        st.info(" **Raadsel 2** Bypass het login scherm met een SQL injection payload")
        st.markdown("""
```
[EXPLOIT FASE]
Je hebt toegang tot het login systeem.
De applicatie voert deze query uit:
    SELECT * FROM users WHERE username='INPUT' AND password='INPUT'

OPDRACHT: Manipuleer de gebruikersnaam zodat de WHERE-clausule
               altijd TRUE wordt, ongeacht het wachtwoord
```
        """)
        
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
                <div class="dot r"></div>
                <div class="dot y"></div>
                <div class="dot g"></div>
                <div class="url-bar">🔒 auth.whitehouse.gov/secure-login</div>
              </div>
              <div class="login-page">
                <div class="company-logo">White<span>House</span></div>
                <div class="tagline">Executive Branch Security Portal — Authorized Personnel Only</div>
                <div class="login-card" id="loginCard">
                  <h3>Secure Authentication</h3>
                  <div class="msg" id="msg"></div>
                  <div class="field">
                    <label>Gebruikersnaam</label>
                    <input type="text" id="uname" placeholder="gebruiker@whitehouse.gov" oninput="liveCheck(this)">
                  </div>
                  <div class="field">
                    <label>Wachtwoord</label>
                    <input type="password" id="pw" placeholder="••••••••">
                  </div>
                  <button class="login-btn" onclick="tryLogin()">🔐 Secure Login</button>
                  <div class="footer-links">
                    <a href="javascript:void(0)" onclick="showForgot()">Wachtwoord vergeten?</a>
                    <a href="javascript:void(0)" onclick="showHelp()">IT Support</a>
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
            <h4>Wachtwoord Reset</h4>
            <p>Contact IT Security: security@whitehouse.gov of bel intern extensie 1600.</p>
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
                msg.innerHTML = '✅ SQL INJECTION GESLAAGD!<br><br><strong style="font-size:15px;">🎯 Ingelogd als: POTUS</strong><br><br><div style="background:#fff3cd;border:1px solid #ffc107;padding:8px;margin-top:8px;border-radius:4px;color:#856404;"><strong>➡️ VOLGENDE STAP:</strong><br>De groene knop is nu actief! Scroll naar beneden en klik erop om door te gaan.</div>';
                
                // Set flag in localStorage and reload
                localStorage.setItem('sql2_unlocked', 'true');
                setTimeout(() => location.reload(), 1000);
            } else if (u === '' || p === '') {
                msg.className = 'msg error';
                msg.style.display = 'block';
                msg.innerHTML = '⚠️ Alle velden zijn verplicht.';
            } else {
                msg.className = 'msg error';
                msg.style.display = 'block';
                msg.innerHTML = '⛔ Ongeldige credentials. Toegang geweigerd.';
                card.style.animation = 'shake 0.3s ease';
                setTimeout(() => card.style.animation = '', 300);
            }
        }
        function showForgot() {
            document.getElementById('forgotModal').style.display = 'flex';
        }
        function showHelp() {
            alert('White House IT Support\\nExtensie: 1600\\nEmail: security@whitehouse.gov\\n24/7 Beschikbaar');
        }
        document.getElementById('uname').addEventListener('keydown', e => { if(e.key === 'Enter') document.getElementById('pw').focus(); });
        document.getElementById('pw').addEventListener('keydown', e => { if(e.key === 'Enter') tryLogin(); });

        const style = document.createElement('style');
        style.textContent = '@keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-8px)} 75%{transform:translateX(8px)} }';
        document.head.appendChild(style);
        </script>
        """, height=700)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Check if unlocked via custom component that reads localStorage
        unlock_check = components.html("""
        <script>
        const unlocked = localStorage.getItem('sql2_unlocked') === 'true';
        if (unlocked) {
            localStorage.removeItem('sql2_unlocked');
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
        } else {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
        }
        </script>
        """, height=0)
        
        if unlock_check:
            if st.button("GA DOOR NAAR LEVEL 3", key="sql2_continue", use_container_width=True, type="primary"):
                fake_progress("AUTHENTICATIE BYPASSEN")
                set_level(user, "sql", 3)
                typewriter_terminal([
                    "[+] SQL query gemanipuleerd",
                    "[+] WHERE clause: TRUE voor alle rijen",
                    "[+] Ingelogd als eerste gebruiker in database: POTUS",
                    "[✓] AUTHENTICATIE BYPASSED"
                ])
                st.rerun()
        else:
            st.info("Voer eerst de SQL injection uit in de laptop hierboven. De knop wordt actief zodra de exploit slaagt.")
            st.button("GA DOOR NAAR LEVEL 3", key="sql2_continue_disabled", use_container_width=True, type="primary", disabled=True)

        hint_widget(user, "sql", lvl)

    elif lvl == 3:
        st.info("**MISSIE:** Extract gevoelige data uit de database met UNION SELECT")
        st.markdown("""
```
[DATA EXTRACTION]
Je bent nu ingelogd in het admin panel.
De SQL console geeft je directe toegang tot de database.

ACTIE VEREIST: Gebruik UNION SELECT om geheime admin credentials te extraheren
               uit de 'users' tabel
```
        """)
        
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
                    <div class="url-bar">🔒 admin.whitehouse.gov/database-console</div>
                  </div>
                  <div class="topnav">
                    <div class="logo">White<span>House</span> Admin</div>
                    <div class="user-info"><div class="avatar">P</div><span>POTUS</span></div>
                  </div>
                  <div class="dashboard">
                    <div class="sidebar">
                      <div class="sidebar-item active">👥 Database Query</div>
                      <div class="sidebar-item" onclick="showMsg('Dashboard')">📊 Dashboard</div>
                      <div class="sidebar-item" onclick="showMsg('Settings')">⚙️ Settings</div>
                      <div class="sidebar-item" onclick="showMsg('Security Logs')">📋 Logs</div>
                      <div class="sidebar-item" onclick="showMsg('Access Control')">🔒 Access</div>
                    </div>
                    <div class="content">
                      <h2>Database Query Console — Direct SQL Access</h2>
                      <div class="sql-console">
                        <div class="sql-header">
                          <span>DATABASE:</span><span class="db-name">whitehouse_main</span>
                          <span style="margin-left:auto;">TABLE: staff</span>
                        </div>
                        <div class="sql-input-row">
                          <span class="sql-prompt">sql&gt;</span>
                          <input class="sql-input" id="sqlInput" type="text"
                            value="SELECT * FROM staff"
                            onkeydown="if(event.key==='Enter')runQuery()">
                          <button class="sql-btn" onclick="runQuery()">▶ EXECUTE</button>
                        </div>
                        <div class="results">
                          <div class="result-info" id="info">3 rows returned</div>
                          <table class="data-table">
                            <thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th></tr></thead>
                            <tbody id="tbody">
                              <tr><td>1</td><td>Sarah Chen</td><td>schen@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr>
                              <tr><td>2</td><td>Marcus Rodriguez</td><td>mrodriguez@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr>
                              <tr><td>3</td><td>Emily Johnson</td><td>ejohnson@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr>
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
                    row.innerHTML = '<td>UNION</td><td>POTUS</td><td>Covfefe2024!</td><td><span class="badge admin">ADMIN</span></td>';
                    tbody.appendChild(row);
                    info.className = 'result-info ok';
                    info.innerHTML = '⚠️ 4 rows gevonden — SECRET ADMIN CREDENTIALS EXTRACTED!<br><br><strong style="color:#28a745;">➡️ De groene knop is nu actief! Scroll naar beneden en claim de flag.</strong>';
                    
                    // Set flag in localStorage and reload
                    localStorage.setItem('sql3_unlocked', 'true');
                    setTimeout(() => location.reload(), 1000);
                } else if (q.includes('drop')||q.includes('delete')||q.includes('truncate')) {
                    info.className = 'result-info err';
                    info.innerHTML = '⛔ ERROR: Write permissions denied.';
                } else if (q.includes('select') && q.includes('where')) {
                    info.className = 'result-info';
                    info.innerHTML = '1 row returned';
                    tbody.innerHTML = '<tr><td>1</td><td>Sarah Chen</td><td>schen@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr>';
                } else if (q.includes('select')) {
                    info.className = 'result-info';
                    info.innerHTML = '3 rows returned';
                    tbody.innerHTML = `<tr><td>1</td><td>Sarah Chen</td><td>schen@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr><tr><td>2</td><td>Marcus Rodriguez</td><td>mrodriguez@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr><tr><td>3</td><td>Emily Johnson</td><td>ejohnson@whitehouse.gov</td><td><span class="badge user">staff</span></td></tr>`;
                } else {
                    info.className = 'result-info err';
                    info.innerHTML = '⛔ SQL SYNTAX ERROR.';
                }
            }
            function showMsg(m) {
                alert(m + ' — Access restricted via SQL console');
            }
            </script>
            """, height=560)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if has_completed(user, "sql"):
            st.success(" FLAG BEHAALD: **GV 71** — Ga naar volgende kamer")
        else:
            # Check if unlocked via localStorage
            unlock_check = components.html("""
            <script>
            const unlocked = localStorage.getItem('sql3_unlocked') === 'true';
            if (unlocked) {
                localStorage.removeItem('sql3_unlocked');
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
            } else {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
            }
            </script>
            """, height=0)
            
            if unlock_check:
                if st.button("CLAIM FLAG", key="sql3_continue", use_container_width=True, type="primary"):
                    fake_progress("DATABASE DUMPEN")
                    give_flag(user, "sql", "GV 71")
                    typewriter_terminal([
                        "[+] UNION query uitgevoerd",
                        "[+] Resultaten gecombineerd:",
                        "",
                        "  ID     | username | password       | role",
                        "  -------|----------|----------------|------",
                        "  UNION  | Potus    | Covfefe2024!   | ADMIN",
                        "",
                        "[✓] GEHEIME CODE GEVONDEN: GV 71"
                    ])
                    st.rerun()
            else:
                st.info("💡 Voer eerst de UNION SELECT query uit in de SQL console hierboven. De knop wordt actief zodra de exploit slaagt.")
                st.button("CLAIM FLAG", key="sql3_continue_disabled", use_container_width=True, type="primary", disabled=True)
            
        hint_widget(user, "sql", lvl)

# ==========================================================
# KAMER 2, DE VERGADERRUIMTE - XSS
# ==========================================================
with tabs[1]:
    st.header("DE VERGADERRUIMTE")
    st.markdown("*Injecteer kwaadaardige scripts in het internal communications portal.*")
    
    lvl = get_level(user, "xss")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        # Show intro video before XSS Level 1
        check_and_show_video("xss", 1, "before")
        
        st.info("**MISSIE:** Identificeer de kwetsbaarheid in het communications portal")
        st.markdown("""
```
[INFORMATIE]
Locatie: White House Internal Communications Portal
Doelwit: comms.whitehouse.gov/search
Bevinding: User input wordt direct in HTML weergegeven
Kwetsbaarheid: Geen sanitization van gebruikersinput

ACTIE VEREIST: Identificeer het type aanval
```
        """)
        st.markdown("**Welk type aanval injecteert kwaadaardige scripts die door andere gebruikers worden uitgevoerd?**")
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
                st.error("Incorrect. Denk: welke aanval injecteert scripts?")
        hint_widget(user, "xss", lvl)

    elif lvl == 2:
        st.info(" **MISSIE:** Trigger een XSS alert om het beveiligingssysteem af te leiden")
        st.markdown("""
```
[EXPLOIT FASE]
Het search portal reflecteert gebruikersinput zonder filtering.

ACTIE VEREIST: Injecteer een JavaScript payload die een alert() triggert
               Dit zal de security bewakers afleiden
```
        """)
        
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
                    <div class="url">🔒 comms.whitehouse.gov/search</div>
                  </div>
                  <div class="topbar">
                    <div class="site-logo">White<span>House</span> Portal</div>
                    <div class="nav-links">
                      <a href="javascript:void(0)">Home</a>
                      <a href="javascript:void(0)">Documents</a>
                      <a href="javascript:void(0)">News</a>
                    </div>
                  </div>
                  <div class="content-area">
                    <div class="page-title">Internal Communications Search</div>
                    <div class="page-sub">Search classified documents and memos — results displayed in real-time</div>
                    <div class="search-row">
                      <input class="search-box" id="searchInput" type="text" placeholder="Enter search query...">
                      <button class="search-btn" onclick="doSearch()">🔍 Search</button>
                    </div>
                    <div class="result-area">
                      <div class="result-label">SEARCH RESULTS — your query:</div>
                      <div class="result-text" id="resultText"><em style="color:#bbb;">No query entered</em></div>
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
                const alertBox = document.getElementById('alertBox');
                if (val.toLowerCase().includes('<script>')) {
                    // XSS vulnerability - deliberately executing user input
                    result.innerHTML = val;
                    alertBox.className = 'alert-box xss';
                    alertBox.style.display = 'block';
                    alertBox.innerHTML = '✅ XSS ATTACK SUCCESSFUL!<br><br><strong style="font-size:14px;">➡️ De groene knop is nu actief! Scroll naar beneden.</strong>';
                    // Trigger actual alert to show XSS works
                    setTimeout(() => alert('🚨 SECURITY BREACH DETECTED! This alert proves XSS works!'), 100);
                    
                    // Set flag in localStorage and reload
                    localStorage.setItem('xss2_unlocked', 'true');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    result.textContent = val || '(empty query)';
                    alertBox.className = 'alert-box';
                    alertBox.style.display = val ? 'block' : 'none';
                    alertBox.innerHTML = '⚠️ Input displayed but no script detected.';
                }
            }
            document.getElementById('searchInput').addEventListener('keydown', e => {
                if (e.key === 'Enter') doSearch();
            });
            </script>
            """, height=520)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Check if unlocked via localStorage
        unlock_check = components.html("""
        <script>
        const unlocked = localStorage.getItem('xss2_unlocked') === 'true';
        if (unlocked) {
            localStorage.removeItem('xss2_unlocked');
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
        } else {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
        }
        </script>
        """, height=0)
        
        if unlock_check:
            if st.button("GA DOOR NAAR LEVEL 3", key="xss2_continue", use_container_width=True, type="primary"):
                fake_progress("PAYLOAD INJECTEREN")
                set_level(user, "xss", 3)
                typewriter_terminal([
                    "[+] Script tag gedetecteerd in input",
                    "[+] Browser voert JavaScript uit",
                    "[+] Security alert getriggered — bewakers afgeleid!",
                    "[✓] REFLECTED XSS GESLAAGD"
                ])
                st.rerun()
        else:
            st.info("💡 Voer eerst de XSS payload uit in de search box hierboven. De knop wordt actief zodra de alert verschijnt.")
            st.button("GA DOOR NAAR LEVEL 3", key="xss2_continue_disabled", use_container_width=True, type="primary", disabled=True)
            
        hint_widget(user, "xss", lvl)

    elif lvl == 3:
        st.info(" **MISSIE:** Plant een persistent XSS payload in de comments database")
        st.markdown("""
```
[PERSISTENT XSS]
Met de bewakers afgeleid, heb je toegang tot het internal news portal.
Comments worden opgeslagen in de database en aan alle users getoond.

ACTIE VEREIST: Injecteer een persistent XSS payload in de comments
               Deze wordt uitgevoerd bij ELKE gebruiker die de pagina bezoekt
```
        """)
        
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
            .page{background:#f5f6fa;min-height:340px;max-height:340px;padding:20px 28px;overflow-y:auto;}
            .page::-webkit-scrollbar{width:8px;}
            .page::-webkit-scrollbar-track{background:#e0e0e0;border-radius:4px;}
            .page::-webkit-scrollbar-thumb{background:#1a73e8;border-radius:4px;}
            .page::-webkit-scrollbar-thumb:hover{background:#1557b0;}
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
            @keyframes slideIn{from{opacity:0;transform:translateY(-10px);}to{opacity:1;transform:translateY(0);}}
            .comment.new-comment{animation:slideIn 0.3s ease-out;}
            </style>
            <div class="wrap">
              <div class="screen">
                <div class="inner">
                  <div class="bar">
                    <div class="dot r"></div><div class="dot y"></div><div class="dot g"></div>
                    <div class="url">🔒 news.whitehouse.gov/article/security-briefing#comments</div>
                  </div>
                  <div class="topbar">
                    <div class="logo">White<span>House</span> News</div>
                    <div class="user"><div class="av">G</div><span>guest (you)</span></div>
                  </div>
                  <div class="page">
                    <h2>Security Briefing: Q1 2025 Protocols</h2>
                    <p class="sub">Posted Jan 15, 2025 — 2 comments</p>
                    <div class="comments" id="comments">
                      <div class="comment"><div class="author">Sarah Chen</div><div class="text">Important update, thanks for sharing.</div></div>
                      <div class="comment"><div class="author">Marcus Rodriguez</div><div class="text">When will this be deployed to production systems?</div></div>
                    </div>
                    <div class="comment-form">
                      <label>Post a Comment (saved to database):</label>
                      <textarea id="commentInput" rows="3" placeholder="Write your comment..."></textarea>
                      <button class="post-btn" onclick="postComment()">💬 Post Comment</button>
                      <div class="xss-banner" id="xssBanner">✅ PERSISTENT XSS SUCCESS! Payload stored in database and executed for ALL users!</div>
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
                const page = document.querySelector('.page');
                const div = document.createElement('div');
                div.className = 'comment new-comment';
                div.style.borderColor = val.toLowerCase().includes('<script>') ? '#28a745' : '#e0e0e0';
                div.innerHTML = '<div class="author" style="color:#e74c3c">you (attacker)</div><div class="text">' + val + '</div>';
                comments.appendChild(div);
                
                // Scroll to the new comment
                setTimeout(() => {
                    div.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
                
                if (val.toLowerCase().includes('<script>')) {
                    banner.style.display = 'block';
                    banner.innerHTML = '✅ PERSISTENT XSS SUCCESS!<br><br><strong style="font-size:14px;">➡️ De groene knop is nu actief! Scroll naar beneden om de flag te claimen.</strong>';
                    // Show the persistent XSS alert
                    setTimeout(() => alert('🚨 PERSISTENT XSS! This payload is now stored in the database and will execute for EVERY user who visits!'), 100);
                    
                    // Set flag in localStorage and reload
                    localStorage.setItem('xss3_unlocked', 'true');
                    setTimeout(() => location.reload(), 1000);
                }
                
                // Clear the input
                document.getElementById('commentInput').value = '';
            }
            document.getElementById('commentInput').addEventListener('keydown', e => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); postComment(); }
            });
            </script>
            """, height=560)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if has_completed(user, "xss"):
            st.success("🏴 FLAG BEHAALD: **N75 ZS** — Ga naar volgende kamer")
        else:
            # Check if unlocked via localStorage
            unlock_check = components.html("""
            <script>
            const unlocked = localStorage.getItem('xss3_unlocked') === 'true';
            if (unlocked) {
                localStorage.removeItem('xss3_unlocked');
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
            } else {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
            }
            </script>
            """, height=0)
            
            if unlock_check:
                if st.button("🏴 CLAIM FLAG", key="xss3_continue", use_container_width=True, type="primary"):
                    fake_progress("PAYLOAD OPSLAAN IN DATABASE")
                    give_flag(user, "xss", "N75 ZS")
                    typewriter_terminal([
                        "[+] Payload opgeslagen in database",
                        "[+] Script wordt uitgevoerd bij elke paginabezoek",
                        "[+] Alle White House staff is nu gecompromitteerd!",
                        "[✓] PERSISTENT XSS GESLAAGD",
                        "[✓] GEHEIME CODE GEVONDEN: N75 ZS"
                    ])
                    st.rerun()
            else:
                st.info("💡 Voer eerst de XSS payload uit in de comment box hierboven. De knop wordt actief zodra de alert verschijnt.")
                st.button("CLAIM FLAG", key="xss3_continue_disabled", use_container_width=True, type="primary", disabled=True)
            
        hint_widget(user, "xss", lvl)

# ==========================================================
# KAMER 3, DE BEVEILIGDE RUIMTE - PRIVILEGE ESCALATION
# ==========================================================
with tabs[2]:
    st.header("DE BEVEILIGDE KAMER")
    st.markdown("*Verhoog je rechten om toegang te krijgen tot classified systems.*")
    
    lvl = get_level(user, "privesc")
    st.progress(min((lvl-1)/3, 1.0), text=f"Voortgang: Stap {min(lvl,3)}/3")

    if lvl == 1:
        # Show intro video before PrivEsc Level 1
        check_and_show_video("privesc", 1, "before")
        
        st.info("**MISSIE:** Identificeer hoe je hogere privileges kunt verkrijgen")
        st.markdown("""
```
[INFORMATIE]
Status: Ingelogd als: guest
Current Privileges: READ_ONLY
Doel: Verkrijg ADMIN rechten
Bevinding: Rolbeheer systeem bevat misconfiguratie

ACTIE VEREIST: Identificeer het type aanval
```
        """)
        st.markdown("**Welk type aanval verschaft hogere gebruikersrechten in een systeem?**")
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
                st.error("Incorrect. Hoe noem je het verhogen van gebruikersrechten?")
        hint_widget(user, "privesc", lvl)

    elif lvl == 2:
        st.info("**MISSIE:** Manipuleer de API request om je rol te veranderen naar admin")
        st.markdown("""
```
[EXPLOIT FASE]
De profile update API accepteert een 'role' parameter.
De server controleert NIET of de gebruiker deze mag wijzigen!

ACTIE VEREIST: Wijzig de role parameter van 'user' naar 'admin'
```
        """)
        
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
                    <div class="url">🔧 Browser DevTools — api.whitehouse.gov/profile/update</div>
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
                        <div class="panel-title">REQUEST — Edit the 'role' parameter:</div>
                        <div class="http-block">
                          <span class="http-method">POST</span> /api/profile/update HTTP/1.1<br>
                          <span class="http-header">Host:</span> api.whitehouse.gov<br>
                          <span class="http-header">Content-Type:</span> application/json<br>
                          <span class="http-header">Authorization:</span> Bearer eyJhb...<br>
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
                          <span style="color:#666;">— Awaiting request —</span>
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
                    resp.innerHTML = '<span class="status-ok">200 OK</span> — 42ms<br><br>{<br>&nbsp;&nbsp;"status": "success",<br>&nbsp;&nbsp;"username": "guest",<br>&nbsp;&nbsp;<span class="highlight">"role": "admin"</span>,<br>&nbsp;&nbsp;"message": "Profile updated"<br>}<br><br><span style="color:#66bb6a;">✅ Server accepted role change!<br><br><strong style="font-size:14px;">➡️ De groene knop is nu actief! Scroll naar beneden.</strong></span>';
                    
                    // Set flag in localStorage and reload
                    localStorage.setItem('priv2_unlocked', 'true');
                    setTimeout(() => location.reload(), 1000);
                } else if (role === '') {
                    resp.innerHTML = '<span class="status-err">400 Bad Request</span><br><br>{"error": "role cannot be empty"}';
                } else {
                    resp.innerHTML = '<span class="status-ok">200 OK</span> — 28ms<br><br>{<br>&nbsp;&nbsp;"status": "success",<br>&nbsp;&nbsp;"username": "guest",<br>&nbsp;&nbsp;"role": "' + role + '",<br>&nbsp;&nbsp;"message": "Profile updated"<br>}<br><br><span style="color:#888;">No admin privileges gained.</span>';
                }
            }
            </script>
            """, height=520)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Check if unlocked via localStorage
        unlock_check = components.html("""
        <script>
        const unlocked = localStorage.getItem('priv2_unlocked') === 'true';
        if (unlocked) {
            localStorage.removeItem('priv2_unlocked');
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
        } else {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
        }
        </script>
        """, height=0)
        
        if unlock_check:
            if st.button("GA DOOR NAAR LEVEL 3", key="priv2_continue", use_container_width=True, type="primary"):
                fake_progress("PRIVILEGES ESCALEREN")
                set_level(user, "privesc", 3)
                typewriter_terminal([
                    "[+] Rolparameter gewijzigd: user → admin",
                    "[+] Server accepteert nieuwe rol zonder verificatie",
                    "[✓] ADMIN PRIVILEGES VERKREGEN"
                ])
                st.rerun()
        else:
            st.info("💡 Voer eerst de privilege escalation uit in de DevTools hierboven. De knop wordt actief zodra 'admin' role is ingesteld.")
            st.button("GA DOOR NAAR LEVEL 3", key="priv2_continue_disabled", use_container_width=True, type="primary", disabled=True)
            
        hint_widget(user, "privesc", lvl)

    elif lvl == 3:
        st.info("**MISSIE:** Installeer een backdoor voor permanente toegang")
        st.markdown("""
```
[PERSISTENCE]
Je hebt nu admin rechten, maar deze zijn tijdelijk.

ACTIE VEREIST: Voer een commando uit om een backdoor te installeren
               voor permanente toegang
```
        """)
        
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
                    <div class="url">root@whitehouse-srv01:~# — SSH Admin Session</div>
                  </div>
                  <div class="terminal">
                    <div class="term-bar"><span>bash — root@whitehouse-srv01</span></div>
                    <div class="term-output" id="output">
<span class="dim">Last login: Wed Jan 15 14:23:11 2025 from 10.0.0.42</span><br>
<span class="yellow">root@whitehouse-srv01:~#</span> whoami<br>
<span class="bright">root</span><br>
<span class="yellow">root@whitehouse-srv01:~#</span> pwd<br>
<span class="bright">/root</span><br>
<span class="yellow">root@whitehouse-srv01:~#</span> <span class="dim">Enter command to establish persistent access...</span><br>
                    </div>
                    <div class="term-input-row">
                      <span class="term-prompt">root@whitehouse-srv01:~#</span>
                      <input class="term-input" id="termInput" type="text" placeholder="command..." onkeydown="if(event.key==='Enter')runCmd()">
                    </div>
                  </div>
                </div>
              </div>
              <div class="hinge"></div>
              <div class="base"></div>
            </div>
            <script>
            const validCmds = ['backdoor', 'install', 'persist', 'crontab', 'ssh-keygen', 'authorized_keys', 'netcat', 'nc', 'chmod', 'cron'];
            function runCmd() {
                const inp = document.getElementById('termInput');
                const out = document.getElementById('output');
                const cmd = inp.value.trim();
                inp.value = '';
                const isValid = validCmds.some(v => cmd.toLowerCase().includes(v));
                out.innerHTML += '<span class="yellow">root@whitehouse-srv01:~#</span> ' + cmd + '<br>';
                if (cmd === '') return;
                if (cmd.toLowerCase() === 'ls' || cmd.toLowerCase() === 'ls -la') {
                    out.innerHTML += '<span class="bright">backdoor_installer.sh &nbsp; config/ &nbsp; .ssh/ &nbsp; logs/</span><br>';
                } else if (cmd.toLowerCase() === 'whoami') {
                    out.innerHTML += '<span class="bright">root</span><br>';
                } else if (cmd.toLowerCase().includes('cat') || cmd.toLowerCase().includes('help')) {
                    out.innerHTML += '<span class="dim">Try: ./backdoor_installer.sh, crontab -e, or ssh-keygen</span><br>';
                } else if (isValid) {
                    out.innerHTML += '<span class="green">[+] Executing...</span><br>';
                    out.innerHTML += '<span class="green">[+] Backdoor installed: /usr/bin/.hidden_access</span><br>';
                    out.innerHTML += '<span class="green">[+] Cron job created for persistence</span><br>';
                    out.innerHTML += '<span class="green">[✓] PERSISTENT ACCESS ESTABLISHED</span><br>';
                    out.innerHTML += '<br><span class="bright" style="font-size:14px;">➡️ De groene knop is nu actief! Scroll naar beneden om de flag te claimen.</span><br>';
                    out.scrollTop = out.scrollHeight;
                    
                    // Set flag in localStorage and reload
                    localStorage.setItem('priv3_unlocked', 'true');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    out.innerHTML += '<span class="dim">bash: ' + cmd + ': command not found</span><br>';
                }
                out.scrollTop = out.scrollHeight;
            }
            </script>
            """, height=520)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Check if unlocked via localStorage
        unlock_check = components.html("""
        <script>
        const unlocked = localStorage.getItem('priv3_unlocked') === 'true';
        if (unlocked) {
            localStorage.removeItem('priv3_unlocked');
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
        } else {
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
        }
        </script>
        """, height=0)
        
        valid_commands = ['backdoor', 'install', 'persist', 'crontab', 'ssh-keygen', 'authorized', 'netcat', 'nc', 'chmod', 'cron', 'bash']
        
        if has_completed(user, "privesc"):
            st.success("🏴 FLAG BEHAALD: **ZIF VH** — Ga naar volgende kamer")
        else:
            # Check if unlocked via localStorage
            unlock_check = components.html("""
            <script>
            const unlocked = localStorage.getItem('priv3_unlocked') === 'true';
            if (unlocked) {
                localStorage.removeItem('priv3_unlocked');
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: true}, '*');
            } else {
                window.parent.postMessage({type: 'streamlit:setComponentValue', value: false}, '*');
            }
            </script>
            """, height=0)
            
            if unlock_check:
                if st.button("🏴 CLAIM FLAG", key="priv3_continue", use_container_width=True, type="primary"):
                    fake_progress("BACKDOOR INSTALLEREN")
                    give_flag(user, "privesc", "ZIF VH")
                    typewriter_terminal([
                        "[+] Admin token opgeslagen",
                        "[+] Backdoor geïnstalleerd: /usr/bin/.hidden_access",
                        "[+] Cron job gecreëerd voor persistence",
                        "[✓] PERMANENTE TOEGANG VERKREGEN",
                        "[✓] GEHEIME CODE GEVONDEN: ZIF VH"
                    ])
                    st.rerun()
            else:
                st.info("💡 Voer eerst een persistence commando uit in de terminal hierboven. De knop wordt actief zodra de backdoor is geïnstalleerd.")
                st.button("CLAIM FLAG", key="priv3_continue_disabled", use_container_width=True, type="primary", disabled=True)
            
        hint_widget(user, "privesc", lvl)

# ==========================================================
# KAMER 4, Trump's kamer - encryptie
# ==========================================================
with tabs[3]:
    st.header("TRUMP'S KAMER - CRYPTOGRAFIE")
    st.markdown("*Kraak Trump's persoonlijke kluis.*")

    rooms_complete = [has_completed(user, r) for r in ["sql", "xss", "privesc"]]
    if not all(rooms_complete):
        missing = [r.upper() for r, done in zip(["Kamer 1","Kamer 2","kamer 3"], rooms_complete) if not done]
        st.error(f"⛔ TOEGANG GEWEIGERD — Voltooi eerst alle vorige missies: {', '.join(missing)}")
        st.stop()

    lvl = get_level(user, "crypto")
    st.progress(min((lvl-1)/4, 1.0), text=f"Voortgang: Stap {min(lvl,4)}/4")

    if lvl == 1:
        # Show intro video before Crypto Level 1
        check_and_show_video("crypto", 1, "before")
        
        st.info(" **MISSIE:** Identificeer het encryption systeem van de kluis")
        st.markdown("""
```
[FINAL CHALLENGE]
Locatie: Presidential Suite — Trump's privé ruimte
Beveiligingsniveau: MAXIMUM
Doelwit: Encrypted vault password
Bevinding: Klassiek versleutelingssysteem gedetecteerd

De kluis is beveiligd met een oud maar effectief encryption system.
Alle verzamelde codes zijn versleuteld met hetzelfde systeem.

ACTIE VEREIST: Identificeer het encryption algoritme
```
        """)
        st.markdown("**Welk klassiek versleutelingssysteem verschuift letters in het alfabet?**")
        cmd = st.text_input("analysis>", key="crypto1", placeholder="naam van het systeem...")
        if st.button("▶ ANALYSEER", key="crypto1_btn"):
            if "caesar" in cmd.lower():
                fake_progress("ENCRYPTIE IDENTIFICEREN")
                set_level(user, "crypto", 2)
                typewriter_terminal([
                    "[+] Caesar cipher geïdentificeerd",
                    "[+] Klassieke verschuivingscodering",
                    "[+] Shift value: detectie in progress...",
                    "[!] Decryptie vereist..."
                ])
                st.rerun()
            else:
                st.error("Incorrect. Welke Romeinse keizer stond bekend om zijn geheime code?")
        hint_widget(user, "crypto", lvl)

    elif lvl == 2:
        st.info(" **RAADSEL:** Ontcijfer de kolomtranspositie code")
        st.markdown("""
```
[DUBBELE BEVEILIGING]
De kluis heeft een tweede laag beveiliging: kolomtranspositie.

Code: MAAUANST!AGGKRAEEI
Sleutelwoord: Epstein (te vinden in de video)

INSTRUCTIES:
1. Haal dubbele letters uit sleutelwoord: EPSTEIN → EPSTIN
2. Nummer de letters alfabetisch: E=1, P=4, S=5, T=6, I=2, N=3
3. Lees de code in kolommen volgens de nummering
```
        """)
        cmd = st.text_input("decrypt>", key="crypto_kolomtransp", placeholder="ontcijferd wachtwoord...")
        if st.button("▶ CONTROLEER", key="crypto2_check"):
            if cmd.strip().upper() == "MAKEUSAGREATAGAIN!":
                fake_progress("KOLOMTRANSPOSITIE DECODEREN")
                set_level(user, "crypto", 3)
                typewriter_terminal([
                    "[+] Kolomtranspositie ontcijferd",
                    "[+] Sleutelwoord: EPSTIN",
                    "[+] Code: MAKE USA GREAT AGAIN!",
                    "[✓] TWEEDE BEVEILIGINGSLAAG DOORBROKEN"
                ])
                st.rerun()
            else:
                st.error("❌ Incorrect. Volg de instructies zorgvuldig.")
        hint_widget(user, "crypto", lvl)

    elif lvl == 3:
        st.info(" **MISSIE:** Decodeer de verzamelde codes en combineer ze tot het vault wachtwoord")
        st.markdown("**Je hebt deze versleutelde codes verzameld tijdens je missies:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.code("GV 71", language=None)
            st.caption("Receptie - SQL Injection")
        with col2:
            st.code("N75 ZS", language=None)
            st.caption("Vergaderruimte - XSS")
        with col3:
            st.code("ZIF VH", language=None)
            st.caption("Beveiligde Kamer - PrivEsc")
        
        st.markdown("""
```
[DECRYPTION INSTRUCTIONS]
Caesar cipher verschuift elke letter een vast aantal posities.
Probeer verschillende shift values (bijvoorbeeld ROT13 = 13 posities).

HINT: Decodeer elke code afzonderlijk en combineer de resultaten.
FORMAAT EINDWACHTWOORD: EXAMENKLAS[JAAR]

Bijvoorbeeld:  GV → ??
               N75 → ???  
               ZIF → ???
```
        """)
        cmd = st.text_input("decrypt>", key="crypto2", placeholder="eindwachtwoord...")
        if st.button("▶ ONTSLEUTEL VAULT", key="crypto2_btn", use_container_width=True):
            if cmd.strip().upper() == "EXAMENKLAS2026":
                fake_progress("VAULT ONTGRENDELEN")
                set_level(user, "crypto", 4)
                typewriter_terminal([
                    "[+] Wachtwoord correct",
                    "[+] Caesar shift decoded: ROT7",
                    "[+] GV 71 → EX AM",
                    "[+] N75 ZS → EN KL",
                    "[+] ZIF VH → AS 20",
                    "[+] Combined: EXAMENKLAS 2026",
                    "[+] Vault ontgrendeld...",
                    "",
                    "  ████████████████████████████████",
                    "  █  🏆 MISSIE VOLTOOID 🏆      █",
                    "  █  White House Gecompromitteerd █",
                    "  ████████████████████████████████",
                ])
                give_flag(user, "crypto", "EXAMENKLAS2026")
                st.success(" **EINDCODE GEACCEPTEERD — ALLE SYSTEMEN GECOMPROMITTEERD!**")
                st.balloons()
                components.html("<script>setTimeout(()=>window.playSuccess&&window.playSuccess(),100);</script>", height=0)
            else:
                st.error("❌ Verkeerde code. Decodeer alle vlaggen en combineer ze correct.")
        hint_widget(user, "crypto", lvl)

    elif lvl >= 4:
        st.success("**KLUIS GEOPEND — MISSIE VOLTOOID!**")
        
        # Show finale video after completing everything
        check_and_show_video("crypto", level=None, position="complete")
        
        # Vault animation
        components.html("""
        <style>
        .vault-container{display:flex;justify-content:center;align-items:center;padding:40px 0;}
        .vault{position:relative;width:300px;height:300px;background:linear-gradient(135deg,#2c3e50,#34495e);border-radius:50%;box-shadow:0 20px 60px rgba(0,0,0,0.5),inset 0 0 40px rgba(0,0,0,0.3);animation:vault-open 2s ease-out;}
        .vault::before{content:'';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:200px;height:200px;background:radial-gradient(circle,#1a252f,#0f1419);border-radius:50%;box-shadow:inset 0 0 30px rgba(0,0,0,0.8);}
        .vault-door{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:180px;height:180px;background:linear-gradient(135deg,#34495e,#2c3e50);border-radius:50%;box-shadow:0 10px 30px rgba(0,0,0,0.5);animation:door-swing 2s ease-out forwards;}
        .vault-handle{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:40px;height:40px;background:radial-gradient(circle,#e74c3c,#c0392b);border-radius:50%;box-shadow:0 5px 15px rgba(231,76,60,0.5);animation:handle-spin 2s ease-out;}
        .vault-contents{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:48px;opacity:0;animation:contents-appear 1s ease-out 2s forwards;}
        @keyframes vault-open{
            0%{transform:scale(1);}
            50%{transform:scale(1.05);}
            100%{transform:scale(1);}
        }
        @keyframes door-swing{
            0%{transform:translate(-50%,-50%) rotateY(0deg);}
            100%{transform:translate(-200%,-50%) rotateY(-90deg);}
        }
        @keyframes handle-spin{
            0%{transform:translate(-50%,-50%) rotate(0deg);}
            100%{transform:translate(-50%,-50%) rotate(720deg);}
        }
        @keyframes contents-appear{
            0%{opacity:0;transform:translate(-50%,-50%) scale(0.5);}
            100%{opacity:1;transform:translate(-50%,-50%) scale(1);}
        }
        </style>
        <div class="vault-container">
            <div class="vault">
                <div class="vault-door">
                    <div class="vault-handle"></div>
                </div>
                <div class="vault-contents">🏆</div>
            </div>
        </div>
        """, height=400)
        
        typewriter_terminal([
            "[✓] SQL Injection     — GECOMPROMITTEERD",
            "[✓] XSS               — GECOMPROMITTEERD",
            "[✓] Privilege Esc.    — GECOMPROMITTEERD",
            "[✓] Cryptografie      — GEDECODEERD",
            "",
            "[✓] WHITE HOUSE VOLLEDIG OVERGENOMEN",
            "",
            "GEFELICITEERD!",
            "Je hebt alle systemen gekraakt en toegang tot de hoogste veiligheids-",
            "niveau's verkregen. Dit is het einde van de White House Cyber Escape Room!"
        ])

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")
st.markdown("""
<div style="text-align:center;color:#00ff9c;opacity:0.7;font-family:'Share Tech Mono',monospace;font-size:11px;">
    THE WHITE HOUSE<br>
    Gemaakt door: Anouk, Marwa, Fenna en Noura<br>
    <em>Cybersecurity escape room — 2025</em>
</div>
""", unsafe_allow_html=True)
