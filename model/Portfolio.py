class Portfolio:
    def __init__(self, id, name, logo):
        self.id = id
        self.name = name
        self.logo = logo

    def __str__(self):
        return f"Portfolio(id={self.id}, name={self.name}, logo={self.logo})"