class Quote:
    def __init__(self, cid, symbol, name, price, last_updated):
        self.cid = cid
        self.symbol = symbol
        self.name = name
        self.price = price
        self.last_updated = last_updated

    def __str__(self):
        return f"Quote(cid={self.cid}, symbol={self.symbol}, name={self.name}, price={self.price}, last_updated={self.last_updated})"