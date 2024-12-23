from fastapi import FastAPI
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import time
from urllib.parse import unquote
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.responses import HTMLResponse


app = FastAPI()

# A mettre en gitignore de préférence ----------------
apiweatherkey = "19442bda530814d94bc18d27ca6c0e53"
# ----------------------------------------------------

# test serveur

@app.get("/") 
async def read_root():
    return {"message": "Serveur REST en ligne"}

# connecter à la base logement.db

def get_db_connection(): 
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn


# =================== Création des classes ===================
# ===========================================================

class Logement(BaseModel):
    adresse: str
    numero_tel: str
    adresse_IP: str

class Pieces(BaseModel):
    x: int
    y: int
    z: int
    adresse_logement: str

class Capteurs_actionneurs(BaseModel):
    ref_type: str
    ref_commerciale: str
    ref_piece: int
    port_com: int
    etat : int

class Mesures(BaseModel):
    ref_capteur: str
    valeur: float

class Factures(BaseModel):
    adresse_logement: str
    type_facture: str
    montant: float
    valeur_conso: float

class Type_capteurs_actionneurs(BaseModel):
    nom: str
    unite: str
    plage_max: int
    plage_min: int

# =================== Afficher sur le serveur la base de donées ===================
# ================================================================================

# obtenir les logements en appelant la base données

@app.get("/logements") # décorateur indique que doit repondre à requete http POST à l'url
async def get_logements(): # executée que quand requete POST justement
    conn = get_db_connection()
    logements_ = conn.execute("SELECT * FROM logements").fetchall()
    conn.close()
    return {"logements": [dict(logements) for logements in logements_]}

# obtenir les pieces en appelant la base données

@app.get("/pieces") # décorateur indique que doit repondre à requete http POST à l'url
async def get_logements(): # executée que quand requete POST justement
    conn = get_db_connection()
    piece_ = conn.execute("SELECT * FROM pieces").fetchall()
    conn.close()
    return {"pieces": [dict(pieces) for pieces in piece_]}

# obtenir les capteurs en appelant la base données

@app.get("/capteurs") # décorateur indique que doit repondre à requete http POST à l'url
async def get_capteurs(): # executée que quand requete get justement
    conn = get_db_connection()
    capteurs_ = conn.execute("SELECT * FROM capteurs_actionneurs").fetchall()
    conn.close()
    return {"capteurs": [dict(capteurs_actionneurs) for capteurs_actionneurs in capteurs_]}

# obtenir les mesures en appelant la base données

@app.get("/mesures") # décorateur indique que doit repondre à requete http POST à l'url
async def get_mesures():
    conn = get_db_connection()
    mesures_ = conn.execute("SELECT * FROM mesures").fetchall()
    conn.close()
    return {"mesures": [dict(mesures) for mesures in mesures_]}

# obtenir les factures en appelant la base données

@app.get("/factures") # décorateur indique que doit repondre à requete http POST à l'url
async def get_factures():
    conn = get_db_connection()
    factures_ = conn.execute("SELECT * FROM factures").fetchall()
    conn.close()
    return {"factures": [dict(factures) for factures in factures_]}

# obtenir type capteurs en appelant la base données

@app.get("/type_capteurs_actionneurs") # décorateur indique que doit repondre à requete http POST à l'url
async def get_type_capteurs():
    conn = get_db_connection()
    type_capteurs_ = conn.execute("SELECT * FROM type_capteurs_actionneurs").fetchall()
    conn.close()
    return {"type_capteurs": [dict(type_capteurs_actionneurs) for type_capteurs_actionneurs in type_capteurs_]}


# =================== Detection ajout logement ===================
# ===============================================================
# Met à jour la base de données quand il y a des changements

# POST pour ajouter un logement

@app.post("/logements") # lorsque post sur adresse /logements
async def create_logement(logement: Logement):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO logements (adresse, numero_tel, adresse_IP) VALUES (?, ?, ?)",
        (logement.adresse, logement.numero_tel, logement.adresse_IP),
    )
    conn.commit() # enregistre changement dans base de donnée
    conn.close() # ferme connexion
    return {"message": "Logement ajouté"}

# POST pour ajouter une piece

@app.post("/pieces") # lorsque post sur adresse /pieces
async def create_piece(piece: Pieces):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO pieces (x, y, z, adresse_logement) VALUES (?, ?, ?, ?)",
        (piece.x, piece.y, piece.z, piece.adresse_logement),
    )
    conn.commit()
    conn.close()
    return {"message": "Piece ajoutée"}

# POST pour ajouter un capteur
@app.post("/capteurs_actionneurs") # lorsque post sur adresse /capteurs 
async def create_capteur(capteur: Capteurs_actionneurs): 
    conn = get_db_connection() 
    conn.execute( 
        "INSERT INTO capteurs_actionneurs (ref_type, ref_commerciale, ref_piece, port_com, etat) VALUES (?, ?, ?, ?, ?)", 
        (capteur.ref_type, capteur.ref_commerciale, capteur.ref_piece, capteur.port_com, capteur.etat), 
    ) 
    conn.commit() 
    conn.close() 
    return {"message": "Capteur ajouté"} 

# POST pour ajouter une mesure 
@app.post("/mesures") # lorsque post sur adresse /mesures 
async def create_mesure(mesure: Mesures):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO mesures (ref_capteur, valeur) VALUES (?, ? )",
        (mesure.ref_capteur, mesure.valeur),
    )
    conn.commit()
    conn.close()
    return {"message": "Mesure ajoutée"}

# POST pour ajouter une facture
@app.post("/factures") # lorsque post sur adresse /factures
async def create_facture(facture: Factures):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO factures (adresse_logement, type_facture, montant, valeur_conso) VALUES (?, ?, ?, ?)",
        (facture.adresse_logement, facture.type_facture, facture.montant, facture.valeur_conso),
    )
    conn.commit()
    conn.close()
    return {"message": "Facture ajoutée"}

# POST pour ajouter un type de capteur
@app.post("/type_capteurs_actionneurs") # lorsque post sur adresse /types_capteurs
async def create_type_capteur(type_capteur: Type_capteurs_actionneurs):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO type_capteurs_actionneurs (nom, unite, plage_max, plage_min) VALUES (?, ?, ?, ?)",
        (type_capteur.nom, type_capteur.unite, type_capteur.plage_max, type_capteur.plage_min),
    )
    conn.commit()
    conn.close()
    return {"message": "Type de capteur ajouté"}


# =================== Afficher un camembert général ===================

@app.get("/camembert", response_class=HTMLResponse)
async def generate_pie_chart():
    conn = get_db_connection()
    factures = conn.execute("SELECT type_facture, montant FROM factures").fetchall() # extraire les facture avec montant et type
    conn.close()

    # données pour le graphique
    chart_data = [["Type de Facture", "Montant"]] + [[facture["type_facture"], facture["montant"]] for facture in factures] # liste de liste pour le graphique

    # page HTML
    html_content = f"""
    <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({chart_data});
                    var options = {{
                        title: 'Camembert',
                        is3D: true
                    }};
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }}
            </script>
        </head>
        <body>
            <h1>Repartition Factures</h1>
            <div id="piechart" style="width: 800px; height: 500px;"></div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# ============================== Camembert par adresses ==========================

@app.get("/camembert/{adresse}", response_class=HTMLResponse)
async def generate_pie_chart(adresse: str):
    adresse = unquote(adresse)  # Décode les caractères spéciaux
    conn = get_db_connection()

    # --> filtrer les factures en fonction de l'adresse
    factures = conn.execute(
        "SELECT type_facture, montant FROM factures WHERE adresse_logement = ?", (adresse,)
    ).fetchall()
    conn.close()

    if not factures:  # si il y a pas de factures pour cette adresse
        return HTMLResponse(content="<h1>Aucune facture trouvée pour cette adresse</h1>")

    # données pour graphique
    chart_data = [["Type de Facture", "Montant"]] + [[facture["type_facture"], facture["montant"]] for facture in factures]

    html_content = f"""
    <html>
        <head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <script type="text/javascript">
                google.charts.load('current', {{'packages':['corechart']}});
                google.charts.setOnLoadCallback(drawChart);
                function drawChart() {{
                    var data = google.visualization.arrayToDataTable({chart_data});
                    var options = {{
                        title: 'Camembert pour {adresse}',
                        is3D: true
                    }};
                    var chart = new google.visualization.PieChart(document.getElementById('piechart'));
                    chart.draw(data, options);
                }}
            </script>
        </head>
        <body>
            <h1>Répartition des factures pour {adresse}</h1>
            <div id="piechart" style="width: 800px; height: 500px;"></div>

            <p><a href="/consommation" class="btn btn-primary">Retour à la consommation</a></p>

        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# =================== Afficher les prévisions météo sur 5j (Paris) ===================

@app.get("/meteo", response_class=HTMLResponse)
async def get_meteo():
    url = f"http://api.openweathermap.org/data/2.5/forecast?q=Paris&appid={apiweatherkey}&lang=fr&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            data = response.json()
            previsions = [
                {
                    "date": forecast["dt_txt"],
                    "température": forecast["main"]["temp"],
                    "description": forecast["weather"][0]["description"],
                }
                for forecast in data["list"] if forecast["dt_txt"].endswith("12:00:00")
            ]
            # page HTML pour que ce soit plus lisible
            html_content = """ 
            <html>
                <head>
                    <title>Prévisions météo</title>
                </head>
                <body>
                    <h1>Prévisions météo pour Paris</h1>
                    <ul>
            """
            for prev in previsions:
                html_content += f"""
                    <li>
                        <strong>Date :</strong> {prev['date']}<br>
                        <strong>Température :</strong> {prev['température']}°C<br>
                        <strong>Description :</strong> {prev['description']}
                    </li>
                    <hr>
                """
            html_content += """
                    </ul>
                </body>
            </html>
            """
            return html_content
        else:
            return "<h1>Erreur lors de la récupération des données météo</h1>"


# ========================= ESP ======================


SEUIL_TEMPERATURE = 25.0 # température de seuil pour led

# Partie ESP, je récupère son id avec code rapide arduino puis avec un second code arduino j’envoi la température 

# Le code arduino_temp_esp me renvoi le code reponse HTTP -1, adresse correcte pourtant, je simule donc un envoi periodique.


# ====================== SERVEUR ========================
# =====================================================

