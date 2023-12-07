import time
from web3 import Web3
from Constants.data import PRIVAT_KEY_ONE, PRIVAT_KEY_TWO

print("Start script\n"
      "-----------------")
web3 = Web3(Web3.HTTPProvider("https://sphinx.shardeum.org/")) # подключение к shardeum узлу
chainIdConnected = web3.eth.chain_id # получение цепи из shardeum узла
if web3.is_connected(): 
    print("Подключение к shardeum узлу успешно!\n")
    # f"ID цепи: {chainIdConnected}")
else:
    print("Не удалось подключиться к shardeum узлу.")

userWalletOne = (web3.eth.account.from_key(PRIVAT_KEY_ONE)).address
userWalletTwo = (web3.eth.account.from_key(PRIVAT_KEY_TWO)).address

def build_txn(*, web3: Web3, from_address: str, to_address: str, amount: float) -> dict[str, int | str]:
    transferTx = {
    'chainId' : chainIdConnected, # цепа из shardeum узла
    'nonce':  web3.eth.get_transaction_count(from_address), # число подтвержденных транзакций отправителя
    'to': to_address, # адрес получателя
    'gas': 2_100_000, # количество газа
    'gasPrice': web3.eth.gas_price, # цена газа
    'value': int(web3.to_wei(amount, 'ether')), # количество денег для перевода
    'accessList' :[{"address" : to_address, "storageKeys": []}] # для того чтобы отправить транзакцию с ключом хранилища адреса получателя
    }
    return transferTx

try:
    transaction = build_txn(web3=web3, from_address=userWalletOne, to_address=userWalletTwo, amount=0.01) # создание транзакции для перевода денег
    signed_tx = web3.eth.account.sign_transaction(transaction, PRIVAT_KEY_ONE) # подпись транзакции с приватным ключом
    tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_tx.rawTransaction)) # отправка транзакции
    print(tx_hash) 
except Exception as e:
    print(e)
    print("Не удалось отправить транзакцию.")