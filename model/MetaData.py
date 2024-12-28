class MetaData:
    def __init__(self, cid, name, symbol, category, description, logo, platform_id, platform_name):
        self.cid = cid
        self.name = name
        self.symbol = symbol
        self.category = category
        self.description = description
        self.logo = logo
        self.platform_id = platform_id
        self.platform_name = platform_name
        self.link = str(f"/meta_data?cid={self.platform_id}")

    def __str__(self):
        return f"MetaData(cid={self.cid}, name={self.name}, symbol={self.symbol}, category={self.category}, platform_id={self.platform_id}, platform_name={self.platform_name})"