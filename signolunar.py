from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import swisseph as swe
import datetime
import os
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# Pasta onde o gráfico será salvo
MAPAS_FOLDER = os.path.join(os.getcwd(), "mapas")
if not os.path.exists(MAPAS_FOLDER):
    os.makedirs(MAPAS_FOLDER)

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

        lunar_sign = signs[int(moon_pos // 30)]
        solar_sign = signs[int(sun_pos // 30)]
        phase = get_lunar_phase(moon_pos, sun_pos)

        return jsonify({
            "lunar_sign": lunar_sign,
            "solar_sign": solar_sign,
            "phase": phase
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    try:
        data = request.json
        date_str = data['date']
        time_str = data['time']
        timezone = float(data['timezone'])

        dt = datetime.datetime.fromisoformat(f"{date_str}T{time_str}")
        utc_hour = dt.hour + dt.minute / 60 - timezone
        jd = swe.julday(dt.year, dt.month, dt.day, utc_hour)

        planet_names = ["☉ Sol", "☽ Lua", "☿ Mercúrio", "♀ Vênus", "♂ Marte", "♃ Júpiter", "♄ Saturno"]
        planet_ids = [swe.SUN, swe.MOON, swe.MERCURY, swe.VENUS, swe.MARS, swe.JUPITER, swe.SATURN]
        positions = [swe.calc_ut(jd, pid)[0][0] for pid in planet_ids]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
        ax.set_theta_direction(-1)
        ax.set_theta_offset(3.14159 / 2)
        ax.set_yticklabels([])
        ax.set_xticks([i * (3.14159 / 6) for i in range(12)])
        ax.set_xticklabels(signs)

        for pos, name in zip(positions, planet_names):
            angle_rad = (360 - pos) * (3.14159 / 180)
            ax.plot([angle_rad], [1], marker='o', label=name)

        ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2)
        chart_path = os.path.join(MAPAS_FOLDER, 'mapa_astral.png')
        plt.savefig(chart_path, bbox_inches='tight')
        plt.close()

        return jsonify({
            "chart_url": "https://signo-lunar.onrender.com/mapas/mapa_astral.png"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mapas/<path:filename>')
def serve_mapas(filename):
    return send_from_directory(MAPAS_FOLDER, filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
