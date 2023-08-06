import asyncio
from qiwi_handler.account_api import Methods


class Client(Methods):
    def __init__(self, token):
        self.token = token
        super().__init__(token)

    def get_token(self):
        return self.token

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._check_pay_handler())

    async def idle(self):
        await self._check_pay_handler()

