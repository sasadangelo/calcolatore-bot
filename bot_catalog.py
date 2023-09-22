import csv
from bot import BOT

class BOTCatalog:
    def __init__(self, csv_file):
        self.bot_list = []
        self.load_data_from_csv(csv_file)

    def load_data_from_csv(self, csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                nome = row['Nome BOT']
                isin = row['ISIN']
                data_emissione = row['DATA EMISSIONE']
                prezzo_emissione = row['PREZZO EMISSIONE']
                scadenza = row['SCADENZA']
                bot = BOT(nome, isin, data_emissione, prezzo_emissione, scadenza)
                self.bot_list.append(bot)

    def get_bot_list(self):
        return self.bot_list