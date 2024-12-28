class SpotView:
    def __init__(self, spot_orders):
        self.spot_orders = spot_orders
        self.total_cost = round(sum(spot.est_cost for spot in spot_orders), 7)
        self.total_market_cost = round(sum(spot.est_market_cost for spot in spot_orders), 7)
        self.pnl = round(sum(spot.pnl for spot in spot_orders), 7)
        self.pnl_percent = round((self.pnl / self.total_cost) * 100, 2)
        self.positive = self.pnl >= 0
        self.last_updated = spot_orders[0].last_updated

    def __str__(self):
        return f"SpotView(total_cost={self.total_cost}, total_market_cost={self.total_market_cost}, pnl={self.pnl}, pnl_percent={self.pnl_percent})"