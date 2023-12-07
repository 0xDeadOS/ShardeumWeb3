import time
from web3 import Web3
from Constants.data import PRIVAT_KEY_ONE, PRIVAT_KEY_TWO

print("Start script\n"
      "-----------------")
web3 = Web3(Web3.HTTPProvider("https://sphinx.shardeum.org/"))
chainIdConnected = web3.eth.chain_id
if web3.is_connected():
    print("Подключение к shardeum узлу успешно!\n")
    # f"ID цепи: {chainIdConnected}")
else:
    print("Не удалось подключиться к shardeum узлу.")

userWalletOne = (web3.eth.account.from_key(PRIVAT_KEY_ONE)).address
userWalletTwo = (web3.eth.account.from_key(PRIVAT_KEY_TWO)).address

def build_txn(*, web3: Web3, from_address: str, to_address: str, amount: float) -> dict[str, int | str]:
    transferTx = {
    'chainId' : chainIdConnected,
    'nonce':  web3.eth.get_transaction_count(from_address),
    'to': to_address,
    'gas': 2_100_000,
    'gasPrice': web3.eth.gas_price,
    'value': int(web3.to_wei(amount, 'ether')),
    'accessList' :[{"address" : to_address, "storageKeys": []}]
    }
    return transferTx

try:
    transaction = build_txn(web3=web3, from_address=userWalletOne, to_address=userWalletTwo, amount=0.01)
    signed_tx = web3.eth.account.sign_transaction(transaction, PRIVAT_KEY_ONE)
    tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_tx.rawTransaction))
    print(tx_hash) 
except Exception as e:
    print(e)
    print("Не удалось отправить транзакцию.")