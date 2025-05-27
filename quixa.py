from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carica il file Excel una sola volta all'avvio
df = pd.read_csv("nome_file.csv", sep=';', engine='python')
  # Assicurati che il file sia nella stessa directory

@app.route('/verifica_polizza', methods=['GET'])
def verifica_polizza():
    numero = request.args.get('numero_polizza')
    if not numero:
        return jsonify({"errore": "Parametro 'numero_polizza' mancante"}), 400

    riga = df[df['numero_polizza'] == numero]

    if not riga.empty:
        polizza = riga.iloc[0].to_dict()
        polizza["esiste"] = True
        return jsonify(polizza)
    else:
        return jsonify({"numero_polizza": numero, "esiste": False})

@app.route('/tutte_le_polizze', methods=['GET'])
def tutte_le_polizze():
    return jsonify(df['numero_polizza'].tolist())

if __name__ == '__main__':
    app.run(debug=True)
