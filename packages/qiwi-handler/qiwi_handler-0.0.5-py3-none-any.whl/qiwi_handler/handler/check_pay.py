import datetime
import inspect
import asyncio

from qiwi_handler import loader

from qiwi_handler.handler import handler_check_pay

already_proc = []


async def already_proc_insert(id_):
    already_proc.append(id_)
    await asyncio.sleep(4)

def from_datetime_to_time(date):
    was = date.split("T")
    was = " ".join(was)
    was = was[:19]
    date_time_obj = datetime.datetime.strptime(was, '%Y-%m-%d %H:%M:%S')
    was = date_time_obj - datetime.datetime(1900, 1, 1)
    return was.total_seconds() + 3600



def now():
    today = datetime.datetime.today()
    dt = today - datetime.datetime(1900, 1, 1)
    return dt.total_seconds()

class CheckPayHandler:
    async def _check_pay_handler(self):

        '''message: str = None, wallets: list, amount: float = None,
        may_be_bigger = True, check_status = True'''

        params = {
            'rows': 5,
        }
        headers = {
            'authorization': f'Bearer {self.token}',
        }

        while True:
            for func, args in handler_check_pay:
                message, wallets, amount, may_be_bigger, check_status = args
                for wallet in wallets:
                    await asyncio.sleep(1 * 60 / 95)
                    url = f'payment-history/v2/persons/{wallet}/payments'
                    req = loader.Request(self.token)
                    json = await req.do_get(url=url, headers=headers, params=params)
                    histories = loader.convert_history(json)

                    for history in histories:
                        if history.data is None:
                            continue

                        sum = history.data.total
                        comment = history.data.comment
                        status = history.data.status
                        date = history.data.date
                        txn_id = history.data.txnId

                        if txn_id in already_proc:
                            continue

                        if message:
                            if message is not comment:
                                continue

                        if amount:
                            if may_be_bigger:
                                if amount > sum.amount:
                                    continue
                            elif amount != sum.amount:
                                continue

                        if check_status:
                            if status == "ERROR":
                                continue

                        if now() >= from_datetime_to_time(date) and (now() - 3) <= from_datetime_to_time(date):

                            if txn_id in already_proc:
                                return
                            if inspect.iscoroutinefunction(func):
                                await func(pay=history)
                            else:
                                func(pay=history)


                            loop = asyncio.get_event_loop()
                            loop.create_task(already_proc_insert(history.data.txnId))


