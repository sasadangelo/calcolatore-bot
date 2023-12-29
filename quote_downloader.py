import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from bot import BOT
from bot_catalog import BOTCatalog
from quote import Quote

class QuoteDownloader:
    def __init__(self, bot_catalog):
        self.bot_catalog = bot_catalog

    def __parse_ora(self, ora_raw):
        current_year = datetime.now().year
        current_date = datetime.now().date()
        try:
            # Prova a convertire l'orario nel formato HH.mm
            parsed_time = datetime.strptime(ora_raw, "%H.%M")
            return datetime(current_year, current_date.month, current_date.day, parsed_time.hour, parsed_time.minute, 0).strftime("%d/%m/%Y %H:%M:%S")
        except ValueError:
            # Se non riesce, assume che l'orario sia una data nel formato DD/MM
            day, month = map(int, ora_raw.split('/'))
            return datetime(current_year, month, day).strftime("%d/%m/%Y 00:00:00")

    def download_quotes(self):
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
                        # Controlla se il BOT esiste nel catalogo, se si allora bisogna prelevare la quotazione.
                        bot = self.bot_catalog.get_bot(bot_name)
                        if bot:
                            ora_raw = columns[1].text.strip()
                            ora = self.__parse_ora(ora_raw)
                            ultimo_prezzo = columns[2].text.strip()
                            variazione = columns[3].text.strip()
                            apertura = columns[4].text.strip()
                            min_max = columns[5].text.strip()
                            if min_max == "---":
                                min_value = max_value = None
                            else:
                                min_value, max_value = map(str.strip, min_max.split('-'))
                            quote = Quote(ora, ultimo_prezzo, variazione, apertura, min_value, max_value)
                            bot.last_quote = quote
            else:
                print(f"Tabella non trovata su {url}")
        else:
            print(f"Errore nella richiesta HTTP per {url}")

    def save_quotes_to_csv(self, csv_file):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Scrivi l'intestazione del file CSV
            writer.writerow(['Nome BOT', 'Ora', 'Ultimo Prezzo', 'Variazione', 'Apertura', 'Min', 'Max'])
            # Scrivi i dati delle quotazioni aggiornate nel file CSV
            for bot in self.bot_catalog.get_bot_list():
                if bot.last_quote:
                    ultimo_prezzo = bot.last_quote.ultimo_prezzo.replace(',', '.').replace('"', '')
                    variazione = bot.last_quote.variazione.replace(',', '.').replace('"', '')
                    apertura = bot.last_quote.apertura.replace(',', '.').replace('"', '')
                    min_value = bot.last_quote.min.replace(',', '.').replace('"', '') if bot.last_quote.min else ''
                    max_value = bot.last_quote.max.replace(',', '.').replace('"', '') if bot.last_quote.max else ''
                    writer.writerow([bot.name, bot.last_quote.ora, ultimo_prezzo, variazione, apertura, min_value, max_value])

if __name__ == "__main__":
    # Carica la lista di BOT dal file CSV
    catalog = BOTCatalog()

    # Crea un oggetto QuoteDownloader
    quote_downloader = QuoteDownloader(catalog)

    # Scarica le quotazioni
    quote_downloader.download_quotes()

    # Salva le quotazioni aggiornate nel file CSV
    quote_downloader.save_quotes_to_csv('data/quotazioni.csv')
