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
st.markdown('<p class="note">*Please enter your yearly income in the fields below.</p>', unsafe_allow_html=True)

# Input Form
st.markdown('<h2 class="header">📄 Enter Your Income Details</h2>', unsafe_allow_html=True)

# Salary Income Subcategories
st.markdown('<h3 class="header">Income from Salary</h3>', unsafe_allow_html=True)
salary_income = st.number_input("Salary (in PKR):", min_value=0, value=0, step=1000)
bonuses_commissions = st.number_input("Bonuses and Commissions (in PKR):", min_value=0, value=0, step=1000)
gratuity = st.number_input("Gratuity (in PKR):", min_value=0, value=0, step=1000)
leave_encashment = st.number_input("Leave Encashment (in PKR):", min_value=0, value=0, step=1000)
perquisites = st.number_input("Perquisites (e.g., car allowances, housing) (in PKR):", min_value=0, value=0, step=1000)
benefits_in_kind = st.number_input("Benefits in Kind (in PKR):", min_value=0, value=0, step=1000)

# Business Income Subcategories
st.markdown('<h3 class="header">Income from Business</h3>', unsafe_allow_html=True)
sole_proprietorship = st.number_input("Sole Proprietorship Income (in PKR):", min_value=0, value=0, step=1000)
partnership_income = st.number_input("Partnership Income (in PKR):", min_value=0, value=0, step=1000)
corporate_income = st.number_input("Corporate Business Income (in PKR):", min_value=0, value=0, step=1000)
manufacturing_income = st.number_input("Profits from Manufacturing, Trading, and Services (in PKR):", min_value=0, value=0, step=1000)
agricultural_income = st.number_input("Agricultural Business Income (in PKR):", min_value=0, value=0, step=1000)
professional_services = st.number_input("Professional Services (e.g., consultancy, freelancing) (in PKR):", min_value=0, value=0, step=1000)

# Property Income Subcategories
st.markdown('<h3 class="header">Income from Property</h3>', unsafe_allow_html=True)
rental_residential = st.number_input("Rental Income from Residential Properties (in PKR):", min_value=0, value=0, step=1000)
rental_commercial = st.number_input("Rental Income from Commercial Properties (in PKR):", min_value=0, value=0, step=1000)
leasing_income = st.number_input("Leasing Income (in PKR):", min_value=0, value=0, step=1000)
subletting_income = st.number_input("Subletting Income (in PKR):", min_value=0, value=0, step=1000)

# Capital Gains Subcategories
st.markdown('<h3 class="header">Capital Gains</h3>', unsafe_allow_html=True)
gains_real_estate = st.number_input("Gains on Sale of Real Estate (in PKR):", min_value=0, value=0, step=1000)
gains_stocks = st.number_input("Gains on Sale of Stocks (in PKR):", min_value=0, value=0, step=1000)
holding_period_stocks = st.selectbox("Holding Period for Stocks:", ["Up to 1 year", "1 to 2 years", "Over 2 years"])
gains_bonds = st.number_input("Gains on Sale of Bonds (in PKR):", min_value=0, value=0, step=1000)
gains_mutual_funds = st.number_input("Gains on Sale of Mutual Fund Units (in PKR):", min_value=0, value=0, step=1000)
gains_other_investments = st.number_input("Gains on Sale of Other Investments (in PKR):", min_value=0, value=0, step=1000)

# Other Sources Subcategories
st.markdown('<h3 class="header">Income from Other Sources</h3>', unsafe_allow_html=True)
interest_income = st.number_input("Interest Income (in PKR):", min_value=0, value=0, step=1000)
dividend_income_taxable = st.number_input("Dividend Income from Taxable Companies (in PKR):", min_value=0, value=0, step=1000)
dividend_income_exempt = st.number_input("Dividend Income from Tax-Exempt Companies (in PKR):", min_value=0, value=0, step=1000)
royalty_income = st.number_input("Royalty Income (in PKR):", min_value=0, value=0, step=1000)
prize_money = st.number_input("Prize Money and Lottery Winnings (in PKR):", min_value=0, value=0, step=1000)
pension_income = st.number_input("Pension and Annuities (in PKR):", min_value=0, value=0, step=1000)

# Foreign Income Subcategories
st.markdown('<h3 class="header">Foreign Income</h3>', unsafe_allow_html=True)
foreign_salaries = st.number_input("Salaries Earned Abroad (in PKR):", min_value=0, value=0, step=1000)
foreign_business = st.number_input("Business Income from Foreign Operations (in PKR):", min_value=0, value=0, step=1000)
foreign_dividends = st.number_input("Dividends and Interest Earned Overseas (in PKR):", min_value=0, value=0, step=1000)
foreign_rental = st.number_input("Foreign Rental Income (in PKR):", min_value=0, value=0, step=1000)

# Tax Calculation
if st.button("📊 Calculate Tax"):
    total_income = (
        salary_income + bonuses_commissions + gratuity + leave_encashment + perquisites + benefits_in_kind +
        sole_proprietorship + partnership_income + corporate_income + manufacturing_income + agricultural_income + professional_services +
        rental_residential + rental_commercial + leasing_income + subletting_income +
        gains_real_estate + gains_stocks + gains_bonds + gains_mutual_funds + gains_other_investments +
        interest_income + dividend_income_taxable + dividend_income_exempt + royalty_income + prize_money + pension_income +
        foreign_salaries + foreign_business + foreign_dividends + foreign_rental
    )
    tax = 0
    tax_breakdown = []

    # Apply tax slabs for Salary Income
    salary_total = salary_income + bonuses_commissions + gratuity + leave_encashment + perquisites + benefits_in_kind
    if salary_total > 0:
        if salary_total <= 600000:
            tax_breakdown.append("Salary Income: Tax-Free")
        elif salary_total <= 1200000:
            tax += (salary_total - 600000) * 0.05
            tax_breakdown.append(f"Salary Income: 5% on PKR {salary_total - 600000}")
        elif salary_total <= 2200000:
            tax += 30000 + (salary_total - 1200000) * 0.15
            tax_breakdown.append(f"Salary Income: PKR 30,000 + 15% on PKR {salary_total - 1200000}")
        elif salary_total <= 3200000:
            tax += 180000 + (salary_total - 2200000) * 0.25
            tax_breakdown.append(f"Salary Income: PKR 180,000 + 25% on PKR {salary_total - 2200000}")
        elif salary_total <= 4100000:
            tax += 430000 + (salary_total - 3200000) * 0.3
            tax_breakdown.append(f"Salary Income: PKR 430,000 + 30% on PKR {salary_total - 3200000}")
        else:
            tax += 700000 + (salary_total - 4100000) * 0.35
            tax_breakdown.append(f"Salary Income: PKR 700,000 + 35% on PKR {salary_total - 4100000}")

    # Apply tax rate for Foreign Income
    foreign_total = foreign_salaries + foreign_business + foreign_dividends + foreign_rental
    if foreign_total > 0:
        tax += foreign_total * 0.01
        tax_breakdown.append(f"Foreign Income: 1% on PKR {foreign_total}")

    # Add more tax calculations for other income sources based on provided rates
    # For example:
    # - Rental Income slabs
    # - Holding periods for capital gains
    # - Withholding tax for other sources

    # Display Results
    st.success(f"Your total income: PKR {total_income}")
    st.success(f"Your estimated tax: PKR {tax}")

    # Visualize Tax Breakdown
    breakdown_data = {
        "Salary": salary_total,
        "Business": sole_proprietorship + partnership_income + corporate_income + manufacturing_income + agricultural_income + professional_services,
        "Property": rental_residential + rental_commercial + leasing_income + subletting_income,
        "Capital Gains": gains_real_estate + gains_stocks + gains_bonds + gains_mutual_funds + gains_other_investments,
        "Other Sources": interest_income + dividend_income_taxable + dividend_income_exempt + royalty_income + prize_money + pension_income,
        "Foreign Income": foreign_total
    }

    fig, ax = plt.subplots()
    ax.bar(breakdown_data.keys(), breakdown_data.values(), color="#4CAF50")
    ax.set_title("Income Breakdown")
    ax.set_ylabel("Amount (PKR)")
    st.pyplot(fig)

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
