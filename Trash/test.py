from typing import Optional
from hexbytes import HexBytes
from web3 import Web3
from Constants.data import PRIVAT_KEY_ONE, PRIVAT_KEY_TWO

print("Start!")

web3 = Web3(Web3.HTTPProvider("https://sphinx.shardeum.org/"))


# 1. функция для build'a транзакции
def build_txn(
  *,
  web3: Web3,
  from_address: str,  # checksum адрес
  to_address: str,  # checksum адрес
  amount: float,  # например, 0.1 BNB
) -> dict[str, int | str]:
  	# цена газа
    gas_price = web3.eth.gas_price
    
    # количество газа
    gas = 2_000_000  # ставим побольше

    # число подтвержденных транзакций отправителя
    nonce = web3.eth.getTransactionCount(from_address)

    txn = {
      'chainId': web3.eth.chain_id,
      'from': from_address,
      'to': to_address,
      'value': int(Web3.toWei(amount, 'ether')),
      'nonce': nonce, 
      'gasPrice': gas_price,
      'gas': gas,
    }
    return txn


transaction = build_txn(
  web3=web3,
  from_address=my_address,
  to_address=to_address,
  amount=0.1,
)


# 2. Подписываем транзакцию с приватным ключом
signed_txn = web3.eth.account.sign_transaction(transaction, PRIVAT_KEY_ONE)


# 3. Отправка транзакции
txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Получаем хэш транзакции
# Можно посмотреть статус тут https://testnet.bscscan.com/
print(txn_hash.hex())