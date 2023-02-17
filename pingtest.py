import csv
import subprocess
import os
import time
import matplotlib.pyplot as plt

# Define the hosts to ping and the number of times to ping it
hosts = ["10.0.200.2", "10.0.200.5", "1.1.1.1", "8.8.8.8"]
num_pings = 25

# Create a new directory for the report files
timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
report_dir = f"report-{timestamp}"
os.mkdir(report_dir)

# Ping each host x times and log the results to a separate CSV file
for host in hosts:
    # Open a CSV file to write the ping results to
    csv_file_path = os.path.join(report_dir, f'ping_results_{host}.csv')
    with open(csv_file_path, mode='w', newline='') as csv_file:
        # Create a CSV writer object
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow(['Ping number', 'Response Time (ms)'])

        # Ping the host x times and log the results to the CSV file
        for i in range(1, num_pings + 1):
            # Run the ping command
            ping_process = subprocess.Popen(['ping', '-c', '1', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Get the output and error streams
            ping_output, ping_error = ping_process.communicate()

            # Parse the ping output to get the response time and status
            ping_output = ping_output.decode('utf-8')
            response_time = None
            for line in ping_output.split('\n'):
                print(line)
                if 'time=' in line:
                    response_time = float(line.split('time=')[1].split(' ')[0])

            # Write the ping results to the CSV file
            writer.writerow([i, response_time])

            # Add a delay of 1 second between pings
            time.sleep(1)

    print(f'Ping results for host {host} saved to file {csv_file_path}')

print(f'All ping results saved to directory {report_dir}')

# Generate graphs for each host
for host in hosts:
    # Open the CSV file for the host
    csv_file_path = os.path.join(report_dir, f'ping_results_{host}.csv')
    with open(csv_file_path, mode='r') as csv_file:
        # Create a CSV reader object
        reader = csv.reader(csv_file)

        # Skip the header row
        next(reader)

        # Extract the ping results and convert to a list of floats
        ping_results = [float(row[1]) for row in reader]

    # Generate a graph for the host
    fig, ax = plt.subplots()
    ax.plot(ping_results)
    ax.set_xlabel('Ping number')
    ax.set_ylabel('Response Time (ms)')
    ax.set_title(f'Ping Results for {host}')
    fig.savefig(os.path.join(report_dir, f'{host}_graph.png'))

# Generate a combined graph for all hosts
fig, ax = plt.subplots()
for host in hosts:
    csv_file_path = os.path.join(report_dir, f'ping_results_{host}.csv')
    with open(csv_file_path, mode='r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        ping_results = [float(row[1]) for row in reader]

    ax.plot(ping_results, label=host)

ax.set_xlabel('Ping number')
ax.set_ylabel('Response Time (ms)')
ax.set_title('Ping Results for All Hosts')
ax.legend()
fig.savefig(os.path.join(report_dir, 'combined_graph'))