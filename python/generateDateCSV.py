import csv
from datetime import datetime, timedelta

def generate_dates(start_year, end_year):
    # Define as datas de início e fim
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    # Gera as datas
    current_date = start_date
    while current_date <= end_date:
        yield current_date.strftime('%Y%m%d')
        current_date += timedelta(days=1)

def save_to_csv(start_year, end_year, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for date in generate_dates(start_year, end_year):
            writer.writerow([date])

# Exemplo de uso:
start_year = 2020
end_year = 2022
filename = "dates.csv"
save_to_csv(start_year, end_year, filename)
