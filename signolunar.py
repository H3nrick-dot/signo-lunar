from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
import datetime
import uuid

app = Flask(__name__)
CORS(app)

# Dicionário temporário para guardar resultados
results = {}

signs = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

@app.route('/lunar-sign', methods=['POST'])
def lunar_sign():
    try:
        data = request.json
        date_str = data['date']  # formato: YYYY-MM-DD
        time_str = data['time']  # formato: HH:MM
        timezone = float(data['timezone'])  # ex: -3

        # Converter string para datetime
        dt = datetime.datetime.fromisoformat(f"{date_str}T{time_str}")
        utc_hour = dt.hour + dt.minute / 60 - timezone

        # Calcular posição da Lua
        jd = swe.julday(dt.year, dt.month, dt.day, utc_hour)
        moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
        sign = signs[int(moon_pos // 30)]

        # Gerar token e armazenar resultado
        token = str(uuid.uuid4())
        results[token] = sign

        return jsonify({"token": token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/lunar-sign/<token>', methods=['GET'])
def get_lunar_sign(token):
    sign = results.get(token)
    if sign:
        return jsonify({"sign": sign})
    else:
        return jsonify({"error": "Token não encontrado"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
