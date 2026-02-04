import streamlit as st
import sqlite3
import os
import hashlib
from datetime import datetime

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config("MegaCorp Breach — Cyber Escape Room", layout="wide")

# ==========================================================
# DATABASES
# ==========================================================
def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()

def init_vuln_db():
    if os.path.exists("megacorp.db"):
        return
    conn = sqlite3.connect("megacorp.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT,
        role TEXT
    )""")
    c.executemany(
        "INSERT INTO users VALUES (NULL,?,?,?)",
        [
            ("jdoe","welcome123","user"),
            ("asmith","password1","user"),
            ("admin","SuperSecret!","admin")
        ]
    )
    conn.commit(); conn.close()

def init_platform_db():
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS progress (
        username TEXT,
        category TEXT,
        level INTEGER,
        PRIMARY KEY(username,category)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS flags (
        username TEXT,
        category TEXT,
        flag TEXT,
        time TEXT
    )""")
    users = [
        ("alice",hash_pw("student123"),"student"),
        ("bob",hash_pw("student123"),"student"),
        ("teacher",hash_pw("teach123"),"teacher")
    ]
    for u in users:
        c.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)",u)
    conn.commit(); conn.close()

init_vuln_db()
init_platform_db()

# ==========================================================
# VULNERABLE LAB FUNCTIONS
# ==========================================================
def insecure_login(u,p):
    conn = sqlite3.connect("megacorp.db")
    c = conn.cursor()
    q = f"SELECT username,role FROM users WHERE username='{u}' AND password='{p}'"
    try: r = c.execute(q).fetchall()
    except Exception as e: r = str(e)
    conn.close(); return r

def insecure_lookup(u):
    conn = sqlite3.connect("megacorp.db")
    c = conn.cursor()
    q = f"SELECT username,password,role FROM users WHERE username='{u}'"
    try: r = c.execute(q).fetchall()
    except Exception as e: r = str(e)
    conn.close(); return r

# ==========================================================
# PLATFORM FUNCTIONS
# ==========================================================
def auth(u,p):
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE username=? AND password=?", (u,hash_pw(p)))
    r = c.fetchone()
    conn.close(); return r[0] if r else None

def load_progress(u):
    base = {"sql":1,"xss":1,"privesc":1,"crypto":1}
    conn = sqlite3.connect("platform.db")
    c = conn.cursor()
    for cat,lvl in c.execute("SELECT category,level FROM progress WHERE username=?", (u,)):
        base[cat]=lvl
    conn.close(); return base

def save_progress(u,c,l):
    conn = sqlite3.connect("platform.db")
    c2 = conn.cursor()
    c2.execute("""INSERT INTO progress VALUES (?,?,?)
                  ON CONFLICT(username,category)
                  DO UPDATE SET level=?""",(u,c,l,l))
    conn.commit(); conn.close()

def save_flag(u,c,f):
    conn = sqlite3.connect("platform.db")
    c2 = conn.cursor()
    c2.execute("INSERT INTO flags VALUES (?,?,?,?)",(u,c,f,datetime.now().isoformat()))
    conn.commit(); conn.close()

# ==========================================================
# SESSION
# ==========================================================
for k in ["user","role","progress","flags","xss_store"]:
    if k not in st.session_state:
        st.session_state[k] = {} if k in ["progress","flags","xss_store"] else None

# ==========================================================
# LOGIN
# ==========================================================
if not st.session_state.user:
    st.title("🏢 MegaCorp Breach — Cyber Escape Room")
    s,t = st.tabs(["🎓 Student","🧑‍🏫 Teacher"])
    with s:
        u = st.text_input("Username", key="stu_username"); p = st.text_input("Password",type="password", key="stu_password")
        if st.button("Enter Facility", key="stu_login"):
            if auth(u,p)=="student":
                st.session_state.user=u
                st.session_state.role="student"
                st.session_state.progress[u]=load_progress(u)
                st.session_state.flags[u]={}
                st.rerun()
            else: st.error("Access denied")
    with t:
        u = st.text_input("Teacher Username", key="teach_username"); p = st.text_input("Password",type="password", key="teach_password")
        if st.button("Enter Control Room", key="teach_login"):
            if auth(u,p)=="teacher":
                st.session_state.user=u; st.session_state.role="teacher"; st.rerun()
            else: st.error("Access denied")
    st.stop()

# ==========================================================
# TEACHER DASHBOARD
# ==========================================================
if st.session_state.role=="teacher":
    st.title("🧑‍🏫 Control Room — Teacher View")
    conn = sqlite3.connect("platform.db")
    rows = conn.execute("SELECT * FROM progress").fetchall()
    conn.close()
    st.table(rows)
    if st.button("Logout"): st.session_state.clear(); st.rerun()
    st.stop()

# ==========================================================
# STUDENT VIEW
# ==========================================================
u = st.session_state.user
p = st.session_state.progress[u]

st.title(f"🎓 Operative: {u}")
tabs = st.tabs(["🗺️ Facility Map","🚪 SQL Front Desk","🖥️ Internal Portal","🧑‍💻 Control Room","🔐 Vault"])

# ==========================================================
# MAP
# ==========================================================
with tabs[0]:
    for c in ["sql","xss","privesc","crypto"]:
        st.markdown(f"**{c.upper()}** — Level {p[c]}/3")

# ==========================================================
# SQL ROOM
# ==========================================================
with tabs[1]:
    st.header("🚪 Front Desk System")

    if p["sql"]==1:
        st.markdown("""
You stand at MegaCorp’s **employee login terminal**.
A sticky note nearby reads:

> *“Passwords are checked directly in the query — quick and dirty.”*
""")
        a = st.text_input("Identify the weakness")
        with st.expander("📄 Dev Note"):
            st.markdown("User input is concatenated into SQL statements.")
        if st.button("Unlock"):
            if "sql" in a.lower():
                p["sql"]=2; save_progress(u,"sql",2); st.rerun()

    elif p["sql"]==2:
        st.markdown("""
The login terminal flickers.
You don’t know any passwords… but logic still works.
""")
        u2=st.text_input("Username", key="sql_l2_username"); p2=st.text_input("Password", key="sql_l2_password")
        with st.expander("📄 Log File"):
            st.markdown("`WHERE username='X' AND password='Y'`")
        if st.button("Bypass", key="sql_l2_bypass"):
            if insecure_login(u2,p2):
                p["sql"]=3; save_progress(u,"sql",3); st.rerun()

    else:
        st.markdown("""
You find a **user lookup console** used by IT.
It returns database rows directly.
""")
        inj=st.text_input("Lookup user", key="sql_l3_lookup")
        with st.expander("📄 Old SQL Manual"):
            st.markdown("UNION merges result sets.")
        if st.button("Query", key="sql_l3_query"):
            st.code(insecure_lookup(inj))
        au=st.text_input("Admin username", key="sql_l3_au"); ap=st.text_input("Admin password", key="sql_l3_ap")
        if st.button("Enter Admin", key="sql_l3_enter"):
            if "admin" in str(insecure_login(au,ap)):
                st.success("FLAG-SQL-REAL")
                save_flag(u,"sql","FLAG-SQL-REAL")

# ==========================================================
# XSS ROOM
# ==========================================================
with tabs[2]:
    st.header("🖥️ Internal Employee Portal")

    if p["xss"]==1:
        st.markdown("""
Employees complain the portal **shows their input exactly as typed**.
""")
        a=st.text_input("What could go wrong?", key="xss_l1_input")
        with st.expander("📄 Security Memo"):
            st.markdown("HTML is rendered without encoding.")
        if st.button("Continue", key="xss_l1_continue"):
            if "xss" in a.lower():
                p["xss"]=2; save_progress(u,"xss",2); st.rerun()

    elif p["xss"]==2:
        q=st.text_input("Search portal", key="xss_l2_search")
        if st.button("Search", key="xss_l2_search_btn"):
            st.markdown(f"Result: {q}",unsafe_allow_html=True)
            if "<" in q:
                p["xss"]=3; save_progress(u,"xss",3); st.rerun()

    else:
        c=st.text_area("Leave comment", key="xss_l3_comment")
        if st.button("Post", key="xss_l3_post"):
            st.session_state.xss_store.setdefault(u,[]).append(c)
        st.markdown("### Admin reviewing comments")
        for x in st.session_state.xss_store.get(u,[]):
            st.markdown(x,unsafe_allow_html=True)
            if "<script>" in x:
                st.success("FLAG-XSS-REAL")
                save_flag(u,"xss","FLAG-XSS-REAL")

# ==========================================================
# PRIV ESC ROOM
# ==========================================================
with tabs[3]:
    st.header("🧑‍💻 Control Room")

    if p["privesc"]==1:
        st.markdown("""
You’re logged in… but doors are locked.
Access checks seem weak.
""")
        a=st.text_input("What class of vulnerability?", key="privesc_l1_input")
        with st.expander("📄 Audit Report"):
            st.markdown("Authorization enforced client-side.")
        if st.button("Proceed", key="privesc_l1_proceed"):
            if "access" in a.lower():
                p["privesc"]=2; save_progress(u,"privesc",2); st.rerun()

    elif p["privesc"]==2:
        st.markdown("""
A request editor shows the role being sent to the server.
""")
        r=st.selectbox("Role parameter",["user","admin"], key="privesc_l2_role")
        if st.button("Send", key="privesc_l2_send"):
            if r=="admin":
                p["privesc"]=3; save_progress(u,"privesc",3); st.rerun()

    else:
        st.markdown("""
Admin console unlocked.
Role changes persist.
""")
        if st.button("Escalate Permanently", key="privesc_l3_escalate"):
            st.success("FLAG-PRIVESC-REAL")
            save_flag(u,"privesc","FLAG-PRIVESC-REAL")

# ==========================================================
# CRYPTO ROOM
# ==========================================================
with tabs[4]:
    st.header("🔐 Backup Vault")

    if p["crypto"]==1:
        st.code("PLAINTEXT: ATTACKATDAWN\nENCRYPTED: DWWDFNDWGDZQ")
        a=st.text_input("Encryption used?", key="crypto_l1_input")
        with st.expander("📄 Old Manual"):
            st.markdown("Shift-based substitution.")
        if st.button("Identify", key="crypto_l1_identify"):
            if "caesar" in a.lower():
                p["crypto"]=2; save_progress(u,"crypto",2); st.rerun()

    elif p["crypto"]==2:
        st.code("CRAGRFGJVA")
        a=st.text_input("Decrypt", key="crypto_l2_decrypt")
        with st.expander("📄 Tool Bookmark"):
            st.markdown("https://www.dcode.fr/rot-cipher")
        if st.button("Unlock", key="crypto_l2_unlock"):
            if a.upper()=="PENTESTWIN":
                p["crypto"]=3; save_progress(u,"crypto",3); st.rerun()

    else:
        if st.button("Open Vault", key="crypto_l3_open"):
            st.success("🏁 FINAL FLAG: PENTEST-WIN")
            save_flag(u,"crypto","PENTEST-WIN")

# ==========================================================
# LOGOUT
# ==========================================================
if st.button("Exit Facility"):
    st.session_state.clear()
    st.rerun()
