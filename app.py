import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import hashlib
from datetime import datetime

# ==========================================================
# CONFIG
# ==========================================================
st.set_page_config("Cyber Escape Room", layout="wide")

# ==========================================================
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
    st.title("CYBER ESCAPE ROOM")

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
