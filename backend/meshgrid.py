import pandas as pd
import numpy as np
import csv
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# df = pd.read_csv('output.csv')
# lat = df['lat'].values
# lon = df['lon'].values
# z = df['duration'].values
# lat_vals = np.linspace(df['lat'].min(), df['lat'].max(), 10)
# lon_vals = np.linspace(df['lon'].min(), df['lon'].max(), 10)
# df['duration'] = df['duration'].str.rstrip('s')
#LAT, LON = np.meshgrid(lat_vals, lon_vals)
#grid_duration = np.empty_like(lat_grid)
# Z = griddata((df['lat'].values, df['lon'].values), df['duration'].values, (lat_vals, lon_vals), method='linear')
# lat_grid, lon_grid = np.meshgrid(np.linspace(min(lat), max(lat), 100), 
#                                  np.linspace(min(lon), max(lon), 100))
# z_grid = griddata((lat, lon), z, (lat_grid, lon_grid), method='cubic')


# plt.figure(figsize=(8, 6))
# plt.contourf(lon_grid, lat_grid, z_grid, levels=20, cmap='viridis')
# plt.colorbar(label='Duration (z)')
# plt.scatter(lon, lat, color='red')  # Show original points
# plt.title('Interpolated Duration over Latitude and Longitude')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()
# # LAT_flat = LAT.flatten()
# LON_flat = LON.flatten()
# Z_flat = Z.flatten()

# df = pd.DataFrame({
#     'Latitude': LAT_flat,
#     'Longitude': LON_flat,
#     'Z_value': Z_flat
# })

# df.to_csv('meshgrid_data.csv',index=False)

# Step 1: Read the CSV into a pandas DataFrame
csv_file = 'new_test.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file, header=None, names=['latitude', 'longitude', 'timestamp', 'seconds'], skiprows=1)

# Step 2: Extract the relevant columns (ignoring timestamp)
df['seconds'] = df['seconds'].str.rstrip('s')
# print(df['seconds'])
points = df[['latitude', 'longitude', 'seconds']]
# print(points)

# Function to generate clusters around a point
def generate_clusters(lat, lon, seconds, scale_factor=30, spread=0.003):
    # Number of points to generate is proportional to the seconds value
    num_points = int(int(seconds) / scale_factor)  # Strip the 's' from the seconds value
    # Random points around (lat, lon), uniformly distributed within a square region
    lat_offsets = np.random.uniform(0, spread, num_points)
    lon_offsets = np.random.uniform(0, spread, num_points)
    
    cluster_lat = lat + lat_offsets
    cluster_lon = lon + lon_offsets
    
    return cluster_lat, cluster_lon

# Step 3: Generate clusters for each point based on their seconds value
cluster_lats, cluster_lons = [], []
for _, row in points.iterrows():
    lat, lon, seconds = row['latitude'], row['longitude'], row['seconds']
    cluster_lat, cluster_lon = generate_clusters(lat, lon, seconds)
    cluster_lats.extend(cluster_lat)
    cluster_lons.extend(cluster_lon)

# Step 4: Plot the generated clusters on a map (scatter plot for simplicity)
# plt.scatter(cluster_lons, cluster_lats, alpha=0.6)
# plt.title("Clusters of Points Based on Seconds Values")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.grid(True)
# plt.show()

data = {
    'Latitude': cluster_lats,
    'Longitude': cluster_lons
}

# Create a DataFrame from the data
df_clusters = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df_clusters.to_csv('clusters_output.csv', index=False)
