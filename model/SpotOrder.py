import decimal


class SpotOrder:
    def __init__(self, cid, symbol, name, logo, market_price, buy_price, qty, last_updated):
        self.cid = cid
        self.symbol = symbol
        self.name = name
        self.logo = logo
        self.market_price = round(market_price, 7)
        self.buy_price = round(buy_price, 7)
        self.qty = qty
        self.est_cost = round(decimal.Decimal(qty) * decimal.Decimal(self.buy_price), 2)
        self.est_market_cost = decimal.Decimal(qty) * decimal.Decimal(self.market_price)
        self.pnl = round(self.est_market_cost - self.est_cost, 4)
        self.pnl_percent = round((self.pnl / self.est_cost) * 100, 2)
        self.positive = self.pnl >= 0
        self.last_updated = last_updated
        self.link = str(f"/meta_data?cid={self.cid}")

    def __str__(self):
        return f"SpotOrder(cid={self.cid}, symbol={self.symbol}, name={self.name}, market_price={self.market_price}, buy_price={self.buy_price}, qty={self.qty}, pnl={self.pnl}, pnl_percent={self.pnl_percent}, last_updated={self.last_updated}, positive={self.positive})"

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {"cid": self.cid, "symbol": self.symbol, "name": self.name, "logo": self.logo, "market_price": self.market_price, "buy_price": self.buy_price, "qty": self.qty, "est_cost": self.est_cost, "est_market_cost": self.est_market_cost, "pnl": self.pnl, "pnl_percent": self.pnl_percent, "positive": self.positive, "last_updated": self.last_updated, "link": self.link}