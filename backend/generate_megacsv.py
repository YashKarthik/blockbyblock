import os
import pandas as pd

# Set the folder containing CSV files and output file path
folder_path = 'clusters_output'  # Update with your folder path
output_file = 'combined_output.csv'

# Initialize an empty list to store the DataFrames
dataframes = []

# Initialize the incremental value
increment_value = 0

# Loop through all the files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)
        
        # Read the current CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Add a new column with the incremental value
        df['offset'] = increment_value
        
        # Append the DataFrame to the list
        dataframes.append(df)
        
        # Increment the value by 5 for the next CSV
        increment_value += 5

# Concatenate all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a new CSV file
combined_df.to_csv(output_file, index=False)

print(f"Combined CSV has been saved as {output_file}")


#Old price generation

# addr_map = {
# '220 Bloor St W, Toronto, ON M5S 1T8': (43.668900476196136,-79.39600231417032),
# '30 Hillsboro Ave, Toronto, ON M5R 1S7, Canada': (43.675639, -79.392917),
# '127 Avenue Rd, Toronto, ON M5R 2H4': (43.67340047619613,-79.39600231417032),
# 'Yorkville, Toronto, Ontario, Canada': (43.671139, -79.392917),
# '32 Davenport Rd, Toronto, ON M5R 0B5': (43.67340047619613,-79.38980231417031),
# "75 Queen's Park Cres E, Toronto, ON M5S 1K7, Canada": (43.666639, -79.392917),
# '86 Bedford Rd, Toronto, ON M5R 2K9, Canada': (43.671139, -79.399117),
# '77 Bloor St W, Toronto, ON M5S 1M2': (43.668900476196136,-79.38980231417031),
# '2 Bloor St E, Toronto, ON M4W 1A8, Canada': (43.671139, -79.386717)
# }
# def read_prices_csv():
#     file = 'locational_prices.csv'
#     df = pd.read_csv(file)
#     mySet = set()
#     end_lat = 43.64362914180176
#     end_lon = -79.37915254421802
#     start_latitudes = []
#     start_longitudes = []
#     increment = timedelta(days=7)
#     durations = []
#     for index, row in df.iterrows():
#         addr = row['start_location']
#         date_str = row['date']
#         time_str = row['time']
#         start_time = datetime.strptime(date_str + "," + time_str, '%m/%d/%Y,%H:%M:%S')
#         start_time += increment
#         rfc3339_timestamp = start_time.isoformat(timespec='seconds') + 'Z'
#         start_lat, start_lon= addr_map[addr]
#         print(rfc3339_timestamp)
#         print(start_lat)
#         print(start_lon)
#         traffic_info = get_traffic_data(start_lat, start_lon, end_lat, end_lon, api_key, rfc3339_timestamp)
#         print(traffic_info)
#         duration = traffic_info['routes'][0]['duration']
#         start_latitudes.append(start_lat)
#         start_longitudes.append(start_lon)
#         durations.append(duration)
#     df['start_lat'] = start_latitudes
#     df['start_lon'] = start_longitudes
#     df['end_lat'] = end_lat
#     df['end_lon'] = end_lon
#     df['duration'] = durations
#     new_file = 'updated_locational_prices.csv'
#     df.to_csv(new_file, index=False)        # print(row['start_location'], row['total_price'])

# read_prices_csv()

