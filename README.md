# tea-sepolia-auto-gm
Auto send gm in Tea Sepolia testnet


![Banner](https://img.shields.io/badge/Helper-EVM_Tea_Sepolia_Testnet-brightgreen)
![Version](https://img.shields.io/badge/Version-2.0-blue)
![License](https://img.shields.io/badge/License-MIT-orange)

Script otomatis untuk berinteraksi dengan jaringan EVM Tea Sepolia Testnet.

## 🌟 Fitur Utama

- 🤖 **Auto Interaction Contract** - Berinteraksi dengan kontrak yang sudah terdeploy

## 🛠️ Persyaratan


- Python 3.8+
- Library Web3.py
- Koneksi internet
- File `privatekey.txt` berisi private key (satu key per baris)

## ⚙️ Instalasi


1. Install Python 3.10 :
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install software-properties-common -y
   sudo add-apt-repository ppa:deadsnakes/ppa -y
   sudo apt update
   sudo apt install python3.10 python3.10-venv python3.10-dev -y

2. Membuat Virtual Environment :
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Dependency Installation :
   ```bash
   pip install web3 python-dotenv

4. Execution Script :
   ```bash
   python3 main.py
   or 
   python main.py

**Input Prompts:**

**privatekey.txt (isi dengan privatekey kalian)**

**Number of Transactions (e.g., 5)**
