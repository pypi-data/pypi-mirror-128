
from qiwi_handler.types.transaction import Transaction

class History:
    def __init__(self, data: Transaction = None,
                 next_txn_id: int = None,
                 next_txn_date: str = None):

        self.data = data
        self.nextTxnId = next_txn_id
        self.nextTxnDate = next_txn_date

    def __str__(self):
        data = str(self.data)
        return str({"data": data, "nextTxnId": self.nextTxnId, "nextTxnDate": self.nextTxnDate})



