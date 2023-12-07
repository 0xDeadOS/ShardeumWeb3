import time
from web3 import Web3
from Constants.data import PRIVAT_KEY_ONE, PRIVAT_KEY_TWO

print("Start!")

web3 = Web3(Web3.HTTPProvider("https://sphinx.shardeum.org/"))

stop = input("Нажмите Enter для продолжения...")

if web3.is_connected():
    print("Подключение к shardeum узлу успешно!\n"
        f"Количество блоков в блокчейне: {web3.eth.block_number}\n"
        f"Цена газа: {web3.eth.gas_price}\n"
        f"Номер текущего блока: {web3.eth.block_number}\n"
        f"Подключен к цепи: {web3.eth.chain_id}\n"
        f"{web3.eth.get_transaction_count(web3.to_checksum_address('0x4F65FCb2dFeAC38E4f6d03eb0AFD6785b03C11c5'))}")
else:
    print("Не удалось подключиться к shardeum узлу.")

stop = input("Нажмите Enter для продолжения...")


chainIdConnected = web3.eth.chain_id

def get_balance_ether(*, web3: Web3, address: str) -> str:
    balance = Web3.from_wei(web3.eth.get_balance(Web3.to_checksum_address(address)), 'ether') 
    return str(balance)

    
def build_txn(*, web3: Web3, from_address: str, to_address: str, amount: float) -> dict[str, int | str]:
    pass


userWalletOne = (web3.eth.account.from_key(PRIVAT_KEY_ONE)).address
userWalletTwo = (web3.eth.account.from_key(PRIVAT_KEY_TWO)).address
print("User Wallet Address one: " + userWalletOne)
print("User Wallet Address one: " + userWalletTwo)

oneEtherInWeiSHM = "1000000000000000000"
print("weiMsgValueToSend: " + oneEtherInWeiSHM)

info1 =  web3.eth.get_balance(userWalletOne)
print("User Balance [Shardeum SHM]" )
print(web3.from_wei(info1, 'ether'))

info2 =  web3.eth.get_balance(userWalletTwo)
print("Receiver Balance [Shardeum SHM]" )
print(web3.from_wei(info2, "ether"))

transferTx = {
    'chainId' : chainIdConnected,
    'nonce':  web3.eth.get_transaction_count(userWalletOne),
    'to': userWalletTwo, #WORKS WITH REGULAR WALLETS BUT CANNOT SEND TO CONTRACT FOR SOME REASON?
    'gas': 2100000, #WORKS WITH 1000000. If not try : Remix > deploy and run transactions
    'gasPrice': web3.to_wei('36', 'gwei'), # https://etherscan.io/gastracker
    'value': int(oneEtherInWeiSHM),
    'accessList' :
                [
                    {
                        "address" : userWalletTwo,
                        "storageKeys": []
                    }
                ]
}

signed_tx = web3.eth.account.sign_transaction(transferTx, PRIVAT_KEY_ONE)
tx_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_tx.rawTransaction))
print("TX HASH: " + tx_hash)

time.sleep(15)

receipt = web3.eth.get_transaction_receipt(tx_hash)
print("TX RECEIPT: " + str(receipt) )