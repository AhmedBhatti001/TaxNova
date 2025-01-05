import streamlit as st
import requests
import matplotlib.pyplot as plt

def set_styles():
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

def input_income():
    st.markdown('<h2 class="header">📄 Enter Your Income Details</h2>', unsafe_allow_html=True)
    salary_income = st.number_input("Basic Salary (in PKR):", min_value=0, value=0, step=1000)
    bonuses_commissions = st.number_input("Bonuses and Commissions (in PKR):", min_value=0, value=0, step=1000)
    gratuity = st.number_input("Gratuity (in PKR):", min_value=0, value=0, step=1000)
    other_sources = st.number_input("Income from Other Sources (in PKR):", min_value=0, value=0, step=1000)
    return salary_income + bonuses_commissions + gratuity + other_sources

def input_deductions():
    st.markdown('<h2 class="header">📉 Enter Applicable Deductions</h2>', unsafe_allow_html=True)
    donation_amount = st.number_input("Charitable Donations (in PKR):", min_value=0, value=0, step=1000)
    education_expenses = st.number_input("Education Expenses (in PKR):", min_value=0, value=0, step=1000)
    medical_expenses = st.number_input("Medical Expenses (in PKR):", min_value=0, value=0, step=1000)
    return donation_amount + education_expenses + medical_expenses

def input_tax_credits():
    st.markdown('<h2 class="header">💸 Enter Applicable Tax Credits</h2>', unsafe_allow_html=True)
    housing_investment = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
    housing_credit = min(housing_investment * 0.15, 2000000)  # 15% capped at PKR 2,000,000
    rd_expenses = st.number_input("R&D Expenses (in PKR):", min_value=0, value=0, step=1000)
    rd_credit = min(rd_expenses * 0.15, 50000)  # Example cap
    return housing_credit + rd_credit

def calculate_tax(income, deductions, credits):
    taxable_income = max(income - deductions, 0)
    tax_payable_before_credits = taxable_income * 0.10  # Example flat tax rate
    tax_payable_after_credits = max(tax_payable_before_credits - credits, 0)
    return taxable_income, tax_payable_after_credits

def main():
    set_styles()
    st.markdown('<h1 class="header">🏦 TaxNova: Comprehensive Tax App</h1>', unsafe_allow_html=True)
    st.write("This app helps calculate taxes with a detailed breakdown of income sources, deductions, and tax credits.")

    income = input_income()
    deductions = input_deductions()
    credits = input_tax_credits()

    if st.button("📊 Calculate Tax"):
        taxable_income, tax_payable = calculate_tax(income, deductions, credits)
        st.success(f"Your taxable income: PKR {taxable_income}")
        st.success(f"Your estimated tax payable: PKR {tax_payable}")

        breakdown_data = {
            "Total Income": income,
            "Deductions": deductions,
            "Taxable Income": taxable_income,
            "Tax Credits": credits,
            "Tax Payable": tax_payable
        }

        fig, ax = plt.subplots()
        ax.bar(breakdown_data.keys(), breakdown_data.values(), color="#4CAF50")
        ax.set_title("Tax Breakdown")
        ax.set_ylabel("Amount (PKR)")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
