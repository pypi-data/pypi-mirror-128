from qiwi_handler.utils.methods import MakeDict
from qiwi_handler.types.transaction import Transaction

class History(MakeDict):
    def __init__(self, data: Transaction = None,
                 next_txn_id: int = None,
                 next_txn_date: str = None):

        self.data = data
        self.nextTxnId = next_txn_id
        self.nextTxnDate = next_txn_date


