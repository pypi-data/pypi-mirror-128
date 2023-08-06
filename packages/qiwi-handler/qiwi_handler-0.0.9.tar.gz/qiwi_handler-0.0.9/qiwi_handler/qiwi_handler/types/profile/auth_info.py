from qiwi_handler.types.profile.mobile_pin_info import MobilePinInfo
from qiwi_handler.types.profile.pass_info import PassInfo
from qiwi_handler.types.profile.pin_info import PinInfo
from qiwi_handler.utils.methods import MakeDict


class AuthInfo(MakeDict):
    """Запрос возвращает информацию о вашем профиле - наборе пользовательских данных и настроек вашего QIWI кошелька."""
    def __init__(self,
                 person_id: int = None,
                 registration_date: str = None,
                 bound_email: str = None,
                 ip: str = None,
                 last_login_date: str = None,
                 mobile_pin_info: MobilePinInfo = MobilePinInfo(),
                 pass_info: PassInfo = PassInfo(),
                 pin_info: PinInfo = PinInfo()
                 ):

        self.personId = person_id
        self.registrationDate = registration_date
        self.boundEmail = bound_email
        self.ip = ip
        self.lastLoginDate = last_login_date
        self.mobilePinInfo = mobile_pin_info
        self.passInfo = pass_info
        self.pinInfo = pin_info


