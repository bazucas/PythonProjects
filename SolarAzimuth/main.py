import matplotlib.pyplot as plt
import pandas as pd
from pvlib import solarposition
from datetime import timedelta

# Coordendas do Cartaxo
latitude = 39.10
longitude = -8.80
tz = 'UTC'

# Gerando datas de início e fim para cada mês em 2023
end_dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
start_dates = end_dates - pd.DateOffset(months=1) + timedelta(days=10)

# Criando o gráfico
fig, ax = plt.subplots()

# Calculando o azimute solar e a elevação, e plotando as curvas mensais
for start in start_dates:
    day_of_month = start.replace(hour=6).tz_localize(tz)  # Início do dia
    day_end = day_of_month.replace(hour=18)  # Fim do dia
    times = pd.date_range(start=day_of_month, end=day_end, freq='5min')
    solpos = solarposition.get_solarposition(times, latitude, longitude)
    ax.plot(solpos['azimuth'], solpos['apparent_elevation'], label=start.strftime('%B'))

# Adicionando as curvas adicionais para cada hora, entre as 5:00 e as 22:00
for hour in range(5, 23):
    hour_times = []
    for start in start_dates:
        day_of_month = start.replace(hour=hour).tz_localize(tz)
        hour_times.append(day_of_month)
    hour_solpos = solarposition.get_solarposition(pd.DatetimeIndex(hour_times), latitude, longitude)
    ax.plot(hour_solpos['azimuth'], hour_solpos['apparent_elevation'], linewidth=1, alpha=0.9)

# Configurando o gráfico
plt.xlabel('Azimute Solar (graus)')
plt.ylabel('Elevação Solar (graus)')
plt.title('Azimute Solar (Lat 39 Long -8.78 - 2023)')

# Configurando a grade
ax.set_xticks(range(60, 290, 20))
ax.set_yticks(range(0, 81, 5))
ax.grid(which='both', linestyle='--', linewidth=0.5)

# Definindo os limites do eixo Y
ax.set_ylim(0, 80)

plt.legend(title='Meses', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()