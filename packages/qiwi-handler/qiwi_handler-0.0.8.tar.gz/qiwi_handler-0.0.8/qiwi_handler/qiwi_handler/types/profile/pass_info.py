from qiwi_handler.utils.methods import MakeDict

class PassInfo(MakeDict):
    def __init__(self,
                 password_used: bool = None,
                 last_pass_change: str = None,
                 next_pass_change: str = None,
                 ):

        self.password_used = password_used
        self.lastPassChange = last_pass_change
        self.nextPassChange = next_pass_change
