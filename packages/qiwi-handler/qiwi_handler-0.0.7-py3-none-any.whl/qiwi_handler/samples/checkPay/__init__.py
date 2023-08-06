from qiwi_handler.handler.check_pay import handler_check_pay


class CheckPay:

    def check_pay(self, *, message: str = None, wallets: list, amount: float = None,
                  may_be_bigger=True, check_status=True):
        def handler(func):
            args = [func, [message, wallets, amount, may_be_bigger, check_status]]
            handler_check_pay.append(args)

        return handler



