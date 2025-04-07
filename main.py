import json
from web3 import Web3
from eth_account import Account

# Configuration
CONTRACT_ADDRESS = "0xB4edA1fA0476405fE8f4BCc6F35D5D2d4A456775"
RPC_URLS = [
    "https://tea-sepolia.g.alchemy.com/v2/bsayB3hJ3hij6-t5YUUQBL5jDV-o5h2f",
    "https://tea-sepolia.g.alchemy.com/v2/Wa-bUwSDb2nujeYWyIZ9eHK3XXsxiM8j",
    "https://tea-sepolia.g.alchemy.com/public"
]
CHAIN_ID = 10218
WALLET_FILE = 'wallet.txt'

# ABI for the smart contract
ABI = [
    {
        "inputs": [],
        "name": "gm",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

def send_gm(private_key, rpc_url, nonce):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        account = Account.from_key(private_key)
        contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

        current_gas_price = w3.eth.gas_price
        increased_gas_price = int(current_gas_price * 1.05)  # Increase gas price by 5%

        tx = contract.functions.gm().build_transaction({
            'gasPrice': increased_gas_price,
            'nonce': nonce,
            'chainId': CHAIN_ID
        })

        signed_tx = account.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Sending 'gm()' from address: {account.address} with nonce: {nonce}")
        print(f"Transaction hash: {tx_hash.hex()}")
        print("Transaction confirmed!")
        print(f"Gas used: {tx_receipt['gasUsed']}")
        print("-------------------------")
        return True
    except Exception as e:
        print(f"Error sending gm() from {account.address}: {e}")
        print("-------------------------")
        return False

def process_wallets():
    try:
        with open(WALLET_FILE, 'r') as f:
            private_keys = [line.strip() for line in f if line.strip()]

        if not private_keys:
            print(f"No private keys found in {WALLET_FILE}")
            return

        for i, private_key in enumerate(private_keys):
            rpc_url = RPC_URLS[i % len(RPC_URLS)]
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            account = Account.from_key(private_key)
            nonce = w3.eth.get_transaction_count(account.address, 'latest')
            send_gm(private_key, rpc_url, nonce + i) # Increment nonce for each account

        print("Finished processing all wallets.")

    except FileNotFoundError:
        print(f"Error: Wallet file '{WALLET_FILE}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    process_wallets()