class Quote:
    def __init__(self, ora, ultimo_prezzo, variazione, apertura, min_value, max_value):
        self.ora = ora
        self.ultimo_prezzo = float(ultimo_prezzo.replace(',', '.'))
        self.variazione = variazione
        self.apertura = apertura
        self.min = min_value
        self.max = max_value
