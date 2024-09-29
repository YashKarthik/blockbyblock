import pandas as pd
import numpy as np
import os

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

# Step 1: Read the CSV into a pandas DataFrame
csv_file = 'output.csv'  # Replace with the actual path to your CSV file
df = pd.read_csv(csv_file, header=None, names=['latitude', 'longitude', 'timestamp', 'seconds'], skiprows=1)

# Step 2: Clean up the 'seconds' column by removing the 's' suffix
df['seconds'] = df['seconds'].str.rstrip('s')

# Step 3: Create an output directory for the CSV files (optional)
output_dir = 'clusters_output'
os.makedirs(output_dir, exist_ok=True)

# Step 4: Group by 'timestamp' and process each group
for timestamp, group in df.groupby('timestamp'):
    cluster_lats, cluster_lons = [], []
    
    # For each row in the group, generate clusters
    for _, row in group.iterrows():
        lat, lon, seconds = row['latitude'], row['longitude'], row['seconds']
        cluster_lat, cluster_lon = generate_clusters(lat, lon, seconds)
        cluster_lats.extend(cluster_lat)
        cluster_lons.extend(cluster_lon)
    
    # Create a DataFrame for the clusters of this timestamp
    data = {
        'Latitude': cluster_lats,
        'Longitude': cluster_lons
    }
    df_clusters = pd.DataFrame(data)
    
    # Sanitize the timestamp for use in filenames by replacing ':' and other invalid characters
    sanitized_timestamp = timestamp.replace(':', '-').replace('T', '_').replace('Z', '')

    # Step 5: Save the DataFrame to a CSV file, using the sanitized timestamp in the filename
    output_file = os.path.join(output_dir, f'clusters_{sanitized_timestamp}.csv')
    df_clusters.to_csv(output_file, index=False)
    print(f'Saved: {output_file}')
