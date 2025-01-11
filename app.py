import streamlit as st
from datetime import datetime, timedelta
import random

# Page configuration
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

# Title Section
st.markdown("""
    <div class='title-section'>
        <h1 style='font-size: 2.8rem; color: #9945FF; margin-bottom: 0.2rem;'>Soezliana</h1>
        <h3 style='color: #fff; font-size: 1.2rem;'>Unified Healthcare Rewards on Solana</h3>
    </div>
""", unsafe_allow_html=True)

# Points Summary
st.markdown("""
    <div class='points-card'>
        <h1 style='font-size: 2.8rem; color: #9945FF; margin: 0;'>125,750</h1>
        <p style='font-size: 1rem; color: #fff; margin: 0;'>Total Healthcare Points Accumulated via Solana</p>
    </div>
""", unsafe_allow_html=True)

# Recent Activity Section
st.markdown("<h2 class='section-title'>Recent Healthcare Activities</h2>", unsafe_allow_html=True)

activities = [
    {
        "date": (datetime.now() - timedelta(days=x)).strftime("%Y-%m-%d"),
        "app": app,
        "points": points,
        "tx": f"https://solscan.io/tx/{random.randint(1000000, 9999999)}"
    }
    for x, (app, points) in enumerate([
        ("MedFit Tracker", 500),
        ("WellnessRewards", 250),
        ("HealthCheck+", 1000),
        ("NutriPoints", 750),
        ("MentalWell", 300)
    ])
]

for activity in activities:
    with st.container():
        st.markdown(f"""
            <div class='activity-container'>
                <div style='display: grid; grid-template-columns: 2fr 2fr 2fr 3fr; gap: 1rem; align-items: center;'>
                    <div>{activity['date']}</div>
                    <div>{activity['app']}</div>
                    <div style='color: #9945FF; font-weight: bold;'>+{activity['points']} pts</div>
                    <div><a href='{activity['tx']}' target='_blank' style='color: #9945FF;'>View on Solana</a></div>
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
        st.button(f"Redeem for {reward['points']} points", key=reward['name'])

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

# Footer Section
st.markdown("""
    <div class='footer'>
        © 2024 John Ong from Team Hoshino Universiti Malaya
    </div>
""", unsafe_allow_html=True)