from qiwi_handler.utils.methods import MakeDict


class MobilePinInfo(MakeDict):
    def __init__(self,
                 mobile_pin_used: bool = None,
                 last_mobile_pin_change: bool = None,
                 next_mobile_pin_change: str = None,
                 ):

        self.mobilePinUsed = mobile_pin_used
        self.lastMobilePinChange = last_mobile_pin_change
        self.nextMobilePinChange = next_mobile_pin_change

