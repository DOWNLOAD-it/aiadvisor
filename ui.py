import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
from dotenv import load_dotenv
from tensorflow.keras.layers import Layer
from groq import Groq

# =====================================================
# 1. INITIALIZATION & SESSION STATE
# =====================================================
load_dotenv()

# Initialize session state variables if they don't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "financial_context" not in st.session_state:
    st.session_state.financial_context = None
if "preds_user" not in st.session_state:
    st.session_state.preds_user = None

st.set_page_config(page_title="AI Financial Advisor", page_icon="💰", layout="wide")

# Styling
st.markdown(
    """
<style>
    .main { background-color: #f8fafc; }
    [data-testid="stMetricValue"] { font-weight: 700; }
    .advisor-box {
        background-color: #ffffff;
        padding: 20px;
        border-left: 5px solid #2563eb;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# 2. CONSTANTS & ASSET LOADING
# =====================================================
EXCHANGE_RATES = {
    "MAD (Moroccan Dirham)": 8.35,
    "INR (Rupee)": 1.0,
    "USD (Dollar)": 83.20,
}
CATEGORIES = [
    "Groceries",
    "Transport",
    "Eating Out",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Education",
    "Misc",
]


class AttentionLayer(Layer):
    def build(self, input_shape):
        self.W = self.add_weight(
            name="att_weight",
            shape=(input_shape[-1], 1),
            initializer="normal",
            trainable=True,
        )
        self.b = self.add_weight(
            name="att_bias",
            shape=(input_shape[1], 1),
            initializer="zeros",
            trainable=True,
        )
        super().build(input_shape)

    def call(self, x):
        e = tf.matmul(x, self.W) + self.b
        e = tf.squeeze(e, -1)
        a = tf.nn.softmax(e)
        a = tf.expand_dims(a, -1)
        return tf.reduce_sum(x * a, axis=1)


@st.cache_resource
def load_assets():
    custom_objs = {
        "AttentionLayer": AttentionLayer,
        "mse": tf.keras.losses.MeanSquaredError(),
    }
    model = tf.keras.models.load_model("savings_model.h5", custom_objects=custom_objs)
    scaler = joblib.load("scaler.joblib")
    encoder = joblib.load("encoder.joblib")
    return model, scaler, encoder


model, scaler, encoder = load_assets()


# =====================================================
# 3. LLM LOGIC
# =====================================================
def get_llm_response(prompt):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "AI Insight unavailable (missing API key)."
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Insight temporarily unavailable: {e}"


# =====================================================
# 4. SIDEBAR & INPUTS
# =====================================================
with st.sidebar:
    st.title("⚙️ Settings")
    selected_currency = st.selectbox("Currency", list(EXCHANGE_RATES.keys()))
    rate = EXCHANGE_RATES[selected_currency]
    sym = selected_currency.split(" ")[0]
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

st.title("💰 Smart Savings Optimizer")
tab_profile, tab_spending = st.tabs(["👤 Profile", "💸 Spending"])

with tab_profile:
    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input(
            f"Monthly Income ({sym})", min_value=0.0, value=15000.0
        )
        age = st.slider("Age", 18, 90, 30)
    with col2:
        occupation = st.selectbox(
            "Occupation", ["Professional", "Self_Employed", "Retired", "Student"]
        )
        city_tier = st.selectbox("City Tier", ["Tier_1", "Tier_2", "Tier_3"])
    desired_savings_pct = st.slider("Target Savings (%)", 5, 50, 20)

with tab_spending:
    c1, c2, c3 = st.columns(3)
    with c1:
        groceries = st.number_input("Groceries", value=3000.0)
        transport = st.number_input("Transport", value=1000.0)
    with c2:
        eating_out = st.number_input("Eating Out", value=1500.0)
        entertainment = st.number_input("Entertainment", value=800.0)
    with c3:
        utilities = st.number_input("Utilities", value=1200.0)
        misc = st.number_input("Miscellaneous", value=1000.0)

# =====================================================
# 5. ANALYSIS EXECUTION
# =====================================================
if st.button("✨ Analyze Financial Status"):
    if income <= 0:
        st.error("Please enter a valid income.")
    else:
        # Prepare model input
        input_data = {
            "Income": income * rate,
            "Age": age,
            "Dependents": 2,
            "Disposable_Income": income * 0.7 * rate,
            "Desired_Savings": income * desired_savings_pct / 100 * rate,
            "Groceries": groceries * rate,
            "Transport": transport * rate,
            "Eating_Out": eating_out * rate,
            "Entertainment": entertainment * rate,
            "Utilities": utilities * rate,
            "Healthcare": 200 * rate,
            "Education": 1000 * rate,
            "Miscellaneous": misc * rate,
        }

        # ML Processing
        num_df = pd.DataFrame([input_data])
        num_df[num_df.columns] = scaler.transform(num_df[num_df.columns])
        cat_encoded = encoder.transform(
            pd.DataFrame([{"Occupation": occupation, "City_Tier": city_tier}])
        )
        final_input = pd.concat(
            [
                num_df,
                pd.DataFrame(cat_encoded, columns=encoder.get_feature_names_out()),
            ],
            axis=1,
        )

        preds = model.predict(final_input, verbose=0)[0]
        st.session_state.preds_user = preds / rate

        # Metrics Calculations
        total_saved = float(np.sum(st.session_state.preds_user))
        target_goal = income * desired_savings_pct / 100
        goal_diff = total_saved - target_goal
        efficiency = (total_saved / income) * 100
        top_cat = CATEGORIES[int(np.argmax(st.session_state.preds_user))]

        # Store results in Session State for Chat context
        st.session_state.financial_context = {
            "income": income,
            "total_saved": total_saved,
            "target_goal": target_goal,
            "goal_diff": goal_diff,
            "efficiency": efficiency,
            "top_cat": top_cat,
            "sym": sym,
            "occupation": occupation,
        }

        # Auto-generate first AI response
        initial_prompt = f"Analyze: Income {income}{sym}, Savings {total_saved:.2f}{sym}, Top Category {top_cat}. Give concise advice for a {occupation}."
        initial_insight = get_llm_response(initial_prompt)
        st.session_state.chat_history = [("AI", initial_insight)]

# =====================================================
# 6. PERSISTENT DASHBOARD & CHAT (Outside the Button)
# =====================================================
if st.session_state.financial_context:
    ctx = st.session_state.financial_context

    # Show Dashboard
    st.markdown("---")
    st.subheader("📊 Financial Overview")
    m1, m2, m3 = st.columns(3)
    m1.metric(
        "Potential Savings",
        f"{ctx['sym']} {ctx['total_saved']:,.2f}",
        delta=f"{ctx['goal_diff']:,.2f} vs Target",
        delta_color="normal" if ctx["goal_diff"] >= 0 else "inverse",
    )
    m2.metric("Top Opportunity", ctx["top_cat"])
    m3.metric(
        "Efficiency Score",
        f"{ctx['efficiency']:.1f}%",
        delta="Savings / Income",
        delta_color="normal" if ctx["efficiency"] >= desired_savings_pct else "inverse",
    )

    # Show Chat History
    st.markdown("---")
    st.subheader("🤖 AI Financial Advisor Chat")

    for role, message in st.session_state.chat_history:
        if role == "You":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)

    # Chat Input Box
    if prompt := st.chat_input("Ask about your savings or financial strategy..."):
        st.session_state.chat_history.append(("You", prompt))

        # Re-construct context for LLM
        full_prompt = (
            f"Context: {ctx}. User asks: {prompt}. Answer as a financial expert."
        )
        with st.spinner("Thinking..."):
            response = get_llm_response(full_prompt)
            st.session_state.chat_history.append(("AI", response))
        st.rerun()

    # Chart
    st.markdown("---")
    st.subheader("📈 Potential Savings Breakdown")
    chart_df = pd.DataFrame(
        {"Category Savings": st.session_state.preds_user}, index=CATEGORIES
    )
    st.bar_chart(chart_df)
