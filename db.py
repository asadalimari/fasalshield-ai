# -*- coding: utf-8 -*-
"""FasalShield AI — MySQL database layer (v9).

Database: fasalshield_db (MySQL / MariaDB — XAMPP par local, ya cloud MySQL).

Design (dual mode — yehi is project ki jaan hai):
  1) Agar MySQL chal raha hai to app data DATABASE se parhta hai, aur har
     leaf scan / irrigation advice database me save bhi hota hai.
  2) Agar MySQL NA mile (online Streamlit Cloud, ya XAMPP band ho) to app
     knowledge.py ki built-in copy use karta hai — app KABHI band nahi hota,
     photo detection hamesha chalta hai.

Pehli dafa MySQL milne par app khud database + tables bana kar seed data
(38 diseases, crops, calendar, contacts...) bhar deta hai. Wahi kaam
fasalshield_db.sql file se phpMyAdmin me haath se bhi ho sakta hai.

Connection settings (pehle jo mile):
  - Streamlit secrets:  [mysql] host/user/password/database/port
  - Environment:        FASAL_MYSQL_HOST / _USER / _PASSWORD / _DB / _PORT
  - Default (XAMPP):    127.0.0.1, root, (khaali password), fasalshield_db
"""
import os
import time

import knowledge

DB_NAME_DEFAULT = "fasalshield_db"

_state = {"checked_at": 0.0, "available": False, "initialised": False}
CHECK_TTL = 45  # seconds — har click par dobara try karke app slow na ho


def _config():
    cfg = {"host": os.environ.get("FASAL_MYSQL_HOST", "127.0.0.1"),
           "port": int(os.environ.get("FASAL_MYSQL_PORT", "3306")),
           "user": os.environ.get("FASAL_MYSQL_USER", "root"),
           "password": os.environ.get("FASAL_MYSQL_PASSWORD", ""),
           "database": os.environ.get("FASAL_MYSQL_DB", DB_NAME_DEFAULT)}
    try:  # Streamlit Cloud secrets (agar user ne lagaye hon)
        import streamlit as st
        if "mysql" in st.secrets:
            s = dict(st.secrets["mysql"])
            for k in ("host", "user", "password", "database"):
                if s.get(k):
                    cfg[k] = s[k]
            if s.get("port"):
                cfg["port"] = int(s["port"])
    except Exception:
        pass
    return cfg


def _connect(with_db=True):
    import pymysql
    cfg = _config()
    kw = dict(host=cfg["host"], port=cfg["port"], user=cfg["user"],
              password=cfg["password"], charset="utf8mb4",
              connect_timeout=3, read_timeout=6, write_timeout=6,
              autocommit=True)
    if with_db:
        kw["database"] = cfg["database"]
    return pymysql.connect(**kw)


# ----------------------------- schema -----------------------------
TABLES_SQL = [
    """CREATE TABLE IF NOT EXISTS diseases (
        disease_id INT AUTO_INCREMENT PRIMARY KEY,
        label VARCHAR(160) NOT NULL UNIQUE,
        plant VARCHAR(80) NOT NULL,
        is_healthy TINYINT(1) NOT NULL DEFAULT 0,
        treatment_en TEXT, prevention_en TEXT,
        advice_ur TEXT, advice_sd TEXT, advice_ur_script TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS crops (
        crop_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL UNIQUE,
        daily_litres_per_acre INT NOT NULL,
        kc DECIMAL(4,2) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS soil_factors (
        soil_id INT AUTO_INCREMENT PRIMARY KEY,
        soil_name VARCHAR(80) NOT NULL UNIQUE,
        factor DECIMAL(4,2) NOT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS fertilizer_plans (
        plan_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL UNIQUE,
        dap_bags DECIMAL(5,2) NULL, urea_bags DECIMAL(5,2) NULL, sop_bags DECIMAL(5,2) NULL,
        timing TEXT, per_plant_text TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS crop_calendar (
        cal_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL UNIQUE,
        season VARCHAR(60), sowing TEXT, harvest TEXT, seed_rate TEXT,
        sowing_en TEXT, harvest_en TEXT, seed_en TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS dept_contacts (
        contact_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(160) NOT NULL, org VARCHAR(200), phone VARCHAR(40),
        address VARCHAR(200), timing VARCHAR(80), note TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS risk_rules (
        rule_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL, disease_name VARCHAR(120) NOT NULL,
        kind VARCHAR(40), advice TEXT, advice_en TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS local_guides (
        guide_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL, section_title VARCHAR(160) NOT NULL,
        section_text TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS leaf_scans (
        scan_id INT AUTO_INCREMENT PRIMARY KEY,
        disease_id INT NULL,
        label VARCHAR(160) NOT NULL,
        confidence DECIMAL(5,2) NOT NULL,
        severity_pct DECIMAL(5,2) NULL,
        scan_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_scan_disease FOREIGN KEY (disease_id) REFERENCES diseases(disease_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
    """CREATE TABLE IF NOT EXISTS irrigation_logs (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        crop_name VARCHAR(80) NOT NULL, acres DECIMAL(6,2) NOT NULL,
        traditional_litres DECIMAL(14,2) NOT NULL, advised_litres DECIMAL(14,2) NOT NULL,
        saved_litres DECIMAL(14,2) NOT NULL,
        log_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""",
]


def plant_of(label: str) -> str:
    """'Tomato with Early Blight' -> 'Tomato'; 'Healthy Bell Pepper Plant' -> 'Bell Pepper'."""
    lab = label.replace(" Plant", "")
    if " with " in lab:
        return lab.split(" with ")[0]
    if lab.startswith("Healthy "):
        return lab[len("Healthy "):]
    return lab


def _seed(cur):
    """Tables khaali hon to knowledge.py ke data se bhar do (INSERT IGNORE = dobara safe)."""
    for lab in knowledge.LABELS:
        adv = knowledge.advice_for(lab)
        cur.execute(
            "INSERT IGNORE INTO diseases (label, plant, is_healthy, treatment_en, prevention_en,"
            " advice_ur, advice_sd, advice_ur_script) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (lab, plant_of(lab), 1 if adv["healthy"] else 0, adv["en"], adv["prevention"],
             adv["urdu"], adv["sindhi"], adv["urdu_script"]))
    for name, c in knowledge.CROPS.items():
        cur.execute("INSERT IGNORE INTO crops (crop_name, daily_litres_per_acre, kc) VALUES (%s,%s,%s)",
                    (name, c["daily_litres_per_acre"], c["kc"]))
    for name, f in knowledge.SOIL_FACTOR.items():
        cur.execute("INSERT IGNORE INTO soil_factors (soil_name, factor) VALUES (%s,%s)", (name, f))
    for name, p in knowledge.FERTILIZER_PLANS.items():
        cur.execute("INSERT IGNORE INTO fertilizer_plans (crop_name, dap_bags, urea_bags, sop_bags, timing, per_plant_text)"
                    " VALUES (%s,%s,%s,%s,%s,NULL)",
                    (name, p["dap_bags"], p["urea_bags"], p["sop_bags"], p["timing"]))
    for name, txt in knowledge.FERTILIZER_PER_PLANT.items():
        cur.execute("INSERT IGNORE INTO fertilizer_plans (crop_name, dap_bags, urea_bags, sop_bags, timing, per_plant_text)"
                    " VALUES (%s,NULL,NULL,NULL,NULL,%s)", (name, txt))
    for c in knowledge.CROP_CALENDAR:
        cur.execute("INSERT IGNORE INTO crop_calendar (crop_name, season, sowing, harvest, seed_rate, sowing_en, harvest_en, seed_en)"
                    " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (c["crop"], c["season"], c["sowing"], c["harvest"], c["seed"],
                     c.get("sowing_en"), c.get("harvest_en"), c.get("seed_en")))
    for c in knowledge.DEPT_CONTACTS:
        cur.execute("INSERT IGNORE INTO dept_contacts (name, org, phone, address, timing, note)"
                    " VALUES (%s,%s,%s,%s,%s,%s)",
                    (c["name"], c["org"], c["phone"], c["address"], c["timing"], c["note"]))
    for r in knowledge.RISK_RULES:
        cur.execute("INSERT IGNORE INTO risk_rules (crop_name, disease_name, kind, advice, advice_en) VALUES (%s,%s,%s,%s,%s)",
                    (r["crop"], r["disease"], r["kind"], r["advice"], r.get("advice_en")))
    for crop, g in knowledge.LOCAL_CROP_GUIDES.items():
        for title, text in g["sections"]:
            cur.execute("INSERT IGNORE INTO local_guides (crop_name, section_title, section_text) VALUES (%s,%s,%s)",
                        (crop, title, text))


def _initialise():
    """Database + tables + seed — sirf pehli kamyab connection par."""
    if _state["initialised"]:
        return True
    cfg = _config()
    conn = _connect(with_db=False)
    try:
        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE IF NOT EXISTS `{cfg['database']}`"
                        " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    finally:
        conn.close()
    conn = _connect(with_db=True)
    try:
        with conn.cursor() as cur:
            for sql in TABLES_SQL:
                cur.execute(sql)
            for _tbl, _col in (("crop_calendar", "sowing_en"), ("crop_calendar", "harvest_en"),
                               ("crop_calendar", "seed_en"), ("risk_rules", "advice_en")):
                try:
                    cur.execute(f"ALTER TABLE {_tbl} ADD COLUMN {_col} TEXT")
                except Exception:
                    pass  # column pehle se hai
            cur.execute("SELECT COUNT(*) FROM diseases")
            if cur.fetchone()[0] == 0:
                _seed(cur)
            # purane DBs me English columns khaali hon to bhar do (migration)
            for _c in knowledge.CROP_CALENDAR:
                cur.execute("UPDATE crop_calendar SET sowing_en=%s, harvest_en=%s, seed_en=%s"
                            " WHERE crop_name=%s AND (sowing_en IS NULL OR sowing_en='')",
                            (_c.get("sowing_en"), _c.get("harvest_en"), _c.get("seed_en"), _c["crop"]))
            for _r in knowledge.RISK_RULES:
                cur.execute("UPDATE risk_rules SET advice_en=%s WHERE crop_name=%s AND disease_name=%s"
                            " AND (advice_en IS NULL OR advice_en='')",
                            (_r.get("advice_en"), _r["crop"], _r["disease"]))
    finally:
        conn.close()
    _state["initialised"] = True
    return True


def db_available() -> bool:
    """MySQL chal raha hai aur tables tayyar hain? (result thodi dair cache rehta hai)"""
    now = time.time()
    if now - _state["checked_at"] < CHECK_TTL and _state["checked_at"] > 0:
        return _state["available"]
    ok = False
    try:
        _initialise()
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM diseases")
                ok = cur.fetchone()[0] >= 38
        finally:
            conn.close()
    except Exception:
        ok = False
    _state.update(checked_at=now, available=ok)
    return ok


def _query(sql, params=(), fetch="all"):
    conn = _connect()
    try:
        import pymysql.cursors
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute(sql, params)
            if fetch == "one":
                return cur.fetchone()
            return cur.fetchall()
    finally:
        conn.close()


# ----------------------------- reads -----------------------------
def get_advice(label):
    """Database se treatment — advice_for() jaisi hi shape. Na mile to None (caller fallback lega)."""
    if not db_available():
        return None
    try:
        row = _query("SELECT * FROM diseases WHERE label=%s", (label,), fetch="one")
        if not row:
            return None
        return {"en": row["treatment_en"] or "", "prevention": row["prevention_en"] or "",
                "urdu": row["advice_ur"] or "", "sindhi": row["advice_sd"] or "",
                "urdu_script": row["advice_ur_script"] or "", "healthy": bool(row["is_healthy"])}
    except Exception:
        return None


def get_calendar():
    if not db_available():
        return None
    try:
        rows = _query("SELECT crop_name, season, sowing, harvest, seed_rate, sowing_en, harvest_en, seed_en"
                      " FROM crop_calendar ORDER BY cal_id")
        return [{"crop": r["crop_name"], "season": r["season"], "sowing": r["sowing"],
                 "harvest": r["harvest"], "seed": r["seed_rate"],
                 "sowing_en": r.get("sowing_en"), "harvest_en": r.get("harvest_en"),
                 "seed_en": r.get("seed_en")} for r in rows] or None
    except Exception:
        return None


def get_contacts():
    if not db_available():
        return None
    try:
        rows = _query("SELECT name, org, phone, address, timing, note FROM dept_contacts ORDER BY contact_id")
        return rows or None
    except Exception:
        return None


def search_knowledge(q):
    """LIKE search — diseases + calendar + guides. List of (title, body). Na mile/DB off to None."""
    if not db_available():
        return None
    try:
        like = f"%{q.strip()}%"
        out = []
        for r in _query("SELECT label, treatment_en FROM diseases WHERE label LIKE %s OR treatment_en LIKE %s LIMIT 5",
                        (like, like)):
            out.append((f"🦠 {r['label']}", r["treatment_en"] or ""))
        for r in _query("SELECT crop_name, sowing, harvest FROM crop_calendar WHERE crop_name LIKE %s OR sowing LIKE %s LIMIT 3",
                        (like, like)):
            out.append((f"🗓️ {r['crop_name']}", f"Sowing: {r['sowing']} • Harvest: {r['harvest']}"))
        for r in _query("SELECT crop_name, section_title, section_text FROM local_guides"
                        " WHERE section_text LIKE %s OR section_title LIKE %s LIMIT 3", (like, like)):
            out.append((f"{r['section_title']} — {r['crop_name']}", r["section_text"] or ""))
        return out
    except Exception:
        return None


# ----------------------------- writes -----------------------------
def log_scan(label, confidence_pct, severity_pct):
    """Scan ko leaf_scans me save karo. Kamyab ho to scan_id, warna None."""
    if not db_available():
        return None
    try:
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO leaf_scans (disease_id, label, confidence, severity_pct)"
                    " VALUES ((SELECT disease_id FROM diseases WHERE label=%s), %s, %s, %s)",
                    (label, label, round(float(confidence_pct), 2),
                     None if severity_pct is None else round(float(severity_pct), 2)))
                return cur.lastrowid
        finally:
            conn.close()
    except Exception:
        return None


def log_irrigation(crop, acres, traditional_l, advised_l, saved_l):
    if not db_available():
        return None
    try:
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO irrigation_logs (crop_name, acres, traditional_litres, advised_litres, saved_litres)"
                    " VALUES (%s,%s,%s,%s,%s)",
                    (crop, acres, round(float(traditional_l), 2), round(float(advised_l), 2), round(float(saved_l), 2)))
                return cur.lastrowid
        finally:
            conn.close()
    except Exception:
        return None


def delete_scan(scan_id):
    """Ek scan record delete karo. Kamyab ho to True."""
    if not db_available():
        return False
    try:
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM leaf_scans WHERE scan_id=%s", (int(scan_id),))
                return cur.rowcount > 0
        finally:
            conn.close()
    except Exception:
        return False


def clear_records():
    """Sare scan + irrigation records delete (database khali). (scans, logs) counts return."""
    if not db_available():
        return (0, 0)
    try:
        conn = _connect()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM leaf_scans")
                ds = cur.rowcount
                cur.execute("DELETE FROM irrigation_logs")
                dl = cur.rowcount
                return (ds, dl)
        finally:
            conn.close()
    except Exception:
        return (0, 0)


def get_stats():
    """Records page ke liye asal SQL aggregates: COUNT, SUM, GROUP BY, JOIN."""
    if not db_available():
        return None
    try:
        total = _query("SELECT COUNT(*) AS n FROM leaf_scans", fetch="one")["n"]
        saved = _query("SELECT COALESCE(SUM(saved_litres),0) AS s FROM irrigation_logs", fetch="one")["s"]
        top = _query("SELECT label, COUNT(*) AS n FROM leaf_scans GROUP BY label ORDER BY n DESC LIMIT 5")
        recent = _query(
            "SELECT s.scan_id, s.label, s.confidence, s.severity_pct, s.scan_at, d.plant"
            " FROM leaf_scans s LEFT JOIN diseases d ON s.disease_id = d.disease_id"
            " ORDER BY s.scan_id DESC LIMIT 10")
        return {"total_scans": int(total), "total_saved": float(saved),
                "top_diseases": top, "recent": recent}
    except Exception:
        return None


# ----------------------------- SQL file -----------------------------
def _esc(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    return "'" + str(v).replace("\\", "\\\\").replace("'", "\\'") + "'"


def build_sql_script() -> str:
    """fasalshield_db.sql ka pura script — phpMyAdmin me import ke liye."""
    L = []
    L.append("-- =============================================================")
    L.append("-- FasalShield AI — fasalshield_db (MySQL / MariaDB, XAMPP)")
    L.append("-- Import: phpMyAdmin > Import > ye file choose karein, ya")
    L.append("-- app chalane par database khud bhi ban jata hai (db.py).")
    L.append("-- Disease data credit: PlantVillage research dataset (public")
    L.append("-- research) — ye data humne apne project me use kiya hai.")
    L.append("-- =============================================================")
    L.append("CREATE DATABASE IF NOT EXISTS fasalshield_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    L.append("USE fasalshield_db;")
    L.append("")
    L.append("DROP TABLE IF EXISTS leaf_scans;")
    L.append("DROP TABLE IF EXISTS irrigation_logs;")
    for t in ("local_guides", "risk_rules", "dept_contacts", "crop_calendar",
              "fertilizer_plans", "soil_factors", "crops", "diseases"):
        L.append(f"DROP TABLE IF EXISTS {t};")
    L.append("")
    for sql in TABLES_SQL:
        L.append(sql + ";")
        L.append("")
    # seed inserts
    for lab in knowledge.LABELS:
        adv = knowledge.advice_for(lab)
        L.append("INSERT INTO diseases (label, plant, is_healthy, treatment_en, prevention_en, advice_ur, advice_sd, advice_ur_script) VALUES ("
                 + ", ".join(_esc(x) for x in (lab, plant_of(lab), 1 if adv["healthy"] else 0, adv["en"],
                                               adv["prevention"], adv["urdu"], adv["sindhi"], adv["urdu_script"])) + ");")
    for name, c in knowledge.CROPS.items():
        L.append(f"INSERT INTO crops (crop_name, daily_litres_per_acre, kc) VALUES ({_esc(name)}, {c['daily_litres_per_acre']}, {c['kc']});")
    for name, f in knowledge.SOIL_FACTOR.items():
        L.append(f"INSERT INTO soil_factors (soil_name, factor) VALUES ({_esc(name)}, {f});")
    for name, p in knowledge.FERTILIZER_PLANS.items():
        L.append("INSERT INTO fertilizer_plans (crop_name, dap_bags, urea_bags, sop_bags, timing) VALUES ("
                 + ", ".join(_esc(x) for x in (name, p["dap_bags"], p["urea_bags"], p["sop_bags"], p["timing"])) + ");")
    for name, txt in knowledge.FERTILIZER_PER_PLANT.items():
        L.append(f"INSERT INTO fertilizer_plans (crop_name, per_plant_text) VALUES ({_esc(name)}, {_esc(txt)});")
    for c in knowledge.CROP_CALENDAR:
        L.append("INSERT INTO crop_calendar (crop_name, season, sowing, harvest, seed_rate, sowing_en, harvest_en, seed_en) VALUES ("
                 + ", ".join(_esc(c.get(k)) for k in ("crop", "season", "sowing", "harvest", "seed", "sowing_en", "harvest_en", "seed_en")) + ");")
    for c in knowledge.DEPT_CONTACTS:
        L.append("INSERT INTO dept_contacts (name, org, phone, address, timing, note) VALUES ("
                 + ", ".join(_esc(c[k]) for k in ("name", "org", "phone", "address", "timing", "note")) + ");")
    for r in knowledge.RISK_RULES:
        L.append("INSERT INTO risk_rules (crop_name, disease_name, kind, advice, advice_en) VALUES ("
                 + ", ".join(_esc(r.get(k)) for k in ("crop", "disease", "kind", "advice", "advice_en")) + ");")
    for crop, g in knowledge.LOCAL_CROP_GUIDES.items():
        for title, text in g["sections"]:
            L.append("INSERT INTO local_guides (crop_name, section_title, section_text) VALUES ("
                     + ", ".join(_esc(x) for x in (crop, title, text)) + ");")
    L.append("")
    L.append("-- ============ Teacher ke liye sample queries (comment me) ============")
    L.append("-- SELECT * FROM diseases;                                        -- 38 records")
    L.append("-- SELECT plant, COUNT(*) FROM diseases GROUP BY plant;           -- har poda, kitni halatein")
    L.append("-- SELECT label, COUNT(*) AS scans FROM leaf_scans GROUP BY label ORDER BY scans DESC;")
    L.append("-- SELECT SUM(saved_litres) FROM irrigation_logs;                 -- kul bacha hua paani")
    L.append("-- SELECT s.label, d.treatment_en FROM leaf_scans s JOIN diseases d ON s.disease_id = d.disease_id;")
    L.append("-- SELECT * FROM diseases WHERE label LIKE '%Tomato%';            -- LIKE search (Sawal-Jawab page yehi use karta hai)")
    return "\n".join(L) + "\n"
