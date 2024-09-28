import requests
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timezone, timedelta
import csv


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
specific_time = datetime(2024, 10, 1, 15, 1, 23, tzinfo=timezone.utc)
# rfc3339_timestamp = specific_time.isoformat(timespec='seconds')
# traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
# data = json.dumps(traffic_info, indent=2)
# print(json.dumps(traffic_info, indent=2))
# print(traffic_info['routes'][0]['duration'])
# print(traffic_info["data"]["routes"]['duration'])
def calculate(start_lat, start_lon, end_lat, end_lon, api_key, start_time):
    increment = timedelta(minutes=5)
    total_duration = timedelta(hours=1)
    current_time = start_time
    db = []
    while current_time <= start_time + total_duration:
        specific_time = datetime(2024, 10, 1, 15, 1, 23, tzinfo=timezone.utc)
        rfc3339_timestamp = specific_time.isoformat(timespec='seconds')
        #center 
        traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
        print(traffic_info)
        duration = traffic_info['routes'][0]['duration']
        db.append({
            "lat":start_lat,
            "lon":start_lon,
            "timestamp": rfc3339_timestamp,
            "duration": duration,
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
        }
        )
        
        #north-west
        traffic_info = get_traffic_data(start_lat, start_lon + 0.009, end_lat + 0.0124 , end_lon, api_key, rfc3339_timestamp)
        duration = traffic_info['routes'][0]['duration']
        db.append({
            "lat":start_lat + 0.009, 
            "lon":start_lon + 0.0124,
            "timestamp": rfc3339_timestamp,
            "duration": duration,
        }
        )
        #north-east
        traffic_info = get_traffic_data(start_lat, start_lon + 0.009, end_lat - 0.0124 , end_lon, api_key, rfc3339_timestamp)
        duration = traffic_info['routes'][0]['duration']
        db.append({
            "lat":start_lat + 0.009, 
            "lon":start_lon - 0.0124,
            "timestamp": rfc3339_timestamp,
            "duration": duration,
        }
        )
         #south-east
        traffic_info = get_traffic_data(start_lat, start_lon - 0.009, end_lat - 0.0124 , end_lon, api_key, rfc3339_timestamp)
        duration = traffic_info['routes'][0]['duration']
        db.append({
            "lat":start_lat - 0.009, 
            "lon":start_lon - 0.0124,
            "timestamp": rfc3339_timestamp,
            "duration": duration,
        }
        )
        #south-west
        traffic_info = get_traffic_data(start_lat, start_lon - 0.009, end_lat + 0.0124 , end_lon, api_key, rfc3339_timestamp)
        duration = traffic_info['routes'][0]['duration']
        db.append({
            "lat":start_lat - 0.009, 
            "lon":start_lon + 0.0124,
            "timestamp": rfc3339_timestamp,
            "duration": duration,
        }
        )
        current_time += increment

    return db

db = calculate(start_lat, start_lon, end_lat, end_lon, api_key, specific_time)
filename = "output.csv"
# Get the headers (keys of the dictionary) from the first dictionary
headers = db[0].keys()

# Write the data to a CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    
    # Write the header
    writer.writeheader()
    
    # Write the data rows
    writer.writerows(db)


def find_best_point():
    # Path to the CSV file
    csv_file = 'output.csv'

    # Initialize an empty list to store the rows as dictionaries
    data = []

    # Read the CSV file and convert it to a list of dictionaries
    with open(csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Initialize variables to store the minimum duration and the corresponding row
    min_duration = float('inf')
    min_row = None

    # Loop through the list of dictionaries to find the shortest duration
    for row in data:
        # Extract the duration value and convert it to an integer (removing the 's' suffix)
        duration = int(row['duration'].strip('s'))
    
        # Check if this duration is the shortest so far
        if duration < min_duration:
            min_duration = duration
            min_row = row

        # Output the row with the shortest duration
    print(f"Row with the shortest duration: {min_row}")

# find_best_point()