import json
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

# Charger ABI et bytecode
with open("tirelire.abi") as f:
    abi = json.load(f)
with open("tirelire.bin") as f:
    bytecode = f.read().strip()

# Adresse du déployeur
account = w3.eth.account.from_key(private_key)
sender = account.address

# Préparer la transaction de déploiement
Tirelire = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(sender)
tx = Tirelire.constructor().build_transaction({
    "from": sender,
    "nonce": nonce,
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "chainId": 32383
})

# Signer et envoyer
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
print("Déploiement envoyé, hash:", tx_hash.hex())

# Attendre la confirmation
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contrat déployé à l'adresse:", receipt.contractAddress)