from qiwi_handler.types.profile.auth_info import AuthInfo
from qiwi_handler.types.profile.contract_info import ContractInfo
from qiwi_handler.types.profile.user_info import UserInfo


class GetCurrent():
    def __init__(self,
                 auth_info: AuthInfo = None,
                 contract_info: ContractInfo = None,
                 user_info: UserInfo = None):

        self.authInfo = auth_info
        self.contractInfo = contract_info
        self.userInfo = user_info

