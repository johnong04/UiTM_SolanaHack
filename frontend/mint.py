import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from backend.solana_utils import SolanaUtils
import time

def main():
    st.title("Solana Token Minting Interface")

    # Initialize SolanaUtils
    try:
        solana = SolanaUtils()
    except Exception as e:
        st.error(f"Failed to initialize Solana utils: {str(e)}")
        return

    # Sidebar
    st.sidebar.header("Network Information")
    st.sidebar.text("Connected to: Local Network")
    if solana.token_mint:
        st.sidebar.text(f"Token Mint: {solana.token_mint[:8]}...")

    # Main content
    tabs = st.tabs(["Mint Tokens", "Check Balance", "Redeem Rewards"])

    # Mint Tokens Tab
    with tabs[0]:
        st.header("Mint New Tokens")

        recipient_key = st.text_input("Recipient Public Key")
        amount = st.number_input("Amount to Mint", min_value=1, value=1000)
        mnemonic = st.text_input("Mnemonic Phrase", type="password")

        if st.button("Mint Tokens"):
            with st.spinner("Processing mint transaction..."):
                try:
                    # Verify mnemonic first
                    if solana.verify_mnemonic(mnemonic, recipient_key):
                        # Create token account if doesn't exist
                        balances = solana.check_balance(recipient_key)

                        # Mint tokens (you'll need to add this method to SolanaUtils)
                        tx_hash = solana._run_command([
                            "spl-token", "mint",
                            solana.token_mint,
                            str(amount),
                            "--owner", recipient_key,
                            "--url", "localhost"
                        ])

                        if tx_hash[0]:  # Check stdout
                            st.success(f"Successfully minted {amount} tokens!")
                            st.info(f"Transaction Hash: {tx_hash[0]}")
                        else:
                            st.error("Minting failed")
                    else:
                        st.error("Invalid mnemonic phrase")
                except Exception as e:
                    st.error(f"Error during minting: {str(e)}")

    # Check Balance Tab
    with tabs[1]:
        st.header("Check Balances")

        check_key = st.text_input("Public Key to Check")
        if st.button("Check Balance"):
            with st.spinner("Fetching balances..."):
                try:
                    balances = solana.check_balance(check_key)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("SOL Balance", f"{balances['sol_balance']:.4f}")
                    with col2:
                        st.metric("Token Balance", balances['token_balance'])
                except Exception as e:
                    st.error(f"Error checking balance: {str(e)}")

    # Redeem Rewards Tab
    with tabs[2]:
        st.header("Redeem Rewards")

        from_key = st.text_input("From Public Key")
        points = st.number_input("Points to Redeem", min_value=1)
        redeem_mnemonic = st.text_input("Enter Mnemonic to Confirm", type="password")

        if st.button("Redeem"):
            with st.spinner("Processing redemption..."):
                try:
                    tx_hash = solana.redeem_reward(from_key, redeem_mnemonic, points)
                    if tx_hash:
                        st.success("Redemption successful!")
                        st.info(f"Transaction Hash: {tx_hash}")
                    else:
                        st.error("Redemption failed")
                except Exception as e:
                    st.error(f"Error during redemption: {str(e)}")

    # Help section
    with st.expander("Need Help?"):
        st.markdown("""
        ### How to Use
        1. **Minting Tokens**:
           - Enter recipient's public key
           - Specify amount to mint
           - Provide mnemonic phrase for authorization

        2. **Checking Balance**:
           - Enter public key to check
           - View both SOL and token balances

        3. **Redeeming Rewards**:
           - Enter your public key
           - Specify points to redeem
           - Confirm with mnemonic phrase

        ### Requirements
        - Local Solana network running
        - Sufficient SOL for transaction fees
        - Valid mnemonic phrase for transactions
        """)

if __name__ == "__main__":
    main()
