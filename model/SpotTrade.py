from decimal import Decimal


class SpotTrade:
    def __init__(self, id, coin_marketcap_id, symbol, buy_price, quantity, logo, portfolioId, updatePrice=False):
        self.id = id
        if coin_marketcap_id is not None:
            self.coin_marketcap_id =  int(coin_marketcap_id)
        else:
            self.coin_marketcap_id = None
        self.symbol = symbol
        self.buy_price = buy_price
        self.quantity = quantity
        self.logo = logo
        self.portfolioId = portfolioId
        self.updatePrice = updatePrice

    def __str__(self):
        return f"SpotTrade(coin_marketcap_id={self.coin_marketcap_id}, symbol={self.symbol}, buy_price={self.buy_price}, quantity={self.quantity}, logo={self.logo}, portfolioId={self.portfolioId})"

    def to_dict(self):
        return {
            'id': self.id,
            'cid': self.coin_marketcap_id,
            'symbol': self.symbol,
            'buyPrice': str(self.buy_price),
            'qty': str(self.quantity),
            'portfolioId': self.portfolioId,
            'updatePrice': self.updatePrice
        }


