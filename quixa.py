from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Carica il file CSV una sola volta all'avvio
df = pd.read_csv("quixa_polizze.csv", sep=';', engine='python')

# Pulisci il DataFrame rimuovendo colonne vuote
df = df.dropna(axis=1, how='all')  # Rimuove colonne completamente vuote
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Rimuove colonne "Unnamed"

# Converti la colonna numero_polizza in stringa e rimuovi spazi
df['numero_polizza'] = df['numero_polizza'].astype(str).str.strip()

# Debug: stampa le prime righe e info sul DataFrame
print("=== DEBUG INFO ===")
print("Colonne nel CSV:", df.columns.tolist())
print("Prime 5 righe:")
print(df.head())
print("Tipo di dato della colonna numero_polizza:", df['numero_polizza'].dtype)
print("Campioni di numeri polizza:")
print(df['numero_polizza'].head(10).tolist())
print("==================")
@app.route('/verifica_polizza', methods=['GET'])
def verifica_polizza():
    numero = request.args.get('numero_polizza')
    if not numero:
        return jsonify({"errore": "Parametro 'numero_polizza' mancante"}), 400

    print(f"Cercando numero: '{numero}' (tipo: {type(numero)})")

    # Converti il numero in stringa e puliscilo
    numero_str = str(numero).strip()

    # Controlla se il numero inizia per "0085"
    is_partner = numero_str.startswith("0085")
    print(f"Inizia con '0085'? {'Sì' if is_partner else 'No'}")

    # Debug: vedi se esiste nel dataframe
    print(f"Numeri unici nel CSV: {df['numero_polizza'].nunique()}")
    print(f"Il numero cercato è nella lista? {numero_str in df['numero_polizza'].values}")

    # Ricerca esatta
    riga = df[df['numero_polizza'] == numero_str]

    if not riga.empty:
        polizza = riga.iloc[0].to_dict()
        polizza["esiste"] = True
        polizza["partner"] = is_partner  # Aggiunta la chiave "partner"
        print(f"TROVATA polizza: {polizza}")
        return jsonify(polizza)
    else:
        print(f"NON TROVATA polizza per: {numero_str}")
        return jsonify({
            "numero_polizza": numero_str,
            "esiste": False,
            "partner": is_partner  # Anche se non trovata, indichiamo se è partner
        })


@app.route('/tutte_le_polizze', methods=['GET'])
def tutte_le_polizze():
    return jsonify(df['numero_polizza'].tolist())

if __name__ == '__main__':
    app.run(debug=True)
