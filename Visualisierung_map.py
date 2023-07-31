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

# Funktion zum Aktualisieren der Karte basierend auf der ausgewählten Zeitspanne, dem Wochentag, dem Fahrzeugtyp und dem Straßenzustand
def update_map(weekday_range, hour_range, vehicle, roadcondition):
    start_weekday = weekday_range[0]
    end_weekday = weekday_range[1]
    start_hour = hour_range[0]
    end_hour = hour_range[1]
    
    if vehicle == 'alle':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['USTRZUSTAND'] == 0) | (df['USTRZUSTAND'] == 1) | (df['USTRZUSTAND'] == 2))]
    elif vehicle == 'Fußgänger':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['USTRZUSTAND'] == 0) | (df['USTRZUSTAND'] == 1) | (df['USTRZUSTAND'] == 2)) & (df['IstFuss'] == 1)]
    elif vehicle == 'PKW':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['USTRZUSTAND'] == 0) | (df['USTRZUSTAND'] == 1) | (df['USTRZUSTAND'] == 2)) & (df['IstPKW'] == 1)]
    elif vehicle == 'Fahrrad':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['USTRZUSTAND'] == 0) | (df['USTRZUSTAND'] == 1) | (df['USTRZUSTAND'] == 2)) & (df['IstRad'] == 1)]
    else:
        filtered_df = pd.DataFrame(columns=df.columns)  # Leerer DataFrame, wenn kein Fahrzeugtyp ausgewählt ist
    
    if roadcondition == 'alle':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['IstFuss'] == 1) | (df['IstPKW'] == 1) | (df['IstRad'] == 1))]
    elif roadcondition == 'trocken':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['IstFuss'] == 1) | (df['IstPKW'] == 1) | (df['IstRad'] == 1)) & (df['USTRZUSTAND'] == 0)]
    elif roadcondition == 'nass/ feucht':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['IstFuss'] == 1) | (df['IstPKW'] == 1) | (df['IstRad'] == 1)) & (df['USTRZUSTAND'] == 1)]
    elif roadcondition == 'winterglatt':
        filtered_df = df[(df['UWOCHENTAG'].between(start_weekday, end_weekday)) & (df['USTUNDE'].between(start_hour, end_hour)) & ((df['IstFuss'] == 1) | (df['IstPKW'] == 1) | (df['IstRad'] == 1)) & (df['USTRZUSTAND'] == 2)]
    
    locations = filtered_df[['YGCSWGS84', 'XGCSWGS84']].dropna()  # Standorte für Heatmap vorbereiten
    
    
    # Karte erstellen und auf Münster zoomen
    map = folium.Map(location=[muenster_lat, muenster_lon], zoom_start=zoom_level)
    
    # Heatmap erstellen
    heatmap = HeatMap(data=locations, radius=15)
    heatmap.add_to(map)
    
    # Karte anzeigen
    display(map)    
    
# Wochentagsbezeichnungen
weekday_labels = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

# Schieberegler für Wochentagsbereich und Stundenbereich sowie Dropdown-Liste für Fahrzeugtyp erstellen
weekday_range_slider = widgets.IntRangeSlider(value=[1, 7], min=1, max=7, description='Wochentagsbereich:', continuous_update=False, step=1, layout={'width': '400px'}, readout_format='02d')
weekday_range_slider.style.handle_color = '#4287f5'
weekday_range_slider.style.slider_color = '#4287f5'
weekday_range_slider_labels = widgets.Label(value='Wochentage: ' + weekday_labels[weekday_range_slider.value[0]-1] + ' - ' + weekday_labels[weekday_range_slider.value[1]-1])

hour_range_slider = widgets.IntRangeSlider(value=[0, 23], min=0, max=23, description='Stundenbereich:', continuous_update=False, step=1, layout={'width': '400px'})
hour_range_slider.style.handle_color = '#4287f5'
hour_range_slider.style.slider_color = '#4287f5'

vehicle_dropdown = widgets.Dropdown(options=['alle', 'Fußgänger', 'PKW', 'Fahrrad'], description='Am Fahrradunfall beteiligter Fahrzeugtyp:')
roadcondition_dropdown = widgets.Dropdown(options=['alle', 'trocken', 'nass/ feucht', 'winterglatt'], description='Straßenzustand:')

def update_weekday_labels(change):
    start_label = weekday_labels[change['new'][0]-1]
    end_label = weekday_labels[change['new'][1]-1]
    weekday_range_slider_labels.value = 'Wochentage: ' + start_label + ' - ' + end_label

weekday_range_slider.observe(update_weekday_labels, 'value')


# Interaktive Anzeige der Karte mit den Widgets
display(widgets.VBox([weekday_range_slider_labels]))
widgets.interactive(update_map, weekday_range=weekday_range_slider, weekday_range_slider_labels = widgets.Label, hour_range=hour_range_slider, vehicle=vehicle_dropdown, roadcondition=roadcondition_dropdown)
