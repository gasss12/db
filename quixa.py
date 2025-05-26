from flask import Flask, request, jsonify
from pymongo import MongoClient
import os
import re

app = Flask(__name__)

# MongoDB connection string (inseriscila direttamente o con variabili d'ambiente)
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/?retryWrites=true&w=majority")

client = MongoClient(MONGO_URI)
db = client["quixa"]
collection = db["quixa_collection"]

@app.route('/verifica-numero-polizza', methods=['POST'])
def verifica_polizza():
    try:
        data = request.get_json()
        numero_polizza = data.get("numero_polizza", "")

        if not numero_polizza:
            return jsonify({"errore": "numero_polizza mancante"}), 400

        # Verifica se inizia per "12"
        if not numero_polizza.startswith("12"):
            return jsonify({"trovato": False, "motivo": "Non inizia per 12"})

        # Controlla se esiste nel DB
        query = { "numero_polizza": { "$regex": "^12" } }
        result = collection.find_one(query)

        if result:
            return jsonify({"trovato": True})
        else:
            return jsonify({"trovato": False})
    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
