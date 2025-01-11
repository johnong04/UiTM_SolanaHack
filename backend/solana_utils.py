import subprocess
import json
import time
from pathlib import Path
import base58
from typing import Tuple, Optional

class SolanaUtils:
    def __init__(self):
        # Initialize token mint if not exists
        self.token_mint = self._get_or_create_token_mint()

    def _run_command(self, command: list) -> Tuple[str, str]:
        """Run a solana CLI command"""
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return stdout.decode(), stderr.decode()

    def _get_or_create_token_mint(self) -> str:
        """Get existing token mint or create new one"""
        # Check if we have stored the mint address
        mint_file = Path("token_mint.txt")
        if mint_file.exists():
            return mint_file.read_text().strip()

        # Create new token mint
        stdout, stderr = self._run_command([
            "spl-token", "create-token",
            "--decimals", "9"
        ])

        if stderr:
            raise Exception(f"Error creating token: {stderr}")

        # Extract token mint address
        mint_address = stdout.split()[2]
        mint_file.write_text(mint_address)

        return mint_address

    def check_balance(self, public_key: str) -> dict:
        """Get SOL and token balances"""
        # Get SOL balance
        stdout, _ = self._run_command([
            "solana", "balance",
            public_key,
            "--url", "localhost"
        ])
        sol_balance = float(stdout.split()[0])

        # Get token balance
        stdout, _ = self._run_command([
            "spl-token", "balance",
            self.token_mint,
            "--owner", public_key,
            "--url", "localhost"
        ])

        try:
            token_balance = int(stdout.strip())
        except:
            # Create token account if doesn't exist
            self._run_command([
                "spl-token", "create-account",
                self.token_mint,
                "--owner", public_key,
                "--url", "localhost"
            ])
            token_balance = 0

        return {
            "sol_balance": sol_balance,
            "token_balance": token_balance
        }

    def verify_mnemonic(self, mnemonic: str, public_key: str) -> bool:
        """Verify if mnemonic corresponds to public key"""
        try:
            # Save mnemonic to temporary file
            temp_file = Path("temp_key.json")
            temp_file.write_text(mnemonic)

            # Import keypair
            stdout, stderr = self._run_command([
                "solana-keygen", "recover",
                "temp_key.json"
            ])

            # Clean up
            temp_file.unlink()

            # Check if public keys match
            recovered_key = stdout.strip()
            return recovered_key == public_key
        except:
            return False

    def redeem_reward(self,
                     from_key: str,
                     mnemonic: str,
                     points: int) -> Optional[str]:
        """Process reward redemption"""
        try:
            # Verify mnemonic
            if not self.verify_mnemonic(mnemonic, from_key):
                return None

            # Create and sign transaction
            stdout, stderr = self._run_command([
                "spl-token", "transfer",
                self.token_mint,
                str(points),
                "Treasury_Account",  # Replace with actual treasury account
                "--from", from_key,
                "--fee-payer", from_key,
                "--url", "localhost"
            ])

            if stderr:
                return None

            # Extract transaction signature
            tx_hash = stdout.split()[-1]

            # Wait for confirmation
            time.sleep(1)

            return tx_hash
        except Exception as e:
            print(f"Error in redemption: {str(e)}")
            return None
