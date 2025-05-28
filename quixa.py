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
        
@app.route('/verifica_email', methods=['GET'])
def verifica_email():
    email = request.args.get('email')
    if not email:
        return jsonify({"errore": "Parametro 'email' mancante"}), 400

    email_str = email.strip().lower()
    print(f"Cercando email: '{email_str}'")

    if 'email' not in df.columns:
        return jsonify({"errore": "La colonna 'email' non è presente nel CSV"}), 500

    riga = df[df['email'].str.lower().str.strip() == email_str]

    if not riga.empty:
        record = riga.iloc[0].to_dict()
        record["esiste"] = True
        print(f"TROVATA email: {record}")
        return jsonify(record)
    else:
        print(f"NON TROVATA email per: {email_str}")
        return jsonify({
            "email": email_str,
            "esiste": False
        })

@app.route('/verifica_tipoCliente', methods=['GET'])
def verifica_tipo_cliente():
    tipo_cliente = request.args.get('tipo_cliente')
    if not tipo_cliente:
        return jsonify({"errore": "Parametro 'tipo_cliente' mancante"}), 400

    tipo_cliente_str = tipo_cliente.strip().upper()
    validi = ["CLIENT", "PROSPECT", "PROSPECT RED"]

    if tipo_cliente_str not in validi:
        return jsonify({
            "tipo_cliente": tipo_cliente,
            "valido": False,
            "messaggio": "Tipo cliente non valido"
        })

    # Cerca nel dataframe (attenzione alla gestione case e spazi)
    df_tipo = df['tipo_cliente'].astype(str).str.upper().str.strip()

    esiste = tipo_cliente_str in df_tipo.values

    return jsonify({
        "tipo_cliente": tipo_cliente,
        "valido": esiste
    })
@app.route('/verifica_tutto', methods=['GET'])
def verifica_tutto():
    numero = request.args.get('numero_polizza', '').strip()
    email = request.args.get('email', '').strip().lower()
    tipo_cliente = request.args.get('tipo_cliente', '').strip().upper()

    risultato = {}

    # Verifica numero_polizza
    if numero:
        is_partner = numero.startswith("0085")
        riga_polizza = df[df['numero_polizza'] == numero]
        if not riga_polizza.empty:
            polizza = riga_polizza.iloc[0].to_dict()
            polizza["esiste"] = True
            polizza["partner"] = is_partner
            risultato["verifica_polizza"] = polizza
        else:
            risultato["verifica_polizza"] = {
                "numero_polizza": numero,
                "esiste": False,
                "partner": is_partner
            }
    else:
        risultato["verifica_polizza"] = {"errore": "Parametro 'numero_polizza' mancante"}

    # Verifica email
    if email:
        if 'email' in df.columns:
            riga_email = df[df['email'].str.lower().str.strip() == email]
            if not riga_email.empty:
                rec = riga_email.iloc[0].to_dict()
                rec["esiste"] = True
                risultato["verifica_email"] = rec
            else:
                risultato["verifica_email"] = {"email": email, "esiste": False}
        else:
            risultato["verifica_email"] = {"errore": "Colonna 'email' non presente nel CSV"}
    else:
        risultato["verifica_email"] = {"errore": "Parametro 'email' mancante"}

    # Verifica tipo_cliente
    validi = ["CLIENT", "PROSPECT", "PROSPECT RED"]
    if tipo_cliente:
        if tipo_cliente not in validi:
            risultato["verifica_tipoCliente"] = {
                "tipo_cliente": tipo_cliente,
                "valido": False,
                "messaggio": "Tipo cliente non valido"
            }
        else:
            df_tipo = df['tipo_cliente'].astype(str).str.upper().str.strip()
            esiste = tipo_cliente in df_tipo.values
            risultato["verifica_tipoCliente"] = {
                "tipo_cliente": tipo_cliente,
                "valido": esiste
            }
    else:
        risultato["verifica_tipoCliente"] = {"errore": "Parametro 'tipo_cliente' mancante"}

    return jsonify(risultato)

@app.route('/tutte_le_polizze', methods=['GET'])
def tutte_le_polizze():
    return jsonify(df['numero_polizza'].tolist())

if __name__ == '__main__':
    app.run(debug=True)
