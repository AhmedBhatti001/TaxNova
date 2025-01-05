import streamlit as st
import matplotlib.pyplot as plt

def set_styles():
    st.markdown(
        """
        <style>
        .header {
            color: #4CAF50;
            font-size: 24px;
            margin-bottom: 20px;
        }
        .note {
            font-size: 14px;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def select_categories():
    st.markdown('<h2 class="header">Select Categories</h2>', unsafe_allow_html=True)
    income_categories = st.multiselect("Select Income Sources:", [
        "Salary", "Bonuses", "Gratuity", "Leave Encashment", "Perquisites", "Benefits in Kind", 
        "Sole Proprietorship Income", "Partnership Income", "Corporate Income", "Manufacturing Income", 
        "Rental Income from Residential", "Rental Income from Commercial", "Gains on Real Estate", 
        "Gains on Stocks", "Gains on Bonds", "Other Income", "Foreign Income"
    ])
    deduction_categories = st.multiselect("Select Deductions:", [
        "Charitable Donations", "Education Expenses", "Medical Expenses", "Zakat Contributions", 
        "Housing Loan Interest", "Depreciation", "Advertising Costs", "Employee Contributions", 
        "Business-Specific Deductions"
    ])
    credit_categories = st.multiselect("Select Tax Credits:", [
        "Investment in Housing", "Foreign Taxes Paid", "R&D Expenses", "Renewable Energy Investment", 
        "Pension Contributions", "Education Loans", "Disabled Persons", "Women Entrepreneurs", 
        "IT and Startups", "Green Investments", "Welfare Projects"
    ])
    return income_categories, deduction_categories, credit_categories

def input_income(selected):
    st.markdown('<h3 class="header">Income Details</h3>', unsafe_allow_html=True)
    income_total = 0
    for category in selected:
        value = st.number_input(f"Enter amount for {category} (in PKR):", min_value=0, value=0, step=1000)
        income_total += value
    return income_total

def input_deductions(selected):
    st.markdown('<h3 class="header">Deductions Details</h3>', unsafe_allow_html=True)
    deductions_total = 0
    for category in selected:
        value = st.number_input(f"Enter amount for {category} (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += value
    return deductions_total

def input_tax_credits(selected):
    st.markdown('<h3 class="header">Tax Credits Details</h3>', unsafe_allow_html=True)
    credits_total = 0
    for category in selected:
        if category == "Investment in Housing":
            investment = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
            credit = min(investment * 0.15, 2000000)  # 15% capped at PKR 2,000,000
        elif category == "Foreign Taxes Paid":
            foreign_taxes = st.number_input("Foreign Taxes Paid (in PKR):", min_value=0, value=0, step=1000)
            foreign_income_tax = st.number_input("Foreign Income Taxable (in PKR):", min_value=0, value=0, step=1000)
            credit = min(foreign_taxes, foreign_income_tax)
        elif category == "R&D Expenses":
            rd_expenses = st.number_input("R&D Expenses (in PKR):", min_value=0, value=0, step=1000)
            credit = min(rd_expenses * 0.15, 50000)  # Example cap
        else:
            credit = st.number_input(f"Enter credit for {category} (in PKR):", min_value=0, value=0, step=1000)
        credits_total += credit
    return credits_total

def calculate_summary(income, deductions, credits):
    taxable_income = max(income - deductions, 0)
    tax_payable_before_credits = taxable_income * 0.10  # Example flat tax rate
    tax_payable_after_credits = max(tax_payable_before_credits - credits, 0)
    return taxable_income, tax_payable_after_credits

def main():
    set_styles()
    st.markdown('<h1 class="header">🏦 TaxNova: Comprehensive Tax App</h1>', unsafe_allow_html=True)
    st.write("This app calculates your taxes with a detailed breakdown of income sources, deductions, and tax credits.")

    income_categories, deduction_categories, credit_categories = select_categories()

    st.markdown('<h2 class="header">Selected Categories</h2>', unsafe_allow_html=True)
    st.write(f"### Income Sources: {income_categories}")
    st.write(f"### Deductions: {deduction_categories}")
    st.write(f"### Tax Credits: {credit_categories}")

    income_total = input_income(income_categories)
    deductions_total = input_deductions(deduction_categories)
    credits_total = input_tax_credits(credit_categories)

    if st.button("📊 Calculate Tax"):
        taxable_income, tax_payable = calculate_summary(income_total, deductions_total, credits_total)
        st.success(f"Your taxable income: PKR {taxable_income}")
        st.success(f"Your estimated tax payable: PKR {tax_payable}")

        breakdown_data = {
            "Total Income": income_total,
            "Deductions": deductions_total,
            "Taxable Income": taxable_income,
            "Tax Credits": credits_total,
            "Tax Payable": tax_payable
        }

        fig, ax = plt.subplots()
        ax.bar(breakdown_data.keys(), breakdown_data.values(), color="#4CAF50")
        ax.set_title("Tax Breakdown")
        ax.set_ylabel("Amount (PKR)")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
