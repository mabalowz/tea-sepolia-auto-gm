from web3 import Web3, HTTPProvider
import json
import random
import secrets
import time
import sys

# ANSI color codes
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# Banner dengan warna rainbow
print(f'{RED}H{YELLOW}e{GREEN}l{YELLOW}l{RED}o {CYAN}E{MAGENTA}V{GREEN}M {YELLOW}T{RED}e{CYAN}a {MAGENTA}S{GREEN}e{YELLOW}p{RED}o{CYAN}l{MAGENTA}i{YELLOW}a {GREEN}T{RED}e{YELLOW}s{CYAN}t{MAGENTA}n{GREEN}e{YELLOW}t {RED}B{CYAN}y {MAGENTA}M{YELLOW}a{GREEN}b{RED}a{YELLOW}l{CYAN}o{MAGENTA}w{YELLOW}z{RESET}')
print(f'{RED}- {GREEN}Auto {YELLOW}Interaction {RED}Contract{RESET}')
print(f'')

web3 = Web3(Web3.HTTPProvider("https://tea-sepolia.g.alchemy.com/public"))
chainId = web3.eth.chain_id

msg_abi = json.loads('[{"inputs": [],"name": "gm","outputs": [],"stateMutability": "nonpayable","type": "function"}]')

def log(txt):
    f = open('dataevmteasepolia.txt', "a")
    f.write(txt + '\n')
    f.close()
    
def get_base_gas_price():
    """Retrieve the base gas price from the latest block."""
    latest_block = web3.eth.get_block('latest')
    base_fee_per_gas = latest_block.get('baseFeePerGas', None)

    if base_fee_per_gas is None:
        raise ValueError("Base fee per gas not available in this block.")

    return base_fee_per_gas

def writeContract(sender, key, ctraddr):
    try:
        getGasPrice = web3.from_wei(int(get_base_gas_price()), 'gwei')
        max_priority_fee = (5*getGasPrice)/100
        max_fee = getGasPrice + max_priority_fee
        gasPrice = web3.to_wei(max_fee, 'gwei')
        nonce = web3.eth.get_transaction_count(sender)
        msg_contract = web3.eth.contract(address=web3.to_checksum_address(ctraddr), abi=msg_abi)
        gasAmount = msg_contract.functions.gm().estimate_gas({
            'chainId': chainId,
            'from': sender,
            'gasPrice': gasPrice,
            'nonce': nonce
        })

        msg_tx = msg_contract.functions.gm().build_transaction({
            'chainId': chainId,
            'from': sender,
            'gasPrice': gasPrice,
            'gas': gasAmount,
            'nonce': nonce
        })
        
        #sign & send the transaction
        tx_hash = web3.eth.send_raw_transaction(web3.eth.account.sign_transaction(msg_tx, key).rawTransaction)
        #get transaction hash
        print(f'Processing Interaction On Contract {ctraddr} From {sender} ...')
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(f'Interaction On Contract {ctraddr} From {sender} Success!')
        print(f'TX-ID : {str(web3.to_hex(tx_hash))}')
    except Exception as e:
        print(f'Error : {e}')
        pass
        
def get_random_address_from_block(block_number=None):
    try:
        # If no block number is provided, get the latest block
        if block_number is None:
            block = web3.eth.get_block('latest', full_transactions=True)
        else:
            block = web3.eth.get_block(block_number, full_transactions=True)

        # Collect addresses involved in transactions (both from and to addresses)
        addresses = set()  # Use a set to avoid duplicates
        
        for tx in block['transactions']:
            sender = tx['from']
            recipient = tx['to']
            
            addresses.add(sender)
            if recipient:
                addresses.add(recipient)
        
        if not addresses:
            print("No addresses found in this block.")
            return None

        # Randomly select an address from the set of addresses
        random_address = random.choice(list(addresses))
        return random_address
    
    except Exception as e:
        print(f"Error while fetching block data: {e}")
        return None


tx_count = int(input('Number of transactions to execute: '))
print(f'')         

def sendTX():
    try:
        executed_txs = 0
        while executed_txs < tx_count:
            with open('pvkeylist.txt', 'r') as file:
                local_data = file.read().splitlines()

                # Check if the file is empty
                if not local_data:
                    print("Notice: 'pvkeylist.txt' is empty. Exiting...")
                    sys.exit(1)

                # Process each private key in the list
                for pvkeylist in local_data:
                    try:
                        if executed_txs >= tx_count:
                            break
                            
                        # Check if the private key is valid
                        sender = web3.eth.account.from_key(pvkeylist)
                    except ValueError:
                        print(f"Notice: Invalid private key format. Exiting...")
                        sys.exit(1)
                    
                    sender = web3.eth.account.from_key(pvkeylist)
                    recipient = web3.to_checksum_address(get_random_address_from_block())
                    
                    print(f'\n=== Transaction {executed_txs + 1} of {tx_count} ===')
                    ctraddr = "0xB4edA1fA0476405fE8f4BCc6F35D5D2d4A456775"
                    print(f'')
                    writeContract(sender.address, sender.key, ctraddr)
                    print(f'')                    
                    executed_txs += 1
                    
                    # Add delay between transactions to avoid nonce issues
                    time.sleep(5)
                    
    except Exception as e:
        print(f'Error : {e}')
        pass
        
sendTX()
