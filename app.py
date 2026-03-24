import streamlit as st
from groq import Groq
import matplotlib.pyplot as plt

client = Groq(api_key="YOUR_API_KEY")  

st.set_page_config(page_title="AI Money Mentor", layout="wide")

st.title("💰 AI Money Mentor")
st.caption("AI-powered financial assistant for Indian youth 🇮🇳")

# Chat history storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Budget Planner", "💰 Investment Advisor", "💬 AI Chat"])

# ---------------- TAB 1 ----------------
with tab1:
    st.header("📊 Budget Planner")

    income = st.number_input("Monthly Income (₹)")
    expenses = st.number_input("Monthly Expenses (₹)")
    goal = st.number_input("🎯 Your Target Savings Goal (₹)")
    st.caption("Example: 100000 for laptop, emergency fund, etc.")

    if st.button("Generate Plan"):
        if income > 0 and expenses > 0 and goal > 0:
            savings = income - expenses

            st.success(f"💰 Monthly Savings: ₹{savings}")

            # Financial Health
            if savings > income * 0.3:
                st.success("🟢 Excellent financial health")
            elif savings > 0:
                st.warning("🟡 Moderate savings")
            else:
                st.error("🔴 High risk: Expenses exceed income")

            # Goal Progress
            if savings > 0:
                months = goal / savings
                st.info(f"🎯 Goal achievable in {int(months)} months")

            st.divider()

            prompt = f"""
            Give SHORT financial advice.

            Income: ₹{income}
            Expenses: ₹{expenses}
            Goal: ₹{goal}

            Format:
            1. Savings advice
            2. Investment split
            3. Tips (3 points max)
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.markdown("### 🤖 AI Advice")
                st.write(response.choices[0].message.content)

            except:
                st.warning("⚠️ Showing basic plan")
                sip = savings * 0.5
                st.write(f"💡 SIP: ₹{sip}")
                st.write("💡 70% Equity, 30% Debt")
                st.write("💡 Emergency fund first")

            st.info("💡 Tip: Track expenses daily")

        else:
            st.warning("⚠️ Fill all details")

# ---------------- TAB 2 ----------------
with tab2:
    st.header("💰 Investment Advisor")

    invest_amount = st.number_input("Monthly Investment Amount (₹)")

    if st.button("Get Investment Advice"):
        if invest_amount > 0:

            prompt = f"""
            You are a financial advisor.

            Monthly Investment: ₹{invest_amount}

            Give:
            1. Allocation (₹ breakup)
            2. Where to invest (max 3 options)
            3. Tips (max 3)

            Keep it short and clean.
            """

            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )

                st.markdown("### 📈 Investment Plan")
                st.write(response.choices[0].message.content)

            except:
                st.warning("⚠️ Showing basic advice")
                st.write("💡 Nifty 50 Index Fund")
                st.write("💡 SIP in Mutual Funds")
                st.write("💡 Gold / FD")

            st.divider()

            # Donut Chart 🍩
            equity = invest_amount * 0.6
            debt = invest_amount * 0.3
            gold = invest_amount * 0.1

            fig, ax = plt.subplots(figsize=(4,4))

            values = [equity, debt, gold]
            labels = ["Equity", "Debt", "Gold"]

            ax.pie(
                values,
                labels=labels,
                autopct=lambda p: f'₹{int(p/100*invest_amount)}',
                startangle=90,
                wedgeprops={'width': 0.35},
                textprops={'color': 'white'}
            )

            ax.axis('equal')

            # remove white background
            fig.patch.set_alpha(0)
            ax.set_facecolor('none')

            st.markdown("### 📊 Investment Distribution")
            st.divider()

            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.pyplot(fig)

        else:
            st.warning("⚠️ Enter valid amount")

# ---------------- TAB 3 ----------------
with tab3:
    st.header("💬 AI Money Mentor Chat")

    user_query = st.text_input("Ask your financial question")

    if st.button("Ask AI"):
        if user_query != "":
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": user_query}]
                )

                reply = response.choices[0].message.content

            except:
                reply = "⚠️ Basic advice: Focus on saving and investing"

            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("AI", reply))

        else:
            st.warning("⚠️ Enter a question")

    st.divider()

    st.markdown("### 🧠 Chat History")
    for sender, msg in st.session_state.chat_history:
        st.write(f"**{sender}:** {msg}")