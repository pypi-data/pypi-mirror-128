from qiwi_handler import loader
from qiwi_handler.types import history


class History:
    def __init__(self, token):
        self.token = token

    async def history(self, *, wallet: str, rows: int = 5,
                      operation: str = None, sources: list = None,
                      start_date: str = None, end_date: str = None,
                      next_txn_date: str = None, next_txn_id: int = None) -> [history.History]:
        """wallet - номер вашего кошелька без знака '+'\n
        rows - Число платежей в ответе, для разбивки отчета на страницы. Целое число от 1 до 50. Запрос возвращает указа
        нное число платежей в обратном хронологическом порядке, начиная от текущей даты или даты в параметре startDate.
        Обязательный параметр\n
        operation - Тип операций в отчете, для отбора. Допустимые значения:\n
        ALL - все операции,
        IN - только пополнения,
        OUT - только платежи,
        QIWI_CARD - только платежи по картам QIWI (QVC, QVP).
        По умолчанию ALL
        sources - Список источников платежа, для фильтра. Каждый источник нумеруется, начиная с нуля (sources[0],
        sources[1] и т.д.). Допустимые значения:
        QW_RUB - рублевый счет кошелька,
        QW_USD - счет кошелька в долларах,
        QW_EUR - счет кошелька в евро,
        CARD - привязанные и непривязанные к кошельку банковские карты,
        MK - счет мобильного оператора. Если не указан, учитываются все источники\n

        start_date - (DateTime URL-encoded) Начальная дата поиска платежей. Используется только вместе с endDate.
        Максимальный допустимый интервал между startDate и endDate - 90 календарных дней. По умолчанию, равна суточному
        сдвигу от текущей даты
        по московскому времени.
        Дату можно указать в любой временной зоне TZD (формат ГГГГ-ММ-ДД'T'чч:мм:ссTZD), однако она должна совпадать с
        временнойзоной в параметре endDate. Обозначение временной зоны TZD: +чч:мм или -чч:мм (временной сдвиг от GMT)\n

        end_date - (DateTime URL-encoded) Конечная дата поиска платежей. Используется только вместе со start_date.
        Максимальный допустимый интервал между startDate и endDate - 90 календарных дней. По умолчанию, равна текущим
        дате/времени по московскому времени. Дату можно указать в любой временной зоне TZD
        (формат ГГГГ-ММ-ДД'T'чч:мм:ссTZD), однако она должна совпадать с временной зоной в параметре startDate.
        Обозначение временной зоны TZD: +чч:мм или -чч:мм (временной сдвиг от GMT).\n

        next_txn_date - (DateTime URL-encoded) Дата транзакции для начала отчета (должна быть равна параметру
        nextTxnDate в предыдущем списке). Используется для продолжения списка, разбитого на страницы.
        Используется только вместе с nextTxnId\n

        next_txn_id - Номер транзакции для начала отчета (должен быть равен параметру nextTxnId в предыдущем списке).
        Используется для продолжения списка, разбитого на страницы. Используется только вместе с nextTxnDate\n
        """
        print(wallet)
        url = f'payment-history/v2/persons/{wallet}/payments'
        headers = {
            'authorization': f'Bearer {self.token}',
        }

        #rows: int, *, operation: str = None, sources: list = None,
        #start_date: str = None, end_date: str = None, next_txn_date: str = None, next_txn_id: int = None):

        params = {
            'rows': rows,
            'operation': operation,
            'sources': sources,
            'startDate': start_date,
            'endDate': end_date,
            'nextTxnDate': next_txn_date,
            'nextTxnId': next_txn_id
        }

        req = loader.Request(self.token)
        json = await req.do_get(url=url, headers=headers, params=params)
        return loader.convert_history(json)

