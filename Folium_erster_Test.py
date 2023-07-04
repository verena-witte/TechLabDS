import pandas as pd
import folium
from folium.plugins import HeatMap

# CSV-Datei einlesen
df = pd.read_csv('Unfallorte_Muenster.csv', encoding='ISO-8859-1')

# Koordinatenwerte im deutschen Zahlenformat in das amerikanische Zahlenformat konvertieren
df['YGCSWGS84'] = df['YGCSWGS84'].str.replace(',', '.').astype(float)
df['XGCSWGS84'] = df['XGCSWGS84'].str.replace(',', '.').astype(float)

# Karte erstellen
map = folium.Map()

# Standorte für Heatmap vorbereiten
locations = df[['YGCSWGS84', 'XGCSWGS84']].dropna()

# Heatmap erstellen
heatmap = HeatMap(data=locations, radius=15)
heatmap.add_to(map)

# Karte anzeigen
map
