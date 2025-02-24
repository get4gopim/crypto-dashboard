class SpotView:
    def __init__(self, spot_orders):
        self.spot_orders = sorted(spot_orders, key=lambda x: x.pnl, reverse=True)
        #self.spot_orders = self.get_top5(spot_orders)
        self.total_cost = round(sum(spot.est_cost for spot in spot_orders), 7)
        self.total_market_cost = round(sum(spot.est_market_cost for spot in spot_orders), 7)
        self.pnl = round(sum(spot.pnl for spot in spot_orders), 7)
        self.pnl_percent = round((self.pnl / self.total_cost) * 100, 2)
        self.positive = self.pnl >= 0
        self.last_updated = spot_orders[0].last_updated

    def __str__(self):
        return f"SpotView(total_cost={self.total_cost}, total_market_cost={self.total_market_cost}, pnl={self.pnl}, pnl_percent={self.pnl_percent})"

    def get_top5(self, spot_orders):
        # Sort the list by the 'score' attribute in descending order
        sorted_list = sorted(spot_orders, key=lambda x: x.pnl, reverse=True)
        # Get the top 5 people with the highest scores
        return sorted_list[:5]

    def to_dict(self):
        """Convert the object to a dictionary."""
        spot_order_dicts = [spot_order.to_dict() for spot_order in self.spot_orders]
        return {"total_cost": self.total_cost, "total_market_cost": self.total_market_cost, "pnl": self.pnl, "pnl_percent": self.pnl_percent, "positive": self.positive, "last_updated": self.last_updated, "spot_orders": spot_order_dicts}