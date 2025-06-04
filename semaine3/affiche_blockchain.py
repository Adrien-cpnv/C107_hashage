from web3 import Web3
from dotenv import load_dotenv
import hashlib
import json

# Load configuration from environment file
load_dotenv("../key.env")
node_url = "http://10.229.43.182:8545"

# Connect to the blockchain node
w3 = Web3(Web3.HTTPProvider(node_url))
if not w3.is_connected():
    print("Erreur de connexion a la blockchain.")
    exit(1)
print("Connecté à la blockchain !")

# Get the latest block number
latest_block = w3.eth.block_number
print(f" Block : {latest_block}")

# Function to compute SHA-256 hash
def compute_sha256(data):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

# Function to iterate through all blocks and generate metadata
def get_all_transactions_with_metadata():
    for block_number in range(0, latest_block + 1):
        try:
            block = w3.eth.get_block(block_number, full_transactions=True)
            print(f"\n📦 Block n°{block_number} Nombre de transaction : {len(block.transactions)}")

            for tx in block.transactions:
                from_addr = tx['from']
                to_addr = tx['to']
                value_eth = w3.from_wei(tx['value'], 'ether')
                tx_hash = tx['hash'].hex()
                input_data = tx['input']
                decoded_input = ""

                # Attempt to decode the input data
                try:
                    decoded_input = w3.to_text(input_data)
                except:
                    decoded_input = "Impossible de décodér les données d'entrée"

                # Compute the SHA-256 hash of the input data
                input_hash = compute_sha256(input_data)

                # Create metadata for the transaction
                metadata = {
                    "blockNumber": block_number,
                    "transactionHash": tx_hash,
                    "from": from_addr,
                    "to": to_addr,
                    "value": f"{value_eth} ETH",
                    "inputData": decoded_input,
                    "inputHash": input_hash
                }

                # Print the metadata in JSON format
                metadata_json = json.dumps(metadata, indent=4)
                print(metadata_json)
        except Exception as e:
            print(f"Erreur du {block_number}: {e}")

# Start retrieving transactions with metadata
get_all_transactions_with_metadata()