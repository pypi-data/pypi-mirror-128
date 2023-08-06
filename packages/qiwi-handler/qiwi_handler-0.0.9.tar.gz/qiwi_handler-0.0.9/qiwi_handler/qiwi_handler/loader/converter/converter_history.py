from qiwi_handler.types import history
from qiwi_handler.types import Sum, Commission, Total, Provider, Source, Extras,Transaction


def convert_history(json) -> list[history.History]:
    if json is None:
        return [history.History()]
    if "errorCode" in json:
        try:
            json["errorCode"]
        except KeyError:
            raise

    try:
        data = json["data"]
        next_txn_id = json["nextTxnId"]
        next_txn_date = json["nextTxnDate"]
    except KeyError as e:
        if json["errorCode"] == "request.blocked":
            return [history.History()]
        raise e

    all_dat = []
    for dat in data:
        txn_id = dat["txnId"]
        person_id = dat["personId"]
        date = dat["date"]
        error_code = dat["errorCode"]
        error = dat["error"]
        type_ = dat["type"]
        status = dat["status"]
        status_text = dat["statusText"]
        trm_txn_id = dat["trmTxnId"]
        account = dat["account"]
        sum = dat["sum"]
        sum_obj = Sum(
            sum["amount"],
            sum["currency"]
        )
        commission = dat["commission"]
        commission_obj = Commission(
            commission["amount"],
            commission["currency"]
        )
        total = dat["total"]
        total_obj = Total(
            total["amount"],
            total["currency"]
        )
        provider = dat["provider"]
        provider_obj = Provider(
            provider["id"],
            provider["shortName"],
            provider["longName"],
            provider["logoUrl"],
            provider["description"],
            provider["keys"],
            provider["siteUrl"]
        )
        source = Source(
            dat["source"]
        )
        comment = dat["comment"]
        currency_rate = dat["currencyRate"]
        extras = Extras(

        )
        cheque_ready = dat["features"]["chequeReady"]
        bank_document_available = dat["features"]["bankDocumentAvailable"]
        repeat_payment_enabled = dat["features"]["repeatPaymentEnabled"]
        favorite_payment_enabled = dat["features"]["favoritePaymentEnabled"]
        regular_payment_enabled = dat["features"]["regularPaymentEnabled"]

        data_obj = Transaction(
            txn_id,
            person_id,
            date,
            error_code,
            error,
            type_,
            status,
            status_text,
            trm_txn_id,
            account,
            sum_obj,
            commission_obj,
            total_obj,
            provider_obj,
            source,
            comment,
            currency_rate,
            extras,
            cheque_ready,
            bank_document_available,
            repeat_payment_enabled,
            favorite_payment_enabled,
            regular_payment_enabled

        )
        all_dat.append(history.History(data_obj, next_txn_id, next_txn_date))

    else:
        all_dat.append(history.History())

    return all_dat
