import aiohttp

from aiohttp.client_exceptions import ContentTypeError


class Request:
    main_url = "https://edge.qiwi.com/"

    def __init__(self, token: str):
        self.token = token

    async def do_get(self, *, url: str = None, params: dict = None, headers: dict = None):
        f""":raise exceptions.NotUrlWasSet:
        """

        if url is None:
            raise NotUrlWasSet("Please, check req")
        link = Request.main_url + url

        for i in params:
            par = params[i]
            if isinstance(par, bool):
                params[i] = str(par)


        exit_params = {
            i: params[i]
            for i in params
            if params[i]

        }

        async with aiohttp.ClientSession() as session:
            if headers is None:
                session.headers['Accept'] = 'application/json'
                session.headers['authorization'] = 'Bearer ' + self.token
            else:
                for header in headers:
                    try:
                        session.headers['Accept'] = 'application/json'
                        session.headers.add(header, headers[header])
                    except ContentTypeError:
                        raise InvalidToken("Check your token")
            params = exit_params
            r = await session.get(url=link, params=params)
            return await r.json()
