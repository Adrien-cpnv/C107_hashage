import json
import codecs
import hashlib
from dotenv import load_dotenv
import os
from web3 import Web3, Account

# Load environment variables
load_dotenv('../key.env')
private_key = os.getenv('PRIVATE_KEY')

if private_key is None:
    print("Private key not found.")
    exit()

# Connect to the blockchain
rpc_url = "http://10.229.43.182:8545"
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    print("Unable to connect to the blockchain.")
    exit()

# Create an account from the private key
account = Account.from_key(private_key)
sender_address = account.address
recipient_address = web3.to_checksum_address("0x0000000000000000000000000000000000000000")

# File path for the PDF
pdf_file_path = r"N:/Commun/ELEVE/INFO/SI-C2b/4emeTrimestre/C107/Adrien.pdf"

# Function to compute SHA-256 hash of a file
def compute_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Compute the hash of the PDF file
pdf_hash = compute_sha256(pdf_file_path)
print("Computed SHA-256 hash of the file:", pdf_hash)

# Create metadata
metadata = {
    "filePath": pdf_file_path,
    "fileHash": pdf_hash
}
metadata_json = json.dumps(metadata)
print("Metadata JSON:", metadata_json)

# Convert metadata to hex
metadata_hex = "0x" + codecs.encode(metadata_json.encode(), "hex").decode()
print("Hex representation of metadata:", metadata_hex)

# Get the current nonce
nonce = web3.eth.get_transaction_count(sender_address)

# Build the transaction
transaction = {
    'from': sender_address,
    'to': recipient_address,
    'value': 0,
    'gas': 200000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': nonce,
    'chainId': 32383,
    'data': metadata_hex
}

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
print("Transaction sent, tx hash:", web3.to_hex(tx_hash))

# Wait for the transaction receipt
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print("Transaction receipt received:", receipt)