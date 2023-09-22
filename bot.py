class BOT:
    def __init__(self, nome, isin, data_emissione, prezzo_emissione, scadenza):
        self.nome = nome
        self.isin = isin
        self.data_emissione = data_emissione
        self.prezzo_emissione = float(prezzo_emissione.replace(',', '.'))
        self.scadenza = scadenza
        self.last_quote = None
