from qiwi_handler.types import ContractInfo, MobilePinInfo, PassInfo, PinInfo, AuthInfo, UserInfo
from qiwi_handler.types.profile import GetCurrent
def convert_profile(json):

    if json["contractInfo"]:
        contract_info = json["contractInfo"]
        blocked = contract_info["blocked"]
        contract_id = contract_info["contractId"]
        creation_date = contract_info["creationDate"]
        features = contract_info["features"]
        identification_info = contract_info["identificationInfo"]
        contract_info_obj = ContractInfo(blocked, contract_id, creation_date, features, identification_info)
    else:
        contract_info_obj = ContractInfo()

    if json["authInfo"]:
        auth_info = json["authInfo"]
        person_id = auth_info["personId"]
        registration_date = auth_info["registrationDate"]
        bound_email = auth_info["boundEmail"]
        ip = auth_info["ip"]
        last_login_date = auth_info["lastLoginDate"]
        pass_info = auth_info["passInfo"]
        pin_info = auth_info["pinInfo"]
        mobile_pin_info = auth_info["mobilePinInfo"]


        mobile_pin_info_obj = MobilePinInfo(
            mobile_pin_info["mobilePinUsed"],
            mobile_pin_info["lastMobilePinChange"],
            mobile_pin_info["nextMobilePinChange"]
        )

        pass_info_obj = PassInfo(
            pass_info["passwordUsed"],
            pass_info["lastPassChange"],
            pass_info["nextPassChange"]
        )

        pin_info_obj = PinInfo(
            pin_info["pinUsed"]
        )



        auth_info_obj = AuthInfo(person_id, registration_date, bound_email, ip, last_login_date,
                                 mobile_pin_info_obj, pass_info_obj, pin_info_obj)
    else:
        auth_info_obj = AuthInfo()

    if json["userInfo"]:
        user_info = json["user_Info"]
        default_pay_currency = user_info["defaultPayCurrency"]
        default_pay_source = user_info["defaultPaySource"]
        email = user_info["email"]
        first_txn_id = user_info["firstTxnId"]
        language = user_info["language"]
        operator = user_info["operator"]
        phone_hash = user_info["phoneHash"]
        promo_enabled = user_info["promoEnabled"]
        user_info_obj = UserInfo(
            default_pay_currency,
            default_pay_source,
            email,
            first_txn_id,
            language,
            operator,
            phone_hash,
            promo_enabled
        )
    else:
        user_info_obj = UserInfo

    return GetCurrent(auth_info_obj, contract_info_obj, user_info_obj)






