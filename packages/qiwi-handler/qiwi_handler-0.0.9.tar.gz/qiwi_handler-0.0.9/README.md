#  полная документация еще не вышла, но есть....

Эта штука работает на декораторе, который отлавливает транзакции кошелька.
Для запуска есть client.run(), и await client.idle() соответсвенно. Оба они являются ассинхронными, но run()
создает новый луп, и не нуждается в запуске с await


##пример:

```
from client import Client
from objects.account_api.types.history import History
client = Client(TOKEN)

@client.check_pay(wallets=[PHONE NUMBER], check_status=False, 
                    amount=5, may_be_bigger=True)
def func(pay: History):
    print(pay)

client.run()
```

# типы:
> основные типы:
> History, UserInfo
> 
> импорт:
> 
> from qiwi_handler.types import History, UserInfo
> 
## Если вам IDE не помогает в том, что может возвращать функция, или вам надо полностью изучить переменную:
### https://developer.qiwi.com/ru/qiwi-wallet-personal/index.html#restrictions
## History (История платежей)

> ### (* - обязательно)
> 
> ### @client.check_pay() - выше показанный обработчик - возвращает History
>
> > `wallet: str` - (номер кошелька(телефона))\
> `rows: int = 5` - (Количество последних транзакций),\
> `operation: str = None` - (Тип операций в отчете, для отбора (ALL, IN, OUT, QIWI_CARD)), \
> `sources: list = None` - (Список источников платежа, для фильтра (QW_RUB, QW_USD, QW_EUR, CARD, MK)),\
> `start_date: str = None` - Начальная дата поиска платежей (DateTime URL-encoded), \
> `end_date: str = None` - Конечная дата поиска платежей (DateTime URL-encoded),\
> `next_txn_date: str = None` - Дата транзакции для начала отчета(DateTime URL-encoded), \
> `next_txn_id: int = None` - Номер транзакции для начала отчета

>  ### client.history(wallet: str) - возвращает array[History]
>
> > `message: str` (строгая проверка на содержание окна "Комментарий к переводу"),\
> `* wallets: list` (список из номеров кошелька (телефона), с который идет парсинг), \
>`amount: float` (строгая проверка на сумму, которая указана в total (с уч. комисии)), \
>`may_be_bigger: bool = True` (превращает amount в не строгую проверку, и пропускает суммы выше), \
>`check_status: bool = True` (проверка на успешность операции),\
> `operation: str = "ALL"` (Тип операций в отчете, для отбора (ALL, IN, OUT, QIWI_CARD)),\
> `updates_per_minute: int = 50` (ВАЖНО! болше 99 в минуту вам не даст поставить сисетма, т.к. если значение
> будет более 100 - ваш апи кей заблокирут на 5 минут. Если вам не достаточно скорости - используйте большое значение
> в rows_per_update), \
> `rows_per_update: int = 5` (Количество последних транзакций, которые передаются нобработку хендлеру,
> больше 50 поставить не выйдет) 

## UserInfo (Профиль пользователя)
> ### (* - обязательно)
> 
> ### await client.get_current() - возарвщает UserInfo
> 
> >`auth_info_enabled: bool = True` - (Логический признак выгрузки настроек авторизации), \
> `contract_info_enabled: bool = True` - (Логический признак выгрузки данных о вашем QIWI кошельке), \
> `user_info_enabled: bool = True` - (Логический признак выгрузки прочих пользовательских данных.)