
class Commission:
    def __init__(self,
                 amount: int = None,
                 currency: int = None):

        self.amount = amount
        self.currency = currency

    def __str__(self):
        return str(self.__dict__)

