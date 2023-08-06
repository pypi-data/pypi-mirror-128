from qiwi_handler.utils.methods import MakeDict

class PinInfo(MakeDict):
    def __init__(self,
                 pin_used: bool = None):

        self.pinUsed = pin_used

