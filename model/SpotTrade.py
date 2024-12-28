class SpotTrade:
    def __init__(self, id, coin_marketcap_id, symbol, buy_price, quantity, logo):
        self.id = id
        self.coin_marketcap_id = int(coin_marketcap_id)
        self.symbol = symbol
        self.buy_price = buy_price
        self.quantity = quantity
        self.logo = logo

    def __str__(self):
        return f"SpotTrade(coin_marketcap_id={self.coin_marketcap_id}, symbol={self.symbol}, buy_price={self.buy_price}, quantity={self.quantity}, logo={self.logo})"




