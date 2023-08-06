

class UserInfo:
    def __init__(self,
                 default_pay_currency: tuple = None,
                 default_pay_source: int = None,
                 email: str = None,
                 first_txn_id: int = None,
                 language: str = None,
                 operator: str = None,
                 phone_hash: str = None,
                 promo_enabled: str = None):

        self.defaultPayCurrency = default_pay_currency
        self.defaultPaySource =default_pay_source
        self.email = email
        self.firstTxnId = first_txn_id
        self.language = language
        self.operator = operator
        self.phoneHash = phone_hash
        self.promoEnabled = promo_enabled

    def __str__(self):
        return str(self.__dict__)
