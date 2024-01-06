import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from src.model.bot import BOT
from src.services.bot_catalog_service import BOTCatalogService
from src.model.quote import Quote

class QuoteDownloader:
    def __init__(self, bot_catalog):
        self.bot_catalog = bot_catalog

    def __parse_datetime(self, datetime_raw):
        current_year = datetime.now().year
        current_date = datetime.now().date()
        try:
            # Prova a convertire l'orario nel formato HH.mm
            parsed_time = datetime.strptime(datetime_raw, "%H.%M")
            return datetime(current_year, current_date.month, current_date.day, parsed_time.hour, parsed_time.minute, 0)
        except ValueError:
            # Se non riesce, assume che l'orario sia una data nel formato DD/MM
            day, month = map(int, datetime_raw.split('/'))
            return datetime(current_year, month, day, 17, 49, 59)

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
                            datetime_raw = columns[1].text.strip()
                            datetime = self.__parse_datetime(datetime_raw)
                            last_price = float(columns[2].text.strip().replace(',', '.'))
                            variation = float(columns[3].text.strip().replace(',', '.').replace('"', '').replace('%',''))
                            opening = float(columns[4].text.strip().replace(',', '.'))
                            min_max = columns[5].text.strip()
                            if min_max == "---":
                                min_value = max_value = None
                            else:
                                min_value_str, max_value_str = map(str.strip, min_max.split('-'))
                                min_value=float(min_value_str.replace(',', '.'))
                                max_value=float(max_value_str.replace(',', '.'))
                            quote = Quote(datetime, last_price, variation, opening, min_value, max_value)
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
                    writer.writerow([bot.name, bot.last_quote.datetime.strftime("%d/%m/%Y %H:%M:%S"), bot.last_quote.last_price, bot.last_quote.variation, bot.last_quote.opening, bot.last_quote.min, bot.last_quote.max])

if __name__ == "__main__":
    # Carica la lista di BOT dal file CSV
    catalog = BOTCatalogService()
    # Crea un oggetto QuoteDownloader
    quote_downloader = QuoteDownloader(catalog)
    # Scarica le quotazioni
    quote_downloader.download_quotes()
    # Salva le quotazioni aggiornate nel file CSV
    quote_downloader.save_quotes_to_csv('data/quotazioni.csv')
