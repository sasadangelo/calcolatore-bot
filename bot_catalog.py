import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from bot import BOT

class BOTCatalog:
    def __init__(self):
        self.bot_dict = {}
        self.__load_data_from_csv("data/emissioni.csv")

    def __load_data_from_csv(self, csv_file):
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
                                    issuance_price_str = bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label37'}).text.strip()

                                    issuance_date_str = bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label36'}).text.strip()
                                    issuance_date = datetime.strptime(issuance_date_str, '%d/%m/%Y').date()

                                    maturity_date_str = bot_detail_soup.find('span', {'id': 'ctl00_phContents_ctlInfoTitolo_Label34'}).text.strip()
                                    maturity_date = datetime.strptime(maturity_date_str, '%d/%m/%Y').date()

                                    # Aggiungi il nuovo BOT al catalogo
                                    new_bot = BOT(bot_name, isin, issuance_date, issuance_price_str, maturity_date)
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
    
    # Ottenere la lista di tutti i BOT 
    #bot_list = catalog.get_bot_list()
    #for bot in bot_list:
    #    print(f"Nome BOT: {bot.name}")
    #    print(f"ISIN: {bot.isin}")
    #    print(f"Data Emissione: {bot.issuance_date}")
    #    print(f"Prezzo Emissione: {bot.issuance_price}")
    #    print(f"Scadenza: {bot.maturity_date}")
         # Calcolare la durata in giorni
    #    duration = (bot.maturity_date - bot.issuance_date).days
         # Calcolare il guadagno e il rendimento all'emissione
    #    gain = 100 - bot.issuance_price
    #    yield_percent = (gain * 100) / bot.issuance_price * (365 / duration) if duration != 0 else 0
         # Stampa la Durata e il Rendimento all'emissione
    #    print(f"Durata: {duration} giorni")
    #    print(f"Rendimento Emissione: {yield_percent:.2f}%")
    #    print("-" * 30)  # Aggiungiamo una linea separatrice tra i risultati di diversi BOT

    catalog.update()
    catalog.save()