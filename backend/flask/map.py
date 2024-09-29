import requests
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timezone, timedelta
import csv
import pandas as pd
import numpy as np


load_dotenv()

def get_traffic_data(origin_lat, origin_lng, destination_lat, destination_lng, api_key, date):
    # URL for the Google Routes API
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    
    # Payload for the POST request
    payload = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": origin_lat,
                    "longitude": origin_lng
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": destination_lat,
                    "longitude": destination_lng
                }
            }
        },
        "travelMode": "DRIVE",
        "departureTime": date,
        "routingPreference": "TRAFFIC_AWARE",
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "IMPERIAL"
    }

    # Headers for the request
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline'
    }

    # Send POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        return data
    else:
        # Return an error message
        return {'error': f"Error: {response.status_code}, {response.text}"}

# Example usage
api_key = os.getenv('API_KEY')  # Replace with your Google API key
# Print the response nicely
print(api_key)
end_lat = 43.64362914180176
end_lon = -79.37915254421802
start_lat = 43.67115047619613
start_lon = -79.39290231417031
#current_time = datetime.now(timezone.utc)
#specific_time = datetime(2024, 9, 1, 15, 1, 23, tzinfo=timezone.utc)
EDT = timezone(timedelta(hours=-4))
specific_time = datetime(2024, 10, 28, 19, 30, 0, tzinfo=EDT)

# rfc3339_timestamp = specific_time.isoformat(timespec='seconds')
# traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
# data = json.dumps(traffic_info, indent=2)
# print(json.dumps(traffic_info, indent=2))
# print(traffic_info['routes'][0]['duration'])
# print(traffic_info["data"]["routes"]['duration'])

def calculate(start_lat, start_lon, end_lat, end_lon, api_key, start_time, offset):
    db = []
    rfc3339_timestamp = start_time.isoformat(timespec='seconds') + "Z"
    #center 
    traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
    print(traffic_info)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat,
        "lon":start_lon,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    print("center complete")
    #north
    traffic_info = get_traffic_data(start_lat, start_lon + 0.0045, end_lat, end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat + 0.0045,
        "lon":start_lon,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    #south
    traffic_info = get_traffic_data(start_lat, start_lon - 0.0045, end_lat, end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat - 0.0045,
        "lon":start_lon,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    #east
    traffic_info = get_traffic_data(start_lat, start_lon , end_lat - 0.0062, end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat, 
        "lon":start_lon - 0.0062,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    #west
    traffic_info = get_traffic_data(start_lat, start_lon , end_lat + 0.0062, end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat, 
        "lon":start_lon + 0.0062,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    
    #north-west
    traffic_info = get_traffic_data(start_lat, start_lon + 0.00225, end_lat + 0.0031 , end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat + 0.00225, 
        "lon":start_lon + 0.0031,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    #north-east
    traffic_info = get_traffic_data(start_lat, start_lon + 0.00225, end_lat - 0.0031 , end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat + 0.00225, 
        "lon":start_lon - 0.0031,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
        #south-east
    traffic_info = get_traffic_data(start_lat, start_lon - 0.00225, end_lat - 0.0031 , end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat - 0.00225, 
        "lon":start_lon - 0.0031,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    #south-west
    traffic_info = get_traffic_data(start_lat, start_lon - 0.00225, end_lat + 0.0031 , end_lon, api_key, rfc3339_timestamp)
    duration = traffic_info['routes'][0]['duration']
    db.append({
        "lat":start_lat - 0.00225, 
        "lon":start_lon + 0.0031,
        "timestamp": rfc3339_timestamp,
        "duration": duration,
        "offset": offset,
    }
    )
    return db

def calculate_total(start_lat, start_lon, end_lat, end_lon, api_key, start_time):
    increment = timedelta(minutes=5)
    total_duration = timedelta(hours=1)
    current_time = start_time
    db = []
    offset = 0
    while current_time <= start_time + total_duration:
        db += calculate(start_lat, start_lon, end_lat, end_lon, api_key, current_time,offset)
        current_time += increment
        offset += 5
    return db

def generate_clusters(lat, lon, seconds, scale_factor=30, spread=0.003):
    # Number of points to generate is proportional to the seconds value
    num_points = int(int(seconds) / scale_factor)  # Strip the 's' from the seconds value
    # Random points around (lat, lon), uniformly distributed within a square region
    lat_offsets = np.random.uniform(0, spread, num_points)
    lon_offsets = np.random.uniform(0, spread, num_points)
    
    cluster_lat = lat + lat_offsets
    cluster_lon = lon + lon_offsets
    
    return cluster_lat, cluster_lon


def mega_cluster(df):
    df['duration'] = df['duration'].str.rstrip('s')
    all_clusters = pd.DataFrame()

    for timestamp, group in df.groupby('timestamp'):
        cluster_lats, cluster_lons, cluster_offset = [], [], []
        
        # For each row in the group, generate clusters
        for _, row in group.iterrows():
            lat, lon, seconds, offset = row['lat'], row['lon'], row['duration'], row['offset']
            cluster_lat, cluster_lon = generate_clusters(lat, lon, seconds)
            cluster_lats.extend(cluster_lat)
            cluster_lons.extend(cluster_lon)
            cluster_offset.extend([offset] * len(cluster_lat))  # Or len(cluster_lon) since both should have the same length
        
        # Create a DataFrame for the clusters of this timestamp
        data = {
            'lat': cluster_lats,
            'lon': cluster_lons,
            'offset': cluster_offset
        }
        df_clusters = pd.DataFrame(data)
        all_clusters = pd.concat([all_clusters, df_clusters], ignore_index=True)
    return all_clusters
        
        # Sanitize the timestamp for use in filenames by replacing ':' and other invalid character

def find_best_point(df):
    # Initialize variables to store the minimum duration and the corresponding row
    min_duration = float('inf')
    min_row = None

    # Loop through the list of dictionaries to find the shortest duration
    for index, row in df.iterrows():
        # Extract the duration value and convert it to an integer (removing the 's' suffix)
        duration = int(row['duration'].strip('s'))
    
        # Check if this duration is the shortest so far
        if duration < min_duration:
            min_duration = duration
            min_row = row

        # Output the row with the shortest duration
    print(f"Row with the shortest duration: {min_row}")
    return min_row

def generate_geoJSON(start_lat, start_lon, end_lat, end_lon):
    start_time = datetime.now()
    increment = timedelta(minutes=5)
    EDT = timedelta(hours=4)
    start_time += increment
    start_time += EDT
    print(start_time)
    # start_time += EDT
    api_key = os.getenv('API_KEY') 
    data = calculate_total(start_lat, start_lon, end_lat, end_lon, api_key, start_time)
    df = pd.DataFrame(data)
    min_row = find_best_point(df)
    best_point = {
        "lat": min_row['lat'],
        "lon": min_row['lon'],
        "offset": min_row['offset']
    }
    #print(best_point)
    df_clusters = mega_cluster(df)
    geojson = dataframe_to_geojson(df_clusters)
    print(geojson)
    with open('my_dict.json', 'w') as json_file:
        json.dump(geojson, json_file, indent=4)
    return geojson , best_point


import pandas as pd

def dataframe_to_geojson(df):
    features = []

    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Assuming the DataFrame has columns: 'lat', 'lon', and 'offset'
        lat = row['lat']
        lon = row['lon']
        offset = row['offset']

        # Create the GeoJSON feature for each row
        feature = {
            "id": str(index),
            "type": "Feature",
            "properties": {
                "lat": float(lat),
                "lon": float(lon),
                "offset": int(offset)  # Assuming offset is an integer
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(lon), float(lat)]
            }
        }
        features.append(feature)

    # Create the GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return geojson


# Function to convert CSV data to GeoJSON
def csv_to_geojson(csv_data):
    reader = csv.reader(csv_data.splitlines())
    headers = next(reader)  # Get the headers from the first line
    features = []
    
    for index, row in enumerate(reader):
        if row:  # Ignore empty rows
            lat, lon, offset = row
            feature = {
                "id": str(index),
                "type": "Feature",
                "properties": {
                    "lat": float(lat),
                    "lon": float(lon),
                    "offset": int(offset)  # Assuming offset is an integer
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lon), float(lat)]
                }
            }
            features.append(feature)
    
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    return geojson


# generate_geoJSON(start_lat, start_lon, end_lat, end_lon)

#print(datetime.now())