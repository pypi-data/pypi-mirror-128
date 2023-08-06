#полная документация еще не вышла, но есть....

Эта штука работает на декораторе, который отлавливает транзакции кошелька.
Для запуска есть client.run(), и await client.idle() соответсвенно. Оба они являются ассинхронными, но run()
создает новый луп, и не нуждается в запуске с await

## Пример
>сlient.check_pay  принимает аргументы:\
> (* - обязательно)\

> `message: str (строгая проверка на содержание окна "Комментарий к переводу") `
> 
> `*wallets: list (список из номеров кошелька (телефона), с который идет парсинг) `
>
>`amount: float (строгая проверка на сумму, которая указана в total (с уч. комисии)), `
>
>`may_be_bigger: bool = True (превращает amount в не строгую проверку, и пропускает суммы выше)`
>
>`check_status: bool = True (проверка на успешность операции)`

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
