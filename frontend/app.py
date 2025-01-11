import streamlit as st
from datetime import datetime, timedelta
import random
import string
import time
import requests

# API Configuration
API_URL = "http://localhost:8000"

# Global variables for account balances

if 'USER1_ACC_SOL' not in st.session_state:
    st.session_state.USER1_ACC_SOL = 8500
if 'USER1_ACC_TOKEN' not in st.session_state:
    st.session_state.USER1_ACC_TOKEN = 150000

# Session State Initialization
if "user_public_key" not in st.session_state:
    st.session_state.user_public_key = ""
if "redeemed_rewards" not in st.session_state:
    st.session_state.redeemed_rewards = []
if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

# Utility Functions
def generate_tx_hash():
    """Generate a fake Solana transaction hash"""
    return ''.join(random.choices(string.hexdigits, k=64)).lower()

def simulate_transaction():
    """Simulate a blockchain transaction with delay"""
    with st.spinner('Processing transaction on Solana...'):
        time.sleep(2)  # Simulate blockchain confirmation time
    return generate_tx_hash()

def get_user_balances(public_key):
    return st.session_state.USER1_ACC_SOL, st.session_state.USER1_ACC_TOKEN

def update_balance(public_key, points_to_deduct):
    """Update user balance in session state"""
    try:
        st.session_state.USER1_ACC_TOKEN -= points_to_deduct
        return True
    except Exception as e:
        st.error(f"Error updating balance: {str(e)}")
        return False

def redeem_reward(reward):
    """Handle reward redemption process"""
    if not st.session_state.user_public_key:
        st.error("Please enter your public key in the sidebar.")
        return

    sol_balance, token_balance = get_user_balances(st.session_state.user_public_key)

    if token_balance < reward['points']:
        st.error(f"Insufficient points. You need {reward['points']} points but have {token_balance}.")
        return

    status_placeholder = st.empty()
    tx_hash = simulate_transaction()

    if update_balance(st.session_state.user_public_key, reward['points']):
        redemption = {
            'reward': reward['name'],
            'points': reward['points'],
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'tx_hash': tx_hash
        }
        st.session_state.redeemed_rewards.append(redemption)

        # Add to transaction history
        st.session_state.transaction_history.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': 'Redemption',
            'points': -reward['points'],
            'tx': tx_hash
        })

        status_placeholder.success(f"""
        ✅ Successfully redeemed: {reward['name']}
        Points deducted: {reward['points']}
        Transaction Hash: [{tx_hash[:8]}...{tx_hash[-8:]}](https://solscan.io/tx/{tx_hash})
        """)

        time.sleep(1)
        st.rerun()
    else:
        status_placeholder.error("Transaction failed. Please try again.")

# Page Configuration
st.set_page_config(
    page_title="Soezliana - Healthcare Rewards on Solana",
    page_icon="⚕️",
    layout="wide"
)

# Custom CSS with dark theme improvements
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #9945FF;
        color: white;
        border-radius: 10px;
        padding: 0.5rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #8935ee;
        transform: translateY(-2px);
    }
    .points-card {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9), rgba(35, 35, 35, 0.8));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .title-section {
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 0.5rem;
        color: white;
    }
    .section-title {
        font-size: 1.8rem;
        color: white;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #9945FF;
        display: inline-block;
    }
    .reward-card {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9), rgba(35, 35, 35, 0.8));
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        margin-bottom: 1rem;
        height: 400px;
        display: flex;
        flex-direction: column;
        transition: transform 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    .reward-card:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(153, 69, 255, 0.3);
    }
    .reward-image-container {
        width: 100%;
        height: 200px;
        overflow: hidden;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    .reward-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .activity-container {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9), rgba(35, 35, 35, 0.8));
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    .activity-container:hover {
        transform: translateX(5px);
        border: 1px solid rgba(153, 69, 255, 0.3);
    }
    .platform-card {
        background: linear-gradient(135deg, rgba(25, 25, 25, 0.9), rgba(35, 35, 35, 0.8));
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        margin: 0.5rem;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: white;
    }
    .platform-card:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(153, 69, 255, 0.3);
    }
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.8rem;
        margin-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Account")
st.session_state.user_public_key = st.sidebar.text_input(
    "Your Public Key",
    value=st.session_state.user_public_key
)

# Main Page Title
st.markdown("""
    <div class='title-section'>
        <h1 style='font-size: 2.8rem; color: #9945FF; margin-bottom: 0.2rem;'>Soezliana</h1>
        <h3 style='color: #fff; font-size: 1.2rem;'>Unified Healthcare Rewards on Solana</h3>
    </div>
""", unsafe_allow_html=True)

# Points Summary
if st.session_state.user_public_key:
    sol_balance, token_balance = get_user_balances(st.session_state.user_public_key)
    total_points = token_balance
else:
    total_points = 0

st.markdown(f"""
    <div class='points-card'>
        <h1 style='font-size: 2.8rem; color: #9945FF; margin: 0;'>{total_points}</h1>
        <p style='font-size: 1rem; color: #fff; margin: 0;'>Total Healthcare Points Accumulated via Solana</p>
    </div>
""", unsafe_allow_html=True)

# Recent Activity Section
st.markdown("<h2 class='section-title'>Recent Healthcare Activities</h2>", unsafe_allow_html=True)

# Combine redeemed rewards with regular activities
all_activities = st.session_state.transaction_history + [
    {
        "date": (datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d"),
        "type": app,
        "points": points,
        "tx": generate_tx_hash()
    }
    for x, (app, points) in enumerate([
        ("MedFit Tracker", 500),
        ("WellnessRewards", 250),
        ("HealthCheck+", 1000),
        ("NutriPoints", 750),
        ("MentalWell", 300)
    ])
]

# Sort activities by date
all_activities.sort(key=lambda x: datetime.strptime(x['date'], "%Y-%m-%d"), reverse=True)

for activity in all_activities:
    with st.container():
        st.markdown(f"""
            <div class='activity-container'>
                <div style='display: grid; grid-template-columns: 2fr 2fr 2fr 3fr; gap: 1rem; align-items: center;'>
                    <div>{activity['date']}</div>
                    <div>{activity['type']}</div>
                    <div style='color: {"#FF4B4B" if activity.get("points", 0) < 0 else "#9945FF"}; font-weight: bold;'>
                        {'+' if activity['points'] > 0 else ''}{activity['points']} pts
                    </div>
                    <div><a href='https://solscan.io/tx/{activity['tx']}' target='_blank' style='color: #9945FF;'>
                        View on Solana
                    </a></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Rewards Section
st.markdown("<h2 class='section-title'>Available Healthcare Rewards</h2>", unsafe_allow_html=True)

rewards = [
    {
        "name": "Annual Health Checkup",
        "points": 5000,
        "image": "https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
        "description": "Complete health screening package"
    },
    {
        "name": "Wellness Subscription",
        "points": 7500,
        "image": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
        "description": "3-month premium wellness app access"
    },
    {
        "name": "Medical Coverage Boost",
        "points": 10000,
        "image": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3",
        "description": "Additional medical coverage worth $500"
    }
]

reward_cols = st.columns(3)
for idx, reward in enumerate(rewards):
    with reward_cols[idx]:
        st.markdown(f"""
            <div class='reward-card'>
                <div class='reward-image-container'>
                    <img src='{reward['image']}' class='reward-image' alt='{reward['name']}'>
                </div>
                <h4 style='margin: 0.5rem 0;'>{reward['name']}</h4>
                <p style='color: rgba(255, 255, 255, 0.8); flex-grow: 1;'>{reward['description']}</p>
                <p style='color: #9945FF; font-weight: bold; margin: 0.5rem 0;'>{reward['points']} points</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button(f"Redeem for {reward['points']} points", key=reward['name']):
            redeem_reward(reward)

# Connected Platforms Section
st.markdown("<h2 class='section-title'>Connected Healthcare Platforms</h2>", unsafe_allow_html=True)
app_cols = st.columns(5)
apps = [
    ("MedFit Tracker", "⚕️", True),
    ("WellnessRewards", "🏥", True),
    ("HealthCheck+", "🫀", True),
    ("NutriPoints", "🥗", False),
    ("MentalWell", "🧠", True)
]

for i, (app_name, icon, connected) in enumerate(apps):
    with app_cols[i]:
        st.markdown(f"""
            <div class='platform-card'>
                <div style='font-size: 1.5rem; margin-bottom: 0.5rem;'>{icon}</div>
                <div style='font-weight: bold; margin-bottom: 0.3rem;'>{app_name}</div>
                <div style='color: {"#28a745" if connected else "#dc3545"};'>
                    {('✅ Connected' if connected else '❌ Not Connected')}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='footer'>
        © 2024 John Ong and Sze Yu Sim from Team Hoshino Universiti Malaya
    </div>
""", unsafe_allow_html=True)
