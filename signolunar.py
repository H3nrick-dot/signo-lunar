from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
import datetime

app = Flask(__name__)
CORS(app)

signs = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

@app.route('/lunar-sign', methods=['POST'])
def lunar_sign():
    try:
        data = request.json
        date_str = data['date']  # formato esperado: "23-02-1999"
        time_str = data['time']  # formato: "13:30"
        timezone = float(data['timezone'])  # exemplo: -3

        # Transformar para datetime
        dt = datetime.datetime.strptime(f"{date_str}T{time_str}", "%d-%m-%YT%H:%M")
        utc_hour = dt.hour + dt.minute / 60 - timezone

        jd = swe.julday(dt.year, dt.month, dt.day, utc_hour)
        moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]
        sign = signs[int(moon_pos // 30)]

        return jsonify({"sign": sign})  # <-- Typebot pega isso!
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
