import swisseph as swe
import datetime

# Entrada do usuário
data = input("Digite a data (AAAA-MM-DD): ")
hora = input("Digite a hora (HH:MM): ")
fuso = float(input("Digite o fuso horário (ex: -3 para Brasil): "))

# Conversão para datetime
dt = datetime.datetime.fromisoformat(f"{data}T{hora}")
utc_hour = dt.hour + dt.minute / 60 - fuso

# Cálculo da posição da Lua
jd = swe.julday(dt.year, dt.month, dt.day, utc_hour)
moon_pos = swe.calc_ut(jd, swe.MOON)[0][0]  # posição da Lua em graus

# Lista dos signos
signos = [
    "Áries", "Touro", "Gêmeos", "Câncer", "Leão", "Virgem",
    "Libra", "Escorpião", "Sagitário", "Capricórnio", "Aquário", "Peixes"
]

# Determinar o signo lunar
signo_lunar = signos[int(moon_pos // 30)]
print(f"\n🌙 Seu signo lunar é: {signo_lunar}")
