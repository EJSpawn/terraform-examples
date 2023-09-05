import csv
import locale
from datetime import datetime, timedelta

# Configurar localidade para português (Brasil)
# Isso pode variar dependendo do sistema. Pode ser necessário ajustar.
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR')
    except locale.Error:
        print("Localidade 'pt_BR' não disponível. Usando padrão.")

def is_leap_year(year):
    """Verifica se um ano é bissexto."""
    return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

def generate_dates(start_year, end_year):
    # Define as datas de início e fim
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)

    # Gera as datas
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y%m%d')
        day_of_week = current_date.strftime('%A')  # Retorna o nome completo do dia da semana
        day = current_date.day
        month = current_date.month
        year = current_date.year
        leap_year = is_leap_year(year)
        
        yield (date_str, day_of_week, day, month, year, leap_year)
        
        current_date += timedelta(days=1)

def save_to_csv(start_year, end_year, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        # Escrever o cabeçalho
        writer.writerow(['Date', 'DayOfWeek', 'Day', 'Month', 'Year', 'IsLeapYear'])
        
        for date_info in generate_dates(start_year, end_year):
            writer.writerow(date_info)

# Exemplo de uso:
start_year = 2020
end_year = 2022
filename = "dates.csv"
save_to_csv(start_year, end_year, filename)