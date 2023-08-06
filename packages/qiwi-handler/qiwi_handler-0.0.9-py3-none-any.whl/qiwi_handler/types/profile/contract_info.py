from qiwi_handler.utils.methods import MakeDict


class ContractInfo(MakeDict):
    def __init__(self,
                 blocked: bool = None,
                 contract_id: int = None,
                 creation_date: str = None,
                 features: tuple = None,
                 identification_info: tuple = None):

        self.blocked = blocked
        self.contractId = contract_id
        self.creationDate = creation_date
        self.features = features
        self.identificationInfo = identification_info


