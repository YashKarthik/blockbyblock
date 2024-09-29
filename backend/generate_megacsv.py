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
