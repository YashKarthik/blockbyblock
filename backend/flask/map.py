import requests
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timezone, timedelta
import csv
import pandas as pd
import numpy as np
from scrape_prices import get_final_price, get_uber_fare

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
    cur_duration = int(df.iloc[0]["duration"].strip('s'))
    # Loop through the list of dictionaries to find the shortest duration
    for index, row in df.iterrows():
        # Extract the duration value and convert it to an integer (removing the 's' suffix)
        duration = int(row['duration'].strip('s'))
    
        # Check if this duration is the shortest so far
        if duration < min_duration:
            min_duration = duration
            min_row = row

        # Output the row with the shortest duration
    min_row["percent"] = min_duration / cur_duration
    min_row["min_duration"] = min_duration
    min_row["cur_duration"] = cur_duration
    print(f"Row with the shortest duration: {min_row}")
    return min_row

def predict_price(dur1, price1, dur2):
    slope = 0.012175451693711713
    intercept = price1 - slope * dur1
    price2 = slope * dur2 + intercept
    return price2

def generate_geoJSON(start_lat, start_lon, end_lat, end_lon):
    start_time = datetime.now()
    increment = timedelta(minutes=5)
    EDT = timedelta(hours=4)
    start_time += increment
    start_time += EDT
    # print(start_time)
    # start_time += EDT
    api_key = os.getenv('API_KEY') 
    data = calculate_total(start_lat, start_lon, end_lat, end_lon, api_key, start_time)
    df = pd.DataFrame(data)
    min_row = find_best_point(df)
    # rfc3339_timestamp = start_time.isoformat(timespec='seconds') + "Z"
    # traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
    # duration = traffic_info['routes'][0]['duration']
    geo_api_key = os.getenv('GEO_API_KEY')  # Replace with your Google API key

    start_location = get_address_from_coordinates(start_lat, start_lon, geo_api_key)
    end_location = get_address_from_coordinates(end_lat, end_lon, geo_api_key)
    
    price_table = get_uber_fare(start_location, end_location)
    total_price = get_final_price( price_table )
    # dur1 = int(duration.strip('s')) - 10
    # dur2 = int(duration.strip('s'))
    # print(dur1)
    # print(dur2)
    # predicted_price = predict_price(dur1, float(total_price), dur2)
    print(total_price)
    predicted_price = predict_price(min_row["cur_duration"], float(total_price) ,min_row["min_duration"])
    print(predicted_price)
    best_point = {
        "lat": min_row['lat'],
        "lon": min_row['lon'],
        "offset": min_row['offset'],
        "og_price": float(total_price),
        "new_price": predicted_price
    }
    df_clusters = mega_cluster(df)
    geojson = dataframe_to_geojson(df_clusters)
    # print(geojson)
    with open('my_dict.json', 'w') as json_file:
        json.dump(geojson, json_file, indent=4)
    return geojson , best_point

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

def get_address_from_coordinates(lat, lon, api_key):
    # URL for Google Maps Geocoding API
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    # Parameters for the request
    params = {
        'latlng': f'{lat},{lon}',
        'key': api_key
    }

    # Make a GET request to the API
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Check if there are results
        if data['results']:
            # Extract the formatted address from the first result
            return data['results'][0]['formatted_address']
        else:
            return 'No address found for the given coordinates.'
    else:
        return f'Error: Unable to connect to the API (status code: {response.status_code}).'

# Example usage
# latitude = 40.714224
# longitude = -73.961452  # Replace with your actual API key

# api_key = os.getenv('GEO_API_KEY')  # Replace with your Google API key

# print()
# address = get_address_from_coordinates(latitude, longitude, api_key)
# print('Address:', address)


# generate_geoJSON(start_lat, start_lon, end_lat, end_lon)

#print(datetime.now())