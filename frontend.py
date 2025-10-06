import streamlit as st
import requests
from datetime import datetime
from requests.exceptions import ConnectionError
import pandas as pd
import plotly.express as px

BACKEND_URL = "http://localhost:8000"

# --- Check backend availability ---
def check_backend_connection():
    try:
        response = requests.get(f"{BACKEND_URL}/api/expenses/")
        return response.status_code == 200
    except ConnectionError:
        return False

# --- Run App ---
def run_streamlit_app():
    st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

    # Custom styles
    st.markdown("""
        <style>
        html, body, [class*="css"]  {
            background-color: #1e1e1e;
            color: white !important;
        }
        .stButton > button {
            background-color: #ffd700 !important;
            color: black !important;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.4rem 1.2rem;
            transition: all 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #ffcf33 !important;
            transform: scale(1.02);
        }
        .stSelectbox, .stNumberInput, .stTextInput, .stTextArea {
            background-color: #2a2a2a !important;
            color: white !important;
            border-radius: 6px;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("💰 Expense Tracker")
    st.caption("Minimal | Dark Theme | Full CRUD | Monthly Visual Reports")

    if not check_backend_connection():
        st.error("❌ Could not connect to the backend server at http://localhost:8000")
        st.stop()

    if 'budget' not in st.session_state:
        st.session_state.budget = 1000.0

    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
        st.session_state.edit_id = None
        st.session_state.edit_data = {}

    # Sidebar
    with st.sidebar:
        st.header("🛠️ Budget Settings")
        new_budget = st.number_input("💵 Set your budget (₹)", min_value=0.0, value=st.session_state.budget, step=100.0, format="%.2f")
        if st.button("🔄 Update Budget"):
            st.session_state.budget = new_budget
            st.success(f"✅ Budget updated to ₹{new_budget:.2f}")

        if st.button("🗑️ Reset All Expenses"):
            try:
                response = requests.delete(f"{BACKEND_URL}/api/expenses/reset/")
                if response.status_code == 200:
                    st.success("🧹 All expenses have been reset!")
                else:
                    st.error("⚠️ Failed to reset expenses")
            except ConnectionError:
                st.error("❌ Could not connect to the backend server")

    st.divider()

    # ------------------- Add or Edit Expense -------------------
    st.subheader("📝 Add / Edit Expense")

    with st.form(key="expense_form", clear_on_submit=not st.session_state.edit_mode):
        col1, col2 = st.columns(2)
        with col1:
            product_name = st.text_input("🏦 Product Name", value=st.session_state.edit_data.get("product_name", ""))
        with col2:
            amount = st.number_input("💲 Amount (₹)", min_value=0.01, step=0.01, format="%.2f", value=st.session_state.edit_data.get("amount", 0.01))

        category = st.selectbox("📂 Category", ["Food", "Travel", "Bills", "Shopping", "Others"], index=["Food", "Travel", "Bills", "Shopping", "Others"].index(st.session_state.edit_data.get("category", "Food")))

        submit_button = st.form_submit_button("➕ Update Expense" if st.session_state.edit_mode else "➕ Add Expense")

        if submit_button:
            if not product_name:
                st.error("⚠️ Please enter a product name")
            else:
                expense_data = {
                    "product_name": product_name,
                    "amount": amount,
                    "category": category,
                    "date": datetime.now().isoformat()
                }

                try:
                    if st.session_state.edit_mode:
                        response = requests.put(f"{BACKEND_URL}/api/expenses/{st.session_state.edit_id}/update/", json=expense_data)
                        if response.status_code == 200:
                            st.success("✅ Expense updated successfully!")
                            st.session_state.edit_mode = False
                            st.session_state.edit_data = {}
                            st.experimental_rerun()
                        else:
                            st.error("❌ Failed to update expense")
                    else:
                        response = requests.post(f"{BACKEND_URL}/api/expenses/add/", json=expense_data)
                        if response.status_code == 201:
                            st.success(f"✅ Added: {product_name} - ₹{amount:.2f} ({category})")
                        else:
                            st.error(f"❌ Failed to add expense: {response.text}")
                except ConnectionError:
                    st.error("❌ Could not connect to the backend server")

    st.divider()

    # ------------------- Expense Summary & Visualizations -------------------
    st.subheader("📊 Expense Summary")
    try:
        total_response = requests.get(f"{BACKEND_URL}/api/expenses/total/")
        if total_response.status_code == 200:
            total_expenses = total_response.json().get("total", 0)
            remaining_budget = st.session_state.budget - total_expenses

            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Budget", f"₹{st.session_state.budget:.2f}")
            col2.metric("💸 Total Expenses", f"₹{total_expenses:.2f}")
            col3.metric("📉 Remaining Budget", f"₹{remaining_budget:.2f}", delta=f"-₹{total_expenses:.2f}")

            expenses_response = requests.get(f"{BACKEND_URL}/api/expenses/")
            if expenses_response.status_code == 200:
                expenses = expenses_response.json()
                if expenses:
                    expense_data = []
                    for expense in expenses:
                        try:
                            date = datetime.fromisoformat(expense["date"].replace("Z", "+00:00"))
                        except Exception:
                            date = datetime.now()
                        expense_data.append({
                            "_id": expense.get("_id", ""),
                            "Date": date.strftime("%Y-%m-%d"),
                            "Month-Year": date.strftime("%B-%Y"),
                            "Product": expense.get("product_name", "Unknown"),
                            "Category": expense.get("category", "Others"),
                            "Amount": expense.get("amount", 0.0)
                        })

                    df = pd.DataFrame(expense_data)
                    df["Amount"] = df["Amount"].astype(float)

                    unique_months = df["Month-Year"].unique()
                    selected_month = st.selectbox("📅 Select Month", options=unique_months)

                    filtered_df = df[df["Month-Year"] == selected_month]

                    if not filtered_df.empty:
                        st.dataframe(filtered_df.drop(columns=["_id"]), use_container_width=True)

                        # -- Edit/Delete --
                        with st.expander("🗑️ Manage Expense"):
                            for i, row in filtered_df.iterrows():
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    st.write(f"{row['Product']} - ₹{row['Amount']} ({row['Category']})")
                                with col2:
                                    if st.button("Edit", key=f"edit_{i}"):
                                        st.session_state.edit_mode = True
                                        st.session_state.edit_id = row["_id"]
                                        st.session_state.edit_data = row.to_dict()
                                        st.experimental_rerun()
                                    if st.button("Delete", key=f"delete_{i}"):
                                        try:
                                            delete_response = requests.delete(f"{BACKEND_URL}/api/expenses/{row['_id']}/delete/")
                                            if delete_response.status_code == 200:
                                                st.success("✅ Deleted!")
                                                st.experimental_rerun()
                                            else:
                                                st.error("❌ Deletion failed")
                                        except Exception as e:
                                            st.error(f"❌ Error: {e}")

                        # Charts
                        st.subheader("📈 Visualizations")
                        chart1, chart2, chart3 = st.columns(3)
                        with chart1:
                            st.caption("Line Chart")
                            st.line_chart(data=filtered_df, x="Date", y="Amount", use_container_width=True)
                        with chart2:
                            fig_bar = px.bar(filtered_df, x="Product", y="Amount", color="Product")
                            st.plotly_chart(fig_bar, use_container_width=True)
                        with chart3:
                            fig_pie = px.pie(filtered_df, names="Category", values="Amount", hole=0.3)
                            st.plotly_chart(fig_pie, use_container_width=True)

                    else:
                        st.info("ℹ️ No expenses for selected month.")
                else:
                    st.info("ℹ️ No data available.")
            else:
                st.error("❌ Failed to fetch expenses")
        else:
            st.error("❌ Failed to calculate total expenses")
    except ConnectionError:
        st.error("❌ Could not connect to the backend server")

if __name__ == "__main__":
    run_streamlit_app()
