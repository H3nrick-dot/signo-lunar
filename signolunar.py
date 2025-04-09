from flask import Flask, request, jsonify
from flask_cors import CORS
import swisseph as swe
import datetime
import os

app = Flask(__name__)
CORS(app)

signs = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

def get_lunar_phase(moon_long, sun_long):
    diff = (moon_long - sun_long) % 360

    if diff < 45:
        return "Lua Nova 🌑"
    elif diff < 90:
        return "Lua Crescente 🌒"
    elif diff < 135:
        return "Quarto Crescente 🌓"
    elif diff < 180:
        return "Lua Gibosa Crescente 🌔"
    elif diff < 225:
        return "Lua Cheia 🌕"
    elif diff < 270:
        return "Lua Gibosa Minguante 🌖"
    elif diff < 315:
        return "Quarto Minguante 🌗"
    else:
        return "Lua Minguante 🌘"

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
        sun_pos = swe.calc_ut(jd, swe.SUN)[0][0]

        sign = signs[int(moon_pos // 30)]
        phase = get_lunar_phase(moon_pos, sun_pos)

        return jsonify({
            "sign": sign,
            "phase": phase
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
