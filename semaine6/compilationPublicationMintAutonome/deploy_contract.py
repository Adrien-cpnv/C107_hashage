from web3 import Web3
import json
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv('../../key.env')
private_key = os.getenv('PRIVATE_KEY')
deployer_address = "0x7967c1641F06A2f5706db0f542FEa3D4eae1DBBF"

# Connexion au nœud Ethereum
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"

# Charger l'ABI et le bytecode du contrat
with open('VoleryAdrienNFT.abi', 'r') as abi_file:
    contract_abi = json.load(abi_file)
with open('VoleryAdrienNFT.bin', 'r') as bin_file:
    contract_bytecode = bin_file.read().strip()

deployer_address = w3.to_checksum_address(deployer_address)
nonce = w3.eth.get_transaction_count(deployer_address)

# Préparer la transaction de déploiement
SimpleMintContract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
construct_txn = SimpleMintContract.constructor(deployer_address).build_transaction({
    'from': deployer_address,
    'nonce': nonce,
    'gas': 3000000,
    'gasPrice': w3.to_wei('10', 'gwei'),
    'chainId': 32383
})

# Signer et envoyer la transaction
signed = w3.eth.account.sign_transaction(construct_txn, private_key)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
print(f"Déploiement envoyé, hash: {tx_hash.hex()}")

# Attendre la confirmation
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Contrat déployé à l'adresse : {tx_receipt.contractAddress}")