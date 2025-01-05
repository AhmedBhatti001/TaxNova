import streamlit as st
import matplotlib.pyplot as plt

# Set styles for the app
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

# Dropdown for categories and subcategories
def select_categories():
    st.markdown('<h2 class="header">Select Categories</h2>', unsafe_allow_html=True)
    income_categories = st.multiselect("Select Income Sources:", [
        "Salary", "Bonuses and Commissions", "Gratuity", "Leave Encashment", "Perquisites", "Benefits in Kind",
        "Sole Proprietorship Income", "Partnership Income", "Corporate Business Income", "Profits from Manufacturing",
        "Rental Income from Residential", "Rental Income from Commercial", "Gains on Real Estate", "Gains on Stocks",
        "Interest Income", "Dividend Income", "Royalty Income", "Prize Money", "Foreign Income"
    ])
    deduction_categories = st.multiselect("Select Deductions:", [
        "Charitable Donations", "Education Expenses", "Medical Expenses", "Zakat Contributions",
        "Housing Loan Interest", "Depreciation", "Employee Contributions", "Business-Specific Deductions"
    ])
    credit_categories = st.multiselect("Select Tax Credits:", [
        "Investment in Housing", "Foreign Taxes Paid", "R&D Expenses", "Renewable Energy Investment",
        "Pension Contributions", "Education Loans", "Disabled Persons", "Women Entrepreneurs",
        "IT and Startups", "Green Investments", "Welfare Projects"
    ])
    return income_categories, deduction_categories, credit_categories

# Input for income sources
def input_income(selected):
    st.markdown('<h3 class="header">Income Details</h3>', unsafe_allow_html=True)
    income_total = 0
    for category in selected:
        value = st.number_input(f"Enter amount for {category} (in PKR):", min_value=0, value=0, step=1000)
        income_total += value
    if st.checkbox("Add Custom Income Source"):
        custom_name = st.text_input("Custom Income Source Name:")
        custom_amount = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
        income_total += custom_amount
    return income_total

# Input for deductions
def input_deductions(selected):
    st.markdown('<h3 class="header">Deductions Details</h3>', unsafe_allow_html=True)
    deductions_total = 0
    for category in selected:
        value = st.number_input(f"Enter amount for {category} (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += value
    if st.checkbox("Add Custom Deduction"):
        custom_name = st.text_input("Custom Deduction Name:")
        custom_amount = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += custom_amount
    return deductions_total

# Input for tax credits
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
    if st.checkbox("Add Custom Tax Credit"):
        custom_name = st.text_input("Custom Tax Credit Name:")
        custom_amount = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
        credits_total += custom_amount
    return credits_total

# Calculate taxable income and tax

def calculate_summary(income, deductions, credits):
    taxable_income = max(income - deductions, 0)
    tax_payable_before_credits = taxable_income * 0.10  # Example flat tax rate
    tax_payable_after_credits = max(tax_payable_before_credits - credits, 0)
    return taxable_income, tax_payable_after_credits

# Main function
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
