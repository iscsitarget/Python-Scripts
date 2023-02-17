import pandas as pd
import matplotlib.pyplot as plt

# Read in the CSV file
df = pd.read_csv('./ping_results.csv')

# Convert the 'Time' column to a datetime data type
df['Time'] = pd.to_datetime(df['Time'])

# Create a pivot table to group the data by IP and Time and calculate the average latency
pivot = pd.pivot_table(df, values='Latency (ms)', index='Time', columns='IP', aggfunc='mean')

# Create a line plot of the latency data
pivot.plot()
plt.xlabel('Time')
plt.ylabel('Latency (ms)')
plt.title('Latency over Time')

# Save the plot to a PNG file
plt.savefig('latency.png')