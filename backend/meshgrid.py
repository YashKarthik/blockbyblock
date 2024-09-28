import pandas as pd
import numpy as np
import csv
from scipy.interpolate import griddata

df = pd.read_csv('output.csv')
lat_vals = np.linspace(df['lat'].min(), df['lat'].max(), 10)
lon_vals = np.linspace(df['lon'].min(), df['lon'].max(), 10)
LAT, LON = np.meshgrid(lat_vals, lon_vals)
#grid_duration = np.empty_like(lat_grid)
Z = griddata((df['lat'], df['lon']), df['duration'], (LAT, LON), method='cubic')

LAT_flat = LAT.flatten()
LON_flat = LON.flatten()
Z_flat = Z.flatten()

df = pd.DataFrame({
    'Latitude': LAT_flat,
    'Longitude': LON_flat,
    'Z_value': Z_flat
})

df.to_csv('meshgrid_data.csv',index=False)