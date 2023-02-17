import csv
import socket
import time

from datetime import datetime
from icmplib import ping


ip_list = ["1.1.1.1", "8.8.8.8"]  # replace with your list of hosts
ping_count = 200  # how many times to ping each host

ping_results = []

for i in range(ping_count):
    for ip in ip_list:
        # Ping the host
        response = ping(ip, count=1)
        # Add detailed results to the ping results list
        ping_results.append({
            "IP": response.address,
            "Source": socket.gethostname(),
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Latency (ms)": response.avg_rtt
        })
    # Wait 1 second before the next ping
    time.sleep(1)

# Export the ping results to a CSV file
with open('ping_results.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["IP", "Source", "Time", "Latency (ms)"])
    writer.writeheader()
    writer.writerows(ping_results)
