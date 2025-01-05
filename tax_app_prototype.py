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
st.markdown('<h1 class="header">🏦 TaxNova: Comprehensive Tax App</h1>', unsafe_allow_html=True)
st.write("This app helps calculate taxes with a detailed breakdown of income sources, deductions, and tax credits.")

# Add a note
st.markdown('<p class="note">*Please enter your yearly income, deductions, and applicable tax credits below.</p>', unsafe_allow_html=True)

# Input Form
st.markdown('<h2 class="header">📄 Enter Your Income Details</h2>', unsafe_allow_html=True)

# Income Sources
st.markdown('<h3 class="header">Income Sources</h3>', unsafe_allow_html=True)
# Salary Income
st.subheader("Salary Income")
salary_income = st.number_input("Basic Salary (in PKR):", min_value=0, value=0, step=1000)
bonuses_commissions = st.number_input("Bonuses and Commissions (in PKR):", min_value=0, value=0, step=1000)
gratuity = st.number_input("Gratuity (in PKR):", min_value=0, value=0, step=1000)
leave_encashment = st.number_input("Leave Encashment (in PKR):", min_value=0, value=0, step=1000)
perquisites = st.number_input("Perquisites (e.g., car allowances, housing) (in PKR):", min_value=0, value=0, step=1000)
benefits_in_kind = st.number_input("Benefits in Kind (in PKR):", min_value=0, value=0, step=1000)

# Business Income
st.subheader("Income from Business")
sole_proprietorship = st.number_input("Sole Proprietorship Income (in PKR):", min_value=0, value=0, step=1000)
partnership_income = st.number_input("Partnership Income (in PKR):", min_value=0, value=0, step=1000)
corporate_income = st.number_input("Corporate Business Income (in PKR):", min_value=0, value=0, step=1000)
manufacturing_income = st.number_input("Profits from Manufacturing, Trading, and Services (in PKR):", min_value=0, value=0, step=1000)
agricultural_income = st.number_input("Agricultural Business Income (in PKR):", min_value=0, value=0, step=1000)
professional_services = st.number_input("Professional Services (e.g., consultancy, freelancing) (in PKR):", min_value=0, value=0, step=1000)

# Property Income
st.subheader("Income from Property")
rental_residential = st.number_input("Rental Income from Residential Properties (in PKR):", min_value=0, value=0, step=1000)
rental_commercial = st.number_input("Rental Income from Commercial Properties (in PKR):", min_value=0, value=0, step=1000)
leasing_income = st.number_input("Leasing Income (in PKR):", min_value=0, value=0, step=1000)
subletting_income = st.number_input("Subletting Income (in PKR):", min_value=0, value=0, step=1000)

# Capital Gains
st.subheader("Capital Gains")
capital_gains_real_estate = st.number_input("Gains on Sale of Real Estate (in PKR):", min_value=0, value=0, step=1000)
capital_gains_stocks = st.number_input("Gains on Sale of Stocks (in PKR):", min_value=0, value=0, step=1000)
capital_gains_bonds = st.number_input("Gains on Sale of Bonds (in PKR):", min_value=0, value=0, step=1000)
capital_gains_mutual_funds = st.number_input("Gains on Sale of Mutual Fund Units (in PKR):", min_value=0, value=0, step=1000)
capital_gains_other = st.number_input("Gains on Sale of Other Investments (in PKR):", min_value=0, value=0, step=1000)

# Other Sources
st.subheader("Income from Other Sources")
interest_income = st.number_input("Interest Income (in PKR):", min_value=0, value=0, step=1000)
dividend_income = st.number_input("Dividend Income (in PKR):", min_value=0, value=0, step=1000)
royalty_income = st.number_input("Royalty Income (in PKR):", min_value=0, value=0, step=1000)
prize_winnings = st.number_input("Prize Money and Lottery Winnings (in PKR):", min_value=0, value=0, step=1000)
pension_income = st.number_input("Pension and Annuities (in PKR):", min_value=0, value=0, step=1000)

# Foreign Income
st.subheader("Foreign Income")
foreign_salaries = st.number_input("Salaries Earned Abroad (in PKR):", min_value=0, value=0, step=1000)
foreign_business = st.number_input("Business Income from Foreign Operations (in PKR):", min_value=0, value=0, step=1000)
foreign_dividends = st.number_input("Dividends and Interest Earned Overseas (in PKR):", min_value=0, value=0, step=1000)
foreign_rental = st.number_input("Foreign Rental Income (in PKR):", min_value=0, value=0, step=1000)

# Deductions
st.markdown('<h2 class="header">📉 Enter Applicable Deductions</h2>', unsafe_allow_html=True)
donation_amount = st.number_input("Charitable Donations (in PKR):", min_value=0, value=0, step=1000)
education_expenses = st.number_input("Education Expenses (in PKR):", min_value=0, value=0, step=1000)
medical_expenses = st.number_input("Medical Expenses (in PKR):", min_value=0, value=0, step=1000)
zakat_paid = st.number_input("Zakat Contributions (in PKR):", min_value=0, value=0, step=1000)
housing_loan_interest = st.number_input("Housing Loan Interest (in PKR):", min_value=0, value=0, step=1000)
depreciation_expenses = st.number_input("Depreciation Expenses (in PKR):", min_value=0, value=0, step=1000)
advertising_expenses = st.number_input("Advertising and Marketing Costs (in PKR):", min_value=0, value=0, step=1000)

# Tax Credits
st.markdown('<h2 class="header">💸 Enter Applicable Tax Credits</h2>', unsafe_allow_html=True)
housing_investment = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
housing_credit = min(housing_investment * 0.15, 2000000)  # 15% capped at PKR 2,000,000
foreign_taxes_paid = st.number_input("Foreign Taxes Paid (in PKR):", min_value=0, value=0, step=1000)
foreign_credit = min(foreign_taxes_paid, foreign_salaries * 0.01)  # Assuming 1% of foreign income
rd_expenses = st.number_input("R&D Expenses (in PKR):", min_value=0, value=0, step=1000)
rd_credit = min(rd_expenses * 0.15, (salary_income + business_income) * 0.05)  # 15% capped at 5% of taxable income
renewable_investment = st.number_input("Renewable Energy Investment (in PKR):", min_value=0, value=0, step=1000)
renewable_credit = min(renewable_investment * 0.20, 2000000)  # 20% capped at PKR 2,000,000
pension_contributions = st.number_input("Pension Fund Contributions (in PKR):", min_value=0, value=0, step=1000)
age = st.number_input("Your Age (in years):", min_value=0, value=30, step=1)
pension_credit_rate = 0.30 if age >= 50 else 0.20
pension_credit = min(pension_contributions * pension_credit_rate, (salary_income + business_income) * pension_credit_rate)

# Tax Calculation
if st.button("📊 Calculate Tax"):
    total_income = (
        salary_income + bonuses_commissions + gratuity + leave_encashment + perquisites + benefits_in_kind +
        sole_proprietorship + partnership_income + corporate_income + manufacturing_income + agricultural_income + professional_services +
        rental_residential + rental_commercial + leasing_income + subletting_income +
        capital_gains_real_estate + capital_gains_stocks + capital_gains_bonds + capital_gains_mutual_funds + capital_gains_other +
        interest_income + dividend_income + royalty_income + prize_winnings + pension_income +
        foreign_salaries + foreign_business + foreign_dividends + foreign_rental
    )

    # Total Deductions
    total_deductions = (
        donation_amount + education_expenses + medical_expenses + zakat_paid + housing_loan_interest +
        depreciation_expenses + advertising_expenses
    )

    # Total Tax Credits
    total_credits = housing_credit + foreign_credit + rd_credit + renewable_credit + pension_credit

    # Taxable Income and Tax Payable
    taxable_income = max(total_income - total_deductions, 0)
    tax_payable_before_credits = taxable_income * 0.10  # Example 10% tax rate
    tax_payable_after_credits = max(tax_payable_before_credits - total_credits, 0)

    # Display Results
    st.success(f"Your total income: PKR {total_income}")
    st.success(f"Your total deductions: PKR {total_deductions}")
    st.success(f"Your taxable income after deductions: PKR {tax
