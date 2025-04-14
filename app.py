from flask import Flask, request
import sqlite3

app = Flask(__name__)

def pripoj_db():
    conn = sqlite3.connect("kurzy.db")
    return conn


@app.route('/')
def index():
    return '''
        <h1>Výber z databázy</h1>
        <a href="/kurzy"><button>Zobraz všetky kurzy</button></a>
        <a href="/treneri"><button>Zobraz všetkých trénerov</button></a>
        <hr>
    '''

@app.route('/kurzy')
def zobraz_kurzy():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Kurzy")
    kurzy = cursor.fetchall()

    conn.close()

    vystup = "<h2>Zoznam kurzov:</h2>"
    for kurz in kurzy:
        vystup += f"<p>{kurz}</p>"

    vystup += '<a href="/">Späť</a>'
    return vystup

@app.route('/treneri')
def zobraz_trenerov():
    conn = pripoj_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT T.ID_trenera, T.Meno || ' ' || T.Priezvisko as Trener, Nazov_kurzu
        FROM Treneri T LEFT JOIN Kurzy K ON T.ID_trenera = K.ID_trenera
    """)
    treneri = cursor.fetchall()

    conn.close()

    vystup = "<h2>Zoznam trénerov a kurzov:</h2>"
    for trener in treneri:
        vystup += f"<p>{trener}</p>"

    vystup += '<a href="/">Späť</a>'
    return vystup

@app.route('/registracia', methods=['GET'])
def registracia_form():
    return '''
        <h2>Registrácia trénera</h2>
        <form action="/registracia" method="post">
            <label>Meno:</label><br>
            <input type="text" name="meno" required><br><br>

            <label>Priezvisko:</label><br>
            <input type="text" name="priezvisko" required><br><br>

            <label>Špecializácia:</label><br>
            <input type="text" name="specializacia" required><br><br>

            <label>Telefón:</label><br>
            <input type="text" name="telefon" required><br><br>

            <label>Heslo:</label><br>
            <input type="password" name="heslo" required><br><br>

            <button type="submit">Registrovať</button>
        </form>
        <hr>
        <a href="/">Späť</a>
    '''

@app.route('/registracia', methods=['POST'])
def registracia_trenera():
    meno = request.form['meno']
    priezvisko = request.form['priezvisko']
    specializacia = request.form['specializacia']
    telefon = request.form['telefon']
    heslo = request.form['heslo']

    heslo_hash = hashlib.sha256(heslo.encode()).hexdigest()

    conn = pripoj_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Treneri (Meno, Priezvisko, Specializacia, Telefon, Heslo) VALUES (?, ?, ?, ?, ?)", 
                   (meno, priezvisko, specializacia, telefon, heslo_hash))
    conn.commit()
    conn.close()

    return '''
        <h2>Tréner bol úspešne zaregistrovaný!</h2>
        <hr>
        <a href="/">Späť</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)