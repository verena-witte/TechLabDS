import pandas as pd
import folium
from folium.plugins import HeatMap
import ipywidgets as widgets
from IPython.display import display

# Koordinaten von Münster (Beispielwerte)
muenster_lat = 51.9607
muenster_lon = 7.6261
zoom_level = 12

# CSV-Datei einlesen
df = pd.read_csv('Unfallorte_Muenster.csv')

# Koordinatenwerte im deutschen Zahlenformat in das amerikanische Zahlenformat konvertieren
df['YGCSWGS84'] = df['YGCSWGS84'].str.replace(',', '.').astype(float)
df['XGCSWGS84'] = df['XGCSWGS84'].str.replace(',', '.').astype(float)

# Funktion zum Aktualisieren der Karte basierend auf dem ausgewählten Wochentag, der Uhrzeit und dem Fahrzeugtyp
def update_map(weekday, hour, vehicle):
    if vehicle == 'Fußgänger':
        filtered_df = df[(df['UWOCHENTAG'] == weekday) & (df['USTUNDE'] == hour) & (df['IstFuss'] == 1)]
    elif vehicle == 'PKW':
        filtered_df = df[(df['UWOCHENTAG'] == weekday) & (df['USTUNDE'] == hour) & (df['IstPKW'] == 1)]
    elif vehicle == 'Fahrrad':
        filtered_df = df[(df['UWOCHENTAG'] == weekday) & (df['USTUNDE'] == hour) & (df['IstRad'] == 1)]
    else:
        filtered_df = pd.DataFrame(columns=df.columns)  # Leerer DataFrame, wenn kein Fahrzeugtyp ausgewählt ist
    
    locations = filtered_df[['YGCSWGS84', 'XGCSWGS84']].dropna()  # Standorte für Heatmap vorbereiten
    
    # Karte erstellen und auf Münster zoomen
    map = folium.Map(location=[muenster_lat, muenster_lon], zoom_start=zoom_level)
    
    # Heatmap erstellen
    heatmap = HeatMap(data=locations, radius=15)
    heatmap.add_to(map)
    
    # Karte anzeigen
    display(map)

# Schieberegler für Wochentag, Uhrzeit und Dropdown-Liste für Fahrzeugtyp erstellen
weekday_slider = widgets.IntSlider(value=1, min=1, max=7, description='Wochentag:')
hour_slider = widgets.IntSlider(value=0, min=0, max=23, description='Uhrzeit:')
vehicle_dropdown = widgets.Dropdown(options=['Fußgänger', 'PKW', 'Fahrrad'], description='Am Fahrradunfall beteiligter Fahrzeugtyp:')
widgets.interactive(update_map, weekday=weekday_slider, hour=hour_slider, vehicle=vehicle_dropdown)
