import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.model.bot import BOT
from src.model.quote import Quote

class BOTCatalogService:
    def __init__(self):
        self.bot_dict = {}
        self.quote_dict = {}
        self.__load_quote_from_csv("data/quotazioni.csv")
        self.__load_data_from_csv("data/emissioni.csv")

    def __load_data_from_csv(self, csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Nome BOT']
                isin = row['ISIN']
                issuance_date = datetime.strptime(row['DATA EMISSIONE'], '%d/%m/%Y').date()
                issuance_price = float(row['PREZZO EMISSIONE'])
                maturity_date = datetime.strptime(row['SCADENZA'], '%d/%m/%Y').date()
                bot = BOT(name, isin, issuance_date, issuance_price, maturity_date)
                bot.last_quote = self.quote_dict.get(name) 
                self.bot_dict[name] = bot

    def __load_quote_from_csv(self, csv_file):
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Nome BOT']
                quote_datetime = datetime.strptime(row['Ora'], '%d/%m/%Y %H:%M:%S')
                last_price = float(row['Ultimo Prezzo'])
                variation = float(row["Variazione"])
                opening = float(row["Apertura"])
                min_value = float(row["Min"]) if row["Min"] != '' else None
                max_value = float(row["Max"]) if row["Max"] != '' else None
                quote = Quote(quote_datetime, last_price, variation, opening, min_value, max_value)
                self.quote_dict[name] = quote

    def update(self):
        url = "https://www.teleborsa.it/Quotazioni/BOT"

        # Effettua la richiesta HTTP
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Trova la tabella con le quotazioni
            table = soup.find('table', {'id': 'ctl00_phContents_ctlListing_gvGrid'})

            if table:
                # Cerca le righe della tabella
                rows = table.find_all('tr')
                for row in rows:
                    columns = row.find_all('td')
                    if len(columns) >= 2:
                        bot_name = columns[0].text.strip()
                        if not bot_name in self.bot_dict:
                            link_tag = columns[0].find('a')
                            if link_tag:
                                href_attribute = link_tag.get('href')
                                bot_detail_url = f"https://www.teleborsa.it{href_attribute}"
                                isin = href_attribute.split('/')[2].split('-')[5].upper()

                                # Effettua la richiesta HTTP per la pagina dettagliata del BOT
                                bot_detail_response = requests.get(bot_detail_url)
                                if bot_detail_response.status_code == 200:
                                    bot_detail_soup = BeautifulSoup(bot_detail_response.text, 'html.parser')

                                    # Estrai prezzo di emissione, data di emissione e scadenza dalla pagina dettagliata
                                    issuance_price = float(bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label37'}).text.strip().replace(",","."))

                                    issuance_date_str = bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label36'}).text.strip()
                                    issuance_date = datetime.strptime(issuance_date_str, '%d/%m/%Y').date()

                                    maturity_date_str = bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label34'}).text.strip()
                                    maturity_date = datetime.strptime(maturity_date_str, '%d/%m/%Y').date()

                                    # Aggiungi il nuovo BOT al catalogo
                                    new_bot = BOT(bot_name, isin, issuance_date, issuance_price, maturity_date)
                                    self.bot_dict[bot_name] = new_bot
                                    print(f"Aggiunto il BOT {bot_name} al catalogo.")
                                else:
                                    print(f"Errore nella richiesta HTTP per {bot_detail_url}")
                            else:
                                print(f"Link alla pagina di dettaglio per il BOT {bot_name} inesistente.")
                        else:
                            print(f"BOT {bot_name} già presente nel catalogo.")

    def save(self):
        with open("data/emissioni.csv", mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nome BOT", "ISIN", "DATA EMISSIONE", "PREZZO EMISSIONE", "SCADENZA"])

            # Ordina i BOT per data di emissione prima di scriverli nel file CSV
            sorted_bots = sorted(self.bot_dict.values(), key=lambda bot: bot.issuance_date)

            for bot in sorted_bots:
                # Formatta il prezzo di emissione con esattamente tre cifre decimali
                issuance_price_formatted = "{:.3f}".format(bot.issuance_price)
                writer.writerow([bot.name, bot.isin, bot.issuance_date.strftime('%d/%m/%Y'),
                                 issuance_price_formatted, bot.maturity_date.strftime('%d/%m/%Y')])
    def get_bot_list(self):
        return list(self.bot_dict.values())

    def get_active_bot_list(self):
        current_date = datetime.now().date()
        active_bots = [bot for bot in self.bot_dict.values() if bot.maturity_date >= current_date]
        return active_bots
        
    def get_bot(self, name):
        return self.bot_dict.get(name)

# Esempio di utilizzo della classe BOTCatalog
if __name__ == "__main__":
    catalog = BOTCatalogService()
    catalog.update()
    catalog.save()
