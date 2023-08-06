from qiwi_handler.types.transaction.sum import Sum
from qiwi_handler.types.transaction.commission import Commission
from qiwi_handler.types.transaction.total import Total
from qiwi_handler.types.transaction.provider import Provider
from qiwi_handler.types.transaction.source import Source
from qiwi_handler.types.transaction.extras import Extras
from qiwi_handler.utils.methods import MakeDict


class Transaction(MakeDict):
    def __init__(self,
                 txn_id: int = None,
                 person_id: int = None,
                 date: int = None,
                 error_code: int = None,
                 error: str = None,
                 type_: str = None,
                 status: str = None,
                 status_text: str = None,
                 trm_txn_id: str = None,
                 account: str = None,
                 sum: Sum = Sum(),
                 commission: Commission = Commission(),
                 total: Total = Total(),
                 provider: Provider = Provider(),
                 source: Source = Source(),
                 comment: str = None,
                 currency_rate: int = None,
                 extras: Extras = Extras(),
                 cheque_ready: bool = False,
                 bank_document_available: bool = False,
                 repeat_payment_enabled: bool = False,
                 favorite_payment_enabled: bool = False,
                 regular_payment_enabled: bool = False):

        self.txnId = txn_id
        self.personId = person_id
        self.date = date
        self.errorCode = error_code
        self.error = error
        self.type = type_
        self.status = status
        self.statusText = status_text
        self.trmTxnId = trm_txn_id
        self.account = account
        self.sum = sum
        self.commission = commission
        self.total = total
        self.provider = provider
        self.source = source
        self.comment = comment
        self.currencyRate = currency_rate
        self.extras = extras
        self.chequeReady = cheque_ready
        self.bankDocumentAvailable = bank_document_available
        self.repeatPaymentEnabled = repeat_payment_enabled
        self.favoritePaymentEnabled = favorite_payment_enabled
        self.regularPaymentEnabled = regular_payment_enabled





