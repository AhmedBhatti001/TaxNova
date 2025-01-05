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
salary_income = st.number_input("Salary Income (in PKR):", min_value=0, value=0, step=1000)
business_income = st.number_input("Business Income (in PKR):", min_value=0, value=0, step=1000)
property_income = st.number_input("Property Income (in PKR):", min_value=0, value=0, step=1000)
capital_gains = st.number_input("Capital Gains (in PKR):", min_value=0, value=0, step=1000)
other_income = st.number_input("Other Sources (in PKR):", min_value=0, value=0, step=1000)
foreign_income = st.number_input("Foreign Income (in PKR):", min_value=0, value=0, step=1000)

# Deductions
st.markdown('<h2 class="header">📉 Enter Applicable Deductions</h2>', unsafe_allow_html=True)
donation_amount = st.number_input("Charitable Donations (in PKR):", min_value=0, value=0, step=1000)
education_expenses = st.number_input("Education Expenses (in PKR):", min_value=0, value=0, step=1000)
medical_expenses = st.number_input("Medical Expenses (in PKR):", min_value=0, value=0, step=1000)
zakat_paid = st.number_input("Zakat Contributions (in PKR):", min_value=0, value=0, step=1000)
housing_loan_interest = st.number_input("Housing Loan Interest (in PKR):", min_value=0, value=0, step=1000)

# Tax Credits
st.markdown('<h2 class="header">💸 Enter Applicable Tax Credits</h2>', unsafe_allow_html=True)
housing_investment = st.number_input("Investment in Housing (in PKR):", min_value=0, value=0, step=1000)
housing_credit = min(housing_investment * 0.15, 2000000)  # 15% capped at PKR 2,000,000
foreign_taxes_paid = st.number_input("Foreign Taxes Paid (in PKR):", min_value=0, value=0, step=1000)
foreign_credit = min(foreign_taxes_paid, foreign_income * 0.01)  # Assuming 1% of foreign income
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
        salary_income + business_income + property_income +
        capital_gains + other_income + foreign_income
    )

    # Total Deductions
    total_deductions = (
        donation_amount + education_expenses + medical_expenses + zakat_paid + housing_loan_interest
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
    st.success(f"Your taxable income after deductions: PKR {taxable_income}")
    st.success(f"Your total tax credits: PKR {total_credits}")
    st.success(f"Your estimated tax payable: PKR {tax_payable_after_credits}")

    # Visualize Tax Breakdown
    breakdown_data = {
        "Total Income": total_income,
        "Deductions": total_deductions,
        "Taxable Income After Deductions": taxable_income,
        "Tax Credits": total_credits,
        "Tax Payable": tax_payable_after_credits
    }

    fig, ax = plt.subplots()
    ax.bar(breakdown_data.keys(), breakdown_data.values(), color="#4CAF50")
    ax.set_title("Tax Breakdown")
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
