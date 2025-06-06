from web3 import Web3
import json
from dotenv import load_dotenv
import os



# Load environment variables from key.env
load_dotenv('../key.env')

# Retrieve the private key from the environment variable
private_key = os.getenv('PRIVATE_KEY')


# Connexion au nœud Ethereum
w3 = Web3(Web3.HTTPProvider("http://10.229.43.182:8545"))  # Remplacez par l'URL de votre nœud
assert w3.is_connected(), "Échec de la connexion au nœud Ethereum"

URI = "https://bronze-petite-antelope-488.mypinata.cloud/ipfs/bafkreigra4k4ekn5qby4t6u7larwfckxkemcnj44qfilknpdi6dmglnkmy"

# Adresse et ABI du contrat déployé
contract_address = "0xCEcF361541E38dD0091525CcF86B4131104E5E0F"
deployer_address = "0x7967c1641F06A2f5706db0f542FEa3D4eae1DBBF"
recipient_address = deployer_address

sender_address = w3.to_checksum_address(deployer_address)


# Charger l'ABI du contrat
with open("SimpleMintContract.abi", "r") as abi_file:
    contract_abi = json.load(abi_file)

# Charger le contrat
nft_contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Étape 1 : Mint du token
nonce = w3.eth.get_transaction_count(sender_address)
valueEth = 0.05
mint_txn = nft_contract.functions.mint(URI).build_transaction({
    "chainId": 32383,  # ID de votre blockchain privée ou testnet
    "gas": 2000000,
    "gasPrice": w3.to_wei("10", "gwei"),
    "value": w3.to_wei(valueEth, "ether"),  # Prix du mint défini dans le contrat
    "nonce": nonce
})

signed_mint_txn = w3.eth.account.sign_transaction(mint_txn, private_key)

try:
    # Send the signed transaction
    mint_tx_hash = w3.eth.send_raw_transaction(signed_mint_txn.raw_transaction)
    print(f"Transaction de mint envoyée : {mint_tx_hash.hex()}")

    # Wait for confirmation
    mint_receipt = w3.eth.wait_for_transaction_receipt(mint_tx_hash)
    print(f"Transaction de mint confirmée dans le bloc {mint_receipt.blockNumber}")
except Exception as e:
    print(f"Une erreur est survenue : {str(e)}")

# Récupérer le tokenId (assume que c'est totalSupply après mint)
token_id = nft_contract.functions.totalSupply().call()
print(f"Token ID minté (c'est totalSupply) : {token_id}")

