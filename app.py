from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = "sala.db"

# Creazione tabelle se non esistono
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pazienti (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT,
                   cognome TEXT,
                   codice_sanitario TEXT,
                   data_nascita TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS interventi (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   paziente_id INTEGER,
                   specialita TEXT,
                   durata INTEGER,
                   sala INTEGER,
                   orario_inizio TEXT,
                   orario_fine TEXT,
                   FOREIGN KEY(paziente_id) REFERENCES pazienti(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS equipe (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   intervento_id INTEGER,
                   chirurgo TEXT,
                   aiuto TEXT,
                   anestesista TEXT,
                   strumentista TEXT,
                   circolante TEXT,
                   FOREIGN KEY(intervento_id) REFERENCES interventi(id))''')
    conn.commit()
    conn.close()

init_db()

# ------------------- API -------------------
@app.route("/api/pazienti", methods=["POST"])
def add_paziente():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO pazienti (nome, cognome, codice_sanitario, data_nascita) VALUES (?, ?, ?, ?)",
              (data["nome"], data["cognome"], data["codice_sanitario"], data["data_nascita"]))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id})

@app.route("/api/interventi", methods=["POST"])
def add_intervento():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO interventi 
                 (paziente_id, specialita, durata, sala, orario_inizio, orario_fine) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (data["paziente_id"], data["specialita"], data["durata"], data["sala"],
               data["orario_inizio"], data["orario_fine"]))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id})

@app.route("/api/equipe", methods=["POST"])
def add_equipe():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""INSERT INTO equipe 
                 (intervento_id, chirurgo, aiuto, anestesista, strumentista, circolante) 
                 VALUES (?, ?, ?, ?, ?, ?)""",
              (data["intervento_id"], data["chirurgo"], data["aiuto"], data["anestesista"],
               data["strumentista"], data["circolante"]))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id})

@app.route("/api/interventi", methods=["GET"])
def get_interventi():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT i.id, p.nome, p.cognome, i.specialita, i.durata, i.sala, i.orario_inizio, i.orario_fine 
                 FROM interventi i JOIN pazienti p ON i.paziente_id = p.id""")
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)

# ------------------- Viste HTML (opzionali) -------------------
@app.route("/")
def index():
    return render_template("index.html")  # il tuo file HTML del planner

if __name__ == "__main__":
    app.run(debug=True, port=5000)
