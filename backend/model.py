# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the dataset
# file_path = 'updated_locational_prices.csv'  # assuming the dataset is uploaded with this file path
# data = pd.read_csv(file_path)

# # Clean and preprocess the data
# # Convert duration to integer by removing 's'
# data['duration'] = data['duration'].str.strip('s').astype(int)

# # Plot Duration vs Price
# # plt.figure(figsize=(10, 6))
# # plt.scatter(data['duration'], data['total_price'], color='blue')
# # plt.title('Duration vs Price')
# # plt.xlabel('Duration (seconds)')
# # plt.ylabel('Price ($)')
# # plt.grid(True)
# correlation = data['duration'].corr(data['total_price'])
# print(f"Correlation between Duration and Price: {correlation}")
# Display the plot
# plt.show()


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression

# Load the dataset
file_path = 'updated_locational_prices.csv'  # assuming the dataset is uploaded with this file path
data = pd.read_csv(file_path)
# file_path = 'updated_locational_prices.csv'  # assuming the dataset is uploaded with this file path


# Clean and preprocess the data
data['duration'] = data['duration'].str.strip('s').astype(int)

# Use price as the main feature for clustering
X = data[['total_price']]  # Use price for clustering

# Apply KMeans clustering with 2 clusters (top and bottom price clusters)
kmeans = KMeans(n_clusters=2, random_state=42)
data['cluster'] = kmeans.fit_predict(X)

# Initialize list to store slopes
slopes = []

# Scatter plot of the clustered data
plt.scatter(data['duration'], data['total_price'], c=data['cluster'], cmap='viridis', label='Data points')

# Create two separate Linear Regression models for each cluster
for cluster in range(2):
    cluster_data = data[data['cluster'] == cluster]
    
    # Prepare data for linear regression
    X_cluster = cluster_data[['duration']].values  # Independent variable (duration)
    y_cluster = cluster_data['total_price'].values  # Dependent variable (price)
    
    # Train a Linear Regression model for the cluster
    model = LinearRegression()
    model.fit(X_cluster, y_cluster)
    
    # Store the slope (coefficient of 'duration')
    slope = model.coef_[0]
    slopes.append(slope)
    
    # Plot the regression line for the cluster
    plt.plot(cluster_data['duration'], model.predict(X_cluster), label=f'Trendline for Cluster {cluster}')

# Calculate the average slope
average_slope = np.mean(slopes)
print(f"Average slope of the two lines: {average_slope}")

# Add labels and title
plt.title('Duration vs Price with Two Linear Regression Models')
plt.xlabel('Duration (seconds)')
plt.ylabel('Price ($)')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()

slope = 0.012175451693711713

def predict_price(slope, dur1, price1, dur2):
    slope = 0.012175451693711713
    intercept = price1 - slope * dur1
    price2 = slope * dur2 + intercept
    return price2

