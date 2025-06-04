from dotenv import load_dotenv
import os
import json
from web3 import Web3, Account

# Load environment variables from key.env
load_dotenv('../key.env')

# Retrieve the private key from the environment variable
private_key = os.getenv('PRIVATE_KEY')

if private_key is None:
    print("La clé privée n'a pas été trouvée.")
    exit()

# Connect to the private blockchain via the provided RPC URL
rpc_url = "http://10.229.43.182:8545"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if the connection is successful
if not web3.is_connected():
    print("Impossible de se connecter à la blockchain.")
    exit()

# Create an account from the private key
account = Account.from_key(private_key)

# Read addresses and names from liste.txt (assumes JSON format)
with open('liste.txt', 'r') as file:
    address_to_name = json.load(file)  # Load as a dictionary

# Convert 0.1 ETH to Wei
amount_in_wei = web3.to_wei(0.1, 'ether')

# Initialize the nonce
nonce = web3.eth.get_transaction_count(account.address)

# Loop through the addresses and send transactions
for address, name in address_to_name.items():
    address = address.strip()  # Remove spaces and newlines
    if web3.is_address(address):
        # Create a transaction
        tx = {
            'to': web3.to_checksum_address(address),  # Convert to checksum address
            'value': amount_in_wei,
            'gas': 21000,  # Gas limit
            'gasPrice': web3.to_wei('50', 'gwei'),  # Gas price
            'nonce': nonce,  # Use the current nonce
            'chainId': 32383  # Replace with your chain ID
        }

        # Sign the transaction with the private key
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)

        try:
            # Send the transaction
            tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)

            # Print the transaction hash and recipient name
            print(f"Transaction envoyée à {name} ({address}), Hash: {web3.to_hex(tx_hash)}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de la transaction à {name} ({address}): {e}")

        # Increment the nonce for the next transaction
        nonce += 1
    else:
        print(f"L'adresse {address} n'est pas valide.")