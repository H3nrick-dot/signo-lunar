from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
import datetime
import uuid

app = Flask(__name__)
CORS(app)

signs = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

# Armazena respostas temporariamente com um ID único
results = {}

@app.route('/lunar-sign', methods=['POST'])
def lunar_sign():
    try:
        data = request.json
        date_str = data['date']
        time_str = data['time']
        timezone = float(data['timezone'])

        dt = datetime.datetime.fromisoformat(f"{date_str}T{time_str}")
        utc_hour = dt.hour + dt.minute / 60 - timezone

        jd = swe.julday(dt.year, dt.month, dt.day, utc_hour)
        moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
        sign = signs[int(moon_pos // 30)]

        token = str(uuid.uuid4())  # Cria um token único
        results[token] = sign

        return jsonify({ "token": token })  # Typebot salva esse token

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/lunar-sign/<token>', methods=['GET'])
def get_sign(token):
    sign = results.get(token)
    if sign:
        return jsonify({ "sign": sign })  # Typebot pega esse valor via GET
    else:
        return jsonify({ "error": "Token inválido ou expirado" }), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
