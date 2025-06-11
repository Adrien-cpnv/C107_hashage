import json
import time
from web3 import Web3
from dotenv import load_dotenv
import os

# Charger la clé privée
load_dotenv('../key.env')
private_key = os.getenv('PRIVATE_KEY')
if private_key is None:
    print("Clé privée manquante.")
    exit()

# Connexion au nœud
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))
assert w3.is_connected(), "Connexion échouée"

# Charger ABI
with open("tirelire.abi") as f:
    abi = json.load(f)


contract_address = "0x4c397Fc5df8DcEfdE2735942Aa0d0a6378103885"  # A remplacé par l'adresse du contrat déployé

# Préparer le contrat
tirelire = w3.eth.contract(address=contract_address, abi=abi)
account = w3.eth.account.from_key(private_key)
sender = account.address

# Dépôt de 1 ETH avec date de retrait dans 10 secondes
date_retrait = int(time.time()) + 10
nonce = w3.eth.get_transaction_count(sender)
tx = tirelire.functions.deposer(date_retrait).build_transaction({
    "from": sender,
    "value": w3.to_wei(1, "ether"),
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "chainId": 32383
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Dépôt envoyé, hash:", tx_hash.hex())
w3.eth.wait_for_transaction_receipt(tx_hash)

# Tentative de retrait avant la date (doit échouer)
try:
    nonce = w3.eth.get_transaction_count(sender)
    tx = tirelire.functions.retirer().build_transaction({
        "from": sender,
        "nonce": nonce,
        "gas": 200000,
        "gasPrice": w3.to_wei("10", "gwei"),
        "chainId": 32383
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Retrait AVANT la date : ERREUR, le retrait aurait dû échouer.")
except Exception as e:
    print("Retrait AVANT la date : échec attendu.")

# Attent la date de retrait
print("Attente de la date de retrait...")
time.sleep(12)

# Retrait après la date (doit réussir)
nonce = w3.eth.get_transaction_count(sender)
tx = tirelire.functions.retirer().build_transaction({
    "from": sender,
    "nonce": nonce,
    "gas": 200000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "chainId": 32383
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Retrait APRÈS la date : succès, tx hash:", tx_hash.hex())