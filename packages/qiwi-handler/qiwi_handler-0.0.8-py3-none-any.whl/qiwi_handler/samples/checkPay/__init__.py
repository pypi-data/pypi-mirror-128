from qiwi_handler.handler.check_pay import handler_check_pay
from qiwi_handler.exceptions import TooMuchRequests, TooMuchRows

class CheckPay:

    def check_pay(self, *, message: str = None, wallets: list, amount: float = None,
                  may_be_bigger: bool = True, check_status: bool = True, operation: str = "ALL", updates_per_minute: int = 50,
                  rows_per_update: int = 5):
        def handler(func):
            if updates_per_minute >= 100 or updates_per_minute <= 0:
                raise TooMuchRequests("updates_per_minute per minute may be only less than 100 and bigger than 0!")

            if rows_per_update > 50 or rows_per_update <= 0:
                raise TooMuchRequests("rows_per_update may be only less than 51 and bigger than 0!")

            args = [func, [message, wallets, amount, may_be_bigger, check_status,
                           operation, updates_per_minute, rows_per_update]]
            handler_check_pay.append(args)

        return handler



