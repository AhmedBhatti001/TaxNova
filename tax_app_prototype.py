import streamlit as st
import requests
import matplotlib.pyplot as plt

# Set custom theme styles using markdown and container formatting
st.markdown(
    """
    <style>
    .income-box {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        background-color: #f9f9f9;
        padding: 10px;
        margin-bottom: 10px;
    }
    .note {
        font-size: 14px;
        color: #555;
    }
    .header {
        color: #4CAF50;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Introduction
st.markdown('<h1 class="header">🏦 TaxNova: Tax Assessment and Guidance App</h1>', unsafe_allow_html=True)
st.write("This app provides an enhanced tax calculation and allows users to provide feedback for continuous improvement.")

# Add a note
st.markdown('<p class="note">*Please enter your yearly income and applicable tax credits in the fields below.</p>', unsafe_allow_html=True)

# Input Form
st.markdown('<h2 class="header">📄 Enter Your Income Details</h2>', unsafe_allow_html=True)

# Salary Income Subcategories
st.markdown('<h3 class="header">Income from Salary</h3>', unsafe_allow_html=True)
salary_income = st.number_input("Salary (in PKR):", min_value=0, value=0, step=1000)
bonuses_commissions = st.number_input("Bonuses and Commissions (in PKR):", min_value=0, value=0, step=1000)

# Tax Credit Categories
st.markdown('<h2 class="header">💸 Enter Applicable Tax Credits</h2>', unsafe_allow_html=True)

# Housing Investment Tax Credit
st.markdown('<h3 class="header">Investment in Housing</h3>', unsafe_allow_html=True)
housing_investment = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
housing_credit = min(housing_investment * 0.15, 2000000)  # 15% capped at PKR 2,000,000

# Foreign Taxes Paid Tax Credit
st.markdown('<h3 class="header">Foreign Taxes Paid</h3>', unsafe_allow_html=True)
foreign_taxes_paid = st.number_input("Foreign Taxes Paid (in PKR):", min_value=0, value=0, step=1000)
foreign_income_tax = salary_income * 0.01  # Assuming 1% of foreign income
foreign_credit = min(foreign_taxes_paid, foreign_income_tax)

# Research and Development Tax Credit
st.markdown('<h3 class="header">Research and Development (R&D)</h3>', unsafe_allow_html=True)
rd_expenses = st.number_input("R&D Expenses (in PKR):", min_value=0, value=0, step=1000)
rd_credit = min(rd_expenses * 0.15, salary_income * 0.05)  # 15% capped at 5% of taxable income

# Renewable Energy Tax Credit
st.markdown('<h3 class="header">Investment in Renewable Energy</h3>', unsafe_allow_html=True)
renewable_investment = st.number_input("Renewable Energy Investment (in PKR):", min_value=0, value=0, step=1000)
renewable_credit = min(renewable_investment * 0.20, 2000000)  # 20% capped at PKR 2,000,000

# Pension Fund Tax Credit
st.markdown('<h3 class="header">Pension Funds</h3>', unsafe_allow_html=True)
pension_contributions = st.number_input("Pension Fund Contributions (in PKR):", min_value=0, value=0, step=1000)
age = st.number_input("Your Age (in years):", min_value=0, value=30, step=1)
pension_credit_rate = 0.30 if age >= 50 else 0.20
pension_credit = min(pension_contributions * pension_credit_rate, salary_income * pension_credit_rate)

# Tax Calculation
if st.button("📊 Calculate Tax"):
    total_income = salary_income + bonuses_commissions

    # Total Tax Credits
    total_credits = housing_credit + foreign_credit + rd_credit + renewable_credit + pension_credit

    # Taxable Income and Tax Payable
    taxable_income = max(total_income - total_credits, 0)
    tax_payable = taxable_income * 0.10  # Simplified example tax rate

    # Display Results
    st.success(f"Your total income: PKR {total_income}")
    st.success(f"Your total tax credits: PKR {total_credits}")
    st.success(f"Your taxable income after credits: PKR {taxable_income}")
    st.success(f"Your estimated tax payable: PKR {tax_payable}")

# Feedback Section
st.header("📝 Feedback")
feedback = st.text_area("Is anything missing or needed to calculate? Provide your feedback below:")
if st.button("Submit Feedback"):
    if feedback:
        # Log feedback to a file
        with open("feedback_log.txt", "a") as file:
            file.write(f"{feedback}\n")
        st.success("Thank you for your feedback! It has been saved for review.")
    else:
        st.warning("Please enter feedback before submitting.")

# Sidebar
with st.sidebar:
    st.header("🛠️ Settings")
    theme_toggle = st.checkbox("Enable Dark Mode")
    st.write("Customize your app appearance and settings.")
