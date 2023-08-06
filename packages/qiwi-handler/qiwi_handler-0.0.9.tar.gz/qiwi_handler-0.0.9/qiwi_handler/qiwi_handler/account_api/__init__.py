from qiwi_handler.account_api.profile import User
from qiwi_handler.account_api.history import History
from qiwi_handler.handler.check_pay import CheckPayHandler

from qiwi_handler.samples.checkPay import CheckPay


"""зарегиструруйте ключ на https://qiwi.com/api
Получите токен, чтобы пользоваться API

С помощью токена вы сможете:
Получать информацию о кошельке (статус, дата создания и прочее)
Получать баланс кошелька
Просматривать историю платежей
Проводить платежи без SMS
Управлять виртуальными картами"""


class Methods(User, History, CheckPayHandler, CheckPay):
    pass
