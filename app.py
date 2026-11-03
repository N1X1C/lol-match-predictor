import streamlit as st
import pandas as pd
import importlib

st.set_page_config(page_title="LoL Match Predictor", page_icon="🎮", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0f1d 0%, #1a1f3c 100%);
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    div[data-testid="stForm"] {
        background: rgba(15, 22, 41, 0.85) !important;
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 25px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.5);
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #ffffff !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
    }
    div[data-testid="stFormSubmitButton"] > button {
        width: 100%; border-radius: 12px; 
        background: linear-gradient(90deg, #ff0055 0%, #00f2fe 100%); 
        color: white !important; font-size: 20px; font-weight: bold; border: none; 
        padding: 12px; box-shadow: 0px 0px 25px rgba(0, 242, 254, 0.6);
    }
    div[data-testid="stFormSubmitButton"] > button:hover {
        transform: scale(1.02); transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

try:
    backend = importlib.import_module('model')
    model = backend.dt_model
    features = backend.features
    accuracy = backend.accuracy
except Exception:
    st.error("خطا: فایل model.py یا دیتابیس پیدا نشد.")
    st.stop()

st.markdown("<h1 style='text-align: center; color: #00f2fe; font-family: Tahoma;'>🎮 هوش مصنوعی پیش‌بینی مسابقات League of Legends</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #bd93f9;'>آموزش دیده با درخت تصمیم (Decision Tree) | دقت مدل روی داده‌های واقعی: {round(accuracy * 100, 1)}%</p><hr>", unsafe_allow_html=True)

with st.form("match_stats"):
    st.markdown("<h3>📊 اطلاعات ۱۰ دقیقه اول بازی را وارد کنید:</h3>", unsafe_allow_html=True)
    first_blood = st.radio("🩸 کدام تیم First Blood گرفت؟", ["تیم آبی (Blue)", "تیم قرمز (Red)"], horizontal=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col_blue, col_red = st.columns(2)

    with col_blue:
        st.markdown("<h3 style='color: #4facfe;'>🔵 آمار تیم آبی</h3>", unsafe_allow_html=True)
        blue_kills = st.number_input("تعداد Kills (آبی)", min_value=0, max_value=50, value=5)
        blue_assists = st.number_input("تعداد Assists (آبی)", min_value=0, max_value=50, value=5)
        blue_dragons = st.selectbox("تعداد اژدها / Dragons (آبی)", [0, 1, 2, 3], key="bd")
        blue_towers = st.selectbox("برج‌های نابود شده (آبی)", [0, 1, 2, 3, 4, 5], key="bt")
        blue_gold = st.slider("مجموع سکه (Gold) تیم آبی:", min_value=10000, max_value=30000, value=17000, step=100, key="bg")
        blue_xp = st.slider("مجموع تجربه (XP) تیم آبی:", min_value=10000, max_value=30000, value=17000, step=100, key="bx")

    with col_red:
        st.markdown("<h3 style='color: #ff4b4b;'>🔴 آمار تیم قرمز</h3>", unsafe_allow_html=True)
        red_kills = st.number_input("تعداد Kills (قرمز)", min_value=0, max_value=50, value=5, key="rk")
        red_assists = st.number_input("تعداد Assists (قرمز)", min_value=0, max_value=50, value=5, key="ra")
        red_dragons = st.selectbox("تعداد اژدها / Dragons (قرمز)", [0, 1, 2, 3], key="rd")
        red_towers = st.selectbox("برج‌های نابود شده (قرمز)", [0, 1, 2, 3, 4, 5], key="rt")
        red_gold = st.slider("مجموع سکه (Gold) تیم قرمز:", min_value=10000, max_value=30000, value=17000, step=100, key="rg")
        red_xp = st.slider("مجموع تجربه (XP) تیم قرمز:", min_value=10000, max_value=30000, value=17000, step=100, key="rx")

    st.markdown("<br>", unsafe_allow_html=True)
    submitted = st.form_submit_button("🔮 پیش‌بینی نتیجه مسابقه")

if submitted:
    new_match = pd.DataFrame([{
        "blueFirstBlood": 1 if first_blood == "تیم آبی (Blue)" else 0,
        "blueKills": blue_kills,
        "redKills": red_kills,
        "blueAssists": blue_assists,
        "redAssists": red_assists,
        "blueDragons": blue_dragons,
        "redDragons": red_dragons,
        "blueTowersDestroyed": blue_towers,
        "redTowersDestroyed": red_towers,
        "blueTotalGold": blue_gold,
        "redTotalGold": red_gold,
        "blueTotalExperience": blue_xp,
        "redTotalExperience": red_xp
    }], columns=features)

    prediction = model.predict(new_match)[0]
    probabilities = model.predict_proba(new_match)[0]

    blue_prob = probabilities[1] * 100
    red_prob = probabilities[0] * 100

    st.markdown("<br>", unsafe_allow_html=True)

    if prediction == 1:
        st.markdown(f"""
        <div style="background: rgba(0, 242, 254, 0.2); padding: 20px; border-radius: 10px; border-left: 5px solid #00f2fe; text-align: center;">
            <h2 style="color: #00f2fe; margin:0;">🏆 پیش‌بینی هوش مصنوعی: پیروزی تیم آبی (Blue Team)</h2>
            <p style="font-size: 18px; margin-top: 10px;">احتمال برد تیم آبی: <b>{blue_prob:.1f}%</b> | احتمال برد تیم قرمز: <b>{red_prob:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: rgba(255, 75, 75, 0.2); padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; text-align: center;">
            <h2 style="color: #ff4b4b; margin:0;">🏆 پیش‌بینی هوش مصنوعی: پیروزی تیم قرمز (Red Team)</h2>
            <p style="font-size: 18px; margin-top: 10px;">احتمال برد تیم قرمز: <b>{red_prob:.1f}%</b> | احتمال برد تیم آبی: <b>{blue_prob:.1f}%</b></p>
        </div>
        """, unsafe_allow_html=True)
