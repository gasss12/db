
from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# Inserisci la tua connection string MongoDB come variabile ambiente
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://admin:admin123@cluster0.mfgmbey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Initialize MongoDB connection
client = None
db = None
collection = None

try:
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    db = client["quixa"]
    collection = db["quixa_collection"]
    
except Exception as e:
    print(f"Errore connessione MongoDB: {e}")
    client = None
    db = None
    collection = None

@app.route("/", methods=["GET"])
def home():
    connection_status = "Connesso" if collection is not None else "Non connesso"
    return jsonify({
        "message": "API Quixa attiva",
        "database_status": connection_status,
        "endpoints": {
            "POST /verifica-polizza": "Verifica esistenza polizza per prefisso"
        }
    })

@app.route("/verifica-polizza", methods=["POST"])
def verifica_polizza():
    if collection is None:
        return jsonify({"errore": "Database non disponibile"}), 500

    try:
        # Recupera tutte le polizze dal database
        results = list(collection.find({}, {"_id": 0}))  # Escludo _id dalla risposta

        if results:
            # Crea lista di tutti i numeri polizza
            numeri_polizza = [doc["numero_polizza"] for doc in results]
            
            # Crea messaggio formattato per il chatbot
            messaggio_polizze = "Ecco tutte le polizze disponibili:\n\n"
            for i, doc in enumerate(results, 1):
                messaggio_polizze += f"{i}. Polizza: {doc['numero_polizza']}\n"
                messaggio_polizze += f"   Utente: {doc['utente_id']}\n"
                messaggio_polizze += f"   Stato: {doc.get('stato', 'attiva')}\n"
                messaggio_polizze += f"   Data creazione: {doc.get('data_creazione', 'N/A')}\n"
                messaggio_polizze += f"   Data scadenza: {doc.get('data_scadenza', 'N/A')}\n\n"

            return jsonify({
                "esiste": True,
                "totale_polizze": len(results),
                "numeri_polizza": numeri_polizza,
                "polizze": results,
                "messaggio": messaggio_polizze
            })
        else:
            return jsonify({
                "esiste": False,
                "messaggio": "Nessuna polizza trovata nel database"
            })
            
    except Exception as e:
        return jsonify({"errore": f"Errore durante la ricerca: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# Inserisci la tua connection string MongoDB come variabile ambiente
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://admin:admin123@cluster0.mfgmbey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Initialize MongoDB connection
client = None
db = None
collection = None

try:
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    db = client["quixa"]
    collection = db["quixa_collection"]
    
except Exception as e:
    print(f"Errore connessione MongoDB: {e}")
    client = None
    db = None
    collection = None

@app.route("/", methods=["GET"])
def home():
    connection_status = "Connesso" if collection is not None else "Non connesso"
    return jsonify({
        "message": "API Quixa attiva",
        "database_status": connection_status,
        "endpoints": {
            "POST /verifica-polizza": "Verifica esistenza polizza per prefisso"
        }
    })

@app.route("/verifica-polizza", methods=["POST"])
def verifica_polizza():
    if collection is None:
        return jsonify({"errore": "Database non disponibile"}), 500

    try:
        # Recupera tutte le polizze dal database
        results = list(collection.find({}, {"_id": 0}))  # Escludo _id dalla risposta

        if results:
            # Crea lista di tutti i numeri polizza
            numeri_polizza = [doc["numero_polizza"] for doc in results]
            
            # Crea messaggio formattato per il chatbot
            messaggio_polizze = "Ecco tutte le polizze disponibili:\n\n"
            for i, doc in enumerate(results, 1):
                messaggio_polizze += f"{i}. Polizza: {doc['numero_polizza']}\n"
                messaggio_polizze += f"   Utente: {doc['utente_id']}\n"
                messaggio_polizze += f"   Stato: {doc.get('stato', 'attiva')}\n"
                messaggio_polizze += f"   Data creazione: {doc.get('data_creazione', 'N/A')}\n"
                messaggio_polizze += f"   Data scadenza: {doc.get('data_scadenza', 'N/A')}\n\n"

            return jsonify({
                "esiste": True,
                "totale_polizze": len(results),
                "numeri_polizza": numeri_polizza,
                "polizze": results,
                "messaggio": messaggio_polizze
            })
        else:
            return jsonify({
                "esiste": False,
                "messaggio": "Nessuna polizza trovata nel database"
            })
            
    except Exception as e:
        return jsonify({"errore": f"Errore durante la ricerca: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
