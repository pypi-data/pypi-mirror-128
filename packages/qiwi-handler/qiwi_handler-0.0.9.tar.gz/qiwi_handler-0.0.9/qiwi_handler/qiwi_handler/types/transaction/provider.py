from qiwi_handler.utils.methods import MakeDict

class Provider(MakeDict):
    def __init__(self,
                 id_: int = None,
                 short_name: str = None,
                 long_name: str = None,
                 logo_url: str = None,
                 description: str = None,
                 keys: str = None,
                 site_url: str = None
                 ):

        self.id = id_
        self.shortName = short_name
        self.longName = long_name
        self.logoUrl = logo_url
        self.description = description
        self.keys = keys
        self.siteUrl = site_url

