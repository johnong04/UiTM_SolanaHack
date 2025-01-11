import streamlit as st
import subprocess
import json
import os
from pathlib import Path
import base58
from mnemonic import Mnemonic
import bip32utils
import hashlib

class SolanaWalletManager:
    def __init__(self):
        self.wallet_dir = Path("solana_wallet")
        self.wallet_dir.mkdir(exist_ok=True)

    def _run_command(self, command):
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return stdout.decode(), stderr.decode()

    def generate_mnemonic(self):
        """Generate a new mnemonic phrase"""
        mnemo = Mnemonic("english")
        return mnemo.generate(strength=256)  # 24 words

    def create_wallet(self, name: str) -> dict:
        """Create a new Solana wallet with mnemonic phrase"""
        wallet_path = self.wallet_dir / f"{name}.json"

        # Generate mnemonic
        mnemonic = self.generate_mnemonic()

        # Generate keypair using mnemonic
        stdout, stderr = self._run_command([
            "solana-keygen", "new",
            "--no-bip39-passphrase",
            "--force",
            "-o", str(wallet_path),
            "--seed", mnemonic
        ])

        # Get public key
        stdout, _ = self._run_command([
            "solana-keygen", "pubkey",
            str(wallet_path)
        ])

        public_key = stdout.strip()

        wallet_data = {
            "name": name,
            "public_key": public_key,
            "path": str(wallet_path),
            "mnemonic": mnemonic
        }

        # Save wallet data (including mnemonic) securely
        with open(self.wallet_dir / f"{name}_data.json", 'w') as f:
            json.dump(wallet_data, f)

        return wallet_data

    def list_wallets(self) -> list:
        """List all wallets in the wallet directory"""
        wallets = []
        for wallet_data_file in self.wallet_dir.glob("*_data.json"):
            with open(wallet_data_file, 'r') as f:
                wallet_data = json.load(f)
                wallets.append(wallet_data)
        return wallets

    def get_balance(self, public_key: str) -> float:
        """Get SOL balance for a wallet"""
        stdout, _ = self._run_command([
            "solana", "balance",
            public_key,
            "--url", "localhost"
        ])
        try:
            return float(stdout.split()[0])
        except:
            return 0.0

def main():
    st.title("Solana Wallet Manager")

    # Initialize wallet manager
    wallet_manager = SolanaWalletManager()

    # Sidebar for wallet creation
    st.sidebar.header("Create New Wallet")
    new_wallet_name = st.sidebar.text_input("Wallet Name")
    if st.sidebar.button("Create Wallet"):
        if new_wallet_name:
            try:
                wallet = wallet_manager.create_wallet(new_wallet_name)
                st.sidebar.success(f"Wallet created: {wallet['name']}")
                st.sidebar.code(f"Public Key: {wallet['public_key']}")

                # Display mnemonic phrase with warning
                st.sidebar.warning("⚠️ SAVE YOUR MNEMONIC PHRASE SECURELY!")
                st.sidebar.text_area(
                    "Mnemonic Phrase (24 words)",
                    wallet['mnemonic'],
                    height=100,
                    help="Write these words down and store them safely!"
                )
            except Exception as e:
                st.sidebar.error(f"Error creating wallet: {str(e)}")
        else:
            st.sidebar.warning("Please enter a wallet name")

    # Main content
    st.header("Your Wallets")

    # List existing wallets
    wallets = wallet_manager.list_wallets()

    if not wallets:
        st.info("No wallets found. Create one using the sidebar!")
    else:
        for wallet in wallets:
            with st.expander(f"Wallet: {wallet['name']}"):
                col1, col2 = st.columns(2)

                with col1:
                    st.text("Public Key")
                    st.code(wallet['public_key'])

                    balance = wallet_manager.get_balance(wallet['public_key'])
                    st.metric("Balance", f"{balance} SOL")

                with col2:
                    st.text("Wallet Path")
                    st.code(wallet['path'])

                    # Show mnemonic phrase in a secure way
                    if st.button("Show Recovery Phrase", key=f"show_{wallet['name']}"):
                        st.warning("⚠️ Keep this phrase secret and safe!")
                        st.text_area(
                            "Mnemonic Phrase",
                            wallet['mnemonic'],
                            height=100,
                            key=f"mnemonic_{wallet['name']}"
                        )

                    # Add airdrop button for testing
                    if st.button(f"Request Airdrop (1 SOL)", key=wallet['public_key']):
                        try:
                            stdout, stderr = wallet_manager._run_command([
                                "solana", "airdrop",
                                "1",
                                wallet['public_key'],
                                "--url", "localhost"
                            ])
                            if stderr:
                                st.error(f"Airdrop failed: {stderr}")
                            else:
                                st.success("Airdrop successful!")
                        except Exception as e:
                            st.error(f"Error during airdrop: {str(e)}")

    # Help section
    with st.expander("Help & Information"):
        st.markdown("""
        ### How to Use This Wallet Manager

        1. **Create a New Wallet**
           - Enter a wallet name in the sidebar
           - Click 'Create Wallet'
           - IMPORTANT: Save your mnemonic phrase securely!
           - Your wallet will be saved in the `solana_wallet` folder

        2. **View Existing Wallets**
           - All your wallets are listed in the main section
           - Click on each wallet to view details
           - See public key and current balance
           - Access recovery phrase when needed

        3. **Test with Airdrop**
           - Use the Airdrop button to get test SOL
           - Only works on test networks

        ### Security Notes
        - Keep your wallet files safe
        - Never share your private keys or mnemonic phrase
        - Store your mnemonic phrase in a secure location
        - Backup your wallet files regularly
        """)

if __name__ == "__main__":
    main()
