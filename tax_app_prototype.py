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
        "Salary", "Bonuses", "Gratuity", "Business Income", "Property Income", "Capital Gains", "Other Income", "Foreign Income"
    ])
    deduction_categories = st.multiselect("Select Deductions:", [
        "Charitable Donations", "Education Expenses", "Medical Expenses", "Zakat Contributions", "Housing Loan Interest", "Business Deductions"
    ])
    credit_categories = st.multiselect("Select Tax Credits:", [
        "Investment in Housing", "Foreign Taxes Paid", "R&D Expenses", "Renewable Energy Investment", "Pension Contributions"
    ])
    return income_categories, deduction_categories, credit_categories

def input_income(selected):
    st.markdown('<h3 class="header">Income Details</h3>', unsafe_allow_html=True)
    income_total = 0
    if "Salary" in selected:
        salary = st.number_input("Basic Salary (in PKR):", min_value=0, value=0, step=1000)
        income_total += salary
    if "Bonuses" in selected:
        bonuses = st.number_input("Bonuses and Commissions (in PKR):", min_value=0, value=0, step=1000)
        income_total += bonuses
    if "Gratuity" in selected:
        gratuity = st.number_input("Gratuity (in PKR):", min_value=0, value=0, step=1000)
        income_total += gratuity
    # Add similar inputs for other selected income categories
    return income_total

def input_deductions(selected):
    st.markdown('<h3 class="header">Deductions Details</h3>', unsafe_allow_html=True)
    deductions_total = 0
    if "Charitable Donations" in selected:
        donations = st.number_input("Charitable Donations (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += donations
    if "Education Expenses" in selected:
        education = st.number_input("Education Expenses (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += education
    if "Medical Expenses" in selected:
        medical = st.number_input("Medical Expenses (in PKR):", min_value=0, value=0, step=1000)
        deductions_total += medical
    # Add similar inputs for other selected deductions
    return deductions_total

def input_tax_credits(selected):
    st.markdown('<h3 class="header">Tax Credits Details</h3>', unsafe_allow_html=True)
    credits_total = 0
    if "Investment in Housing" in selected:
        housing = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
        housing_credit = min(housing * 0.15, 2000000)  # 15% capped at PKR 2,000,000
        credits_total += housing_credit
    if "Foreign Taxes Paid" in selected:
        foreign_taxes = st.number_input("Foreign Taxes Paid (in PKR):", min_value=0, value=0, step=1000)
        foreign_income_tax = st.number_input("Foreign Income Taxable (in PKR):", min_value=0, value=0, step=1000)
        foreign_credit = min(foreign_taxes, foreign_income_tax)
        credits_total += foreign_credit
    if "R&D Expenses" in selected:
        rd_expenses = st.number_input("R&D Expenses (in PKR):", min_value=0, value=0, step=1000)
        rd_credit = min(rd_expenses * 0.15, 50000)  # Example cap
        credits_total += rd_credit
    # Add similar inputs for other selected credits
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
