from backend.solana_utils import SolanaUtils

# Example usage
utils = SolanaUtils()
mnemonic = "raven snap earn taste fossil pelican law fever smoke cat mountain primary"
public_key = "FRop2RpXbp7ftp8CY3WzAJkPApfNcQwP2bn52xsC5iNp"

is_valid = utils.verify_mnemonic(mnemonic, public_key)
print(f"Mnemonic is valid: {is_valid}")
