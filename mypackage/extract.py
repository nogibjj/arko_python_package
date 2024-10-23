import requests
import csv

def extract():
    url = 'https://raw.githubusercontent.com/MainakRepositor/Datasets/refs/heads/master/Stocks/AAPL.csv'

    response = requests.get(url)
    response.raise_for_status()
    csv_file = 'data/AAPL.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            writer.writerow(decoded_line.split(','))

    print(f'Data saved to {csv_file}')
