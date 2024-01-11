from datetime import datetime

class Quote:
    def __init__(self, quote_datetime=datetime.now(), last_price=0.000, variation=0.000, opening=0.000, min_value=None, max_value=None):
        self.quote_datetime = quote_datetime
        self.last_price = last_price
        self.variation = variation
        self.opening = opening
        self.min = min_value
        self.max = max_value
