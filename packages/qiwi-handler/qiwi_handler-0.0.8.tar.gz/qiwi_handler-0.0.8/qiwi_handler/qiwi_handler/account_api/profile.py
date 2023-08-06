from qiwi_handler import loader


class User:
    def __init__(self, token):
        self.token = token

    async def get_current(self,
                          auth_info_enabled: bool = True,
                          contract_info_enabled: bool = True,
                          user_info_enabled: bool = True,
                          ):
        url = 'person-profile/v1/profile/current?authInfoEnabled=true'
        '&contractInfoEnabled=true&userInfoEnabled=true'

        params = {
            "authInfoEnabled": auth_info_enabled,
            "contractInfoEnabled": contract_info_enabled,
            "userInfoEnabled": user_info_enabled
        }
        for i in params:
            par = params[i]
            if isinstance(par, bool):
                params[i] = str(par)

        req = loader.Request(self.token)
        json = await req.do_get(url=url, params=params)
        return loader.convert_profile(json)

