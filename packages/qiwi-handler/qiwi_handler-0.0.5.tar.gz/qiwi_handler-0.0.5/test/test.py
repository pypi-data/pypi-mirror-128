from qiwi_handler import Client

QIWI_TOKEN = "d4c433ec3bfd1362a59a39fd7805643f"

client = Client(QIWI_TOKEN)


@client.check_pay(check_status=False, wallets=["380633760080"])
def func(pay):
    print("Do smth")


client.run()
