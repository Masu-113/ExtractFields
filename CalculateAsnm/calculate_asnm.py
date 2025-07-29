import pandas as pd
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Lee el archivo CSV
df = pd.read_csv("coordenadas.csv", sep=';')
# Inicializa el geolocalizador
geolocator = Nominatim(user_agent="altitud_calculator")

# Función para obtener la altitud
def get_altitude(latitude, longitude):
    location = geolocator.reverse((latitude, longitude), exactly_one=True, language='es')
    if location and 'altitude' in location.raw['address']:
        return location.raw['address']['altitude']
    else:
        return None

# Aplica la función a cada fila del DataFrame
df['altitud'] = df.apply(lambda row: get_altitude(row['latitud'], row['longitud']), axis=1)

# Guarda los resultados en un nuevo archivo CSV o DataFrame
df.to_csv("coordenadas_con_altitud.csv", index=False)
print(df)