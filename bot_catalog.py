import csv
from datetime import datetime
from bot import BOT

class BOTCatalog:
    def __init__(self):
        self.bot_dict = {}
        self.load_data_from_csv("data/emissioni.csv")

    def load_data_from_csv(self, csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Nome BOT']
                isin = row['ISIN']
                issuance_date = datetime.strptime(row['DATA EMISSIONE'], '%d/%m/%Y').date()
                issuance_price = row['PREZZO EMISSIONE']
                maturity_date = datetime.strptime(row['SCADENZA'], '%d/%m/%Y').date()
                bot = BOT(name, isin, issuance_date, issuance_price, maturity_date)
                self.bot_dict[name] = bot

    def get_bot_list(self):
        return list(self.bot_dict.values())

    def get_bot(self, name):
        return self.bot_dict.get(name)

# Esempio di utilizzo della classe BOTCatalog
if __name__ == "__main__":
    catalog = BOTCatalog()
    
    # Ottenere un singolo BOT per nome
    #bot_name = "Bot Zc St23 S Eur"
    #bot = catalog.get_bot(bot_name)
    #if bot:
    #    print(f"Nome BOT: {bot.nome}")
    #    print(f"ISIN: {bot.isin}")
    #    print(f"Data Emissione: {bot.data_emissione}")
    #    print(f"Prezzo Emissione: {bot.prezzo_emissione}")
    #    print(f"Scadenza: {bot.scadenza}")
    #else:
    #   print(f"BOT con nome '{bot_name}' non trovato.")
    
    # Ottenere la lista di tutti i BOT come lista
    bot_list = catalog.get_bot_list()
    for bot in bot_list:
        print(f"Nome BOT: {bot.name}")
        print(f"ISIN: {bot.isin}")
        print(f"Data Emissione: {bot.issuance_date}")
        print(f"Prezzo Emissione: {bot.issuance_price}")
        print(f"Scadenza: {bot.maturity_date}")