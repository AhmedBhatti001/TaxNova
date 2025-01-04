import streamlit as st
import requests
import matplotlib.pyplot as plt

# Title and Introduction
st.markdown("# 🏦 TaxNova: Tax Assessment and Guidance App")
st.write("This app provides an enhanced tax calculation and allows users to provide feedback for continuous improvement.")

# Input Form
st.header("📄 Enter Your Income Details")

# Dropdown menus for main headings
income_type = st.selectbox("Select Income Type:", [
    "Income from Salary",
    "Income from Business",
    "Foreign Income",
    "Income from Capital Gains",
    "Other Sources"
])

# Variables for calculations
salary_income = 0
business_income = 0
foreign_income = 0
capital_gains_securities = 0
capital_gains_property = 0
sukuk_income = 0
dividend_income = 0
prizes_winnings = 0
profit_on_debt = 0

# Based on the selected type, show relevant inputs
if income_type == "Income from Salary":
    salary_income = st.number_input("Enter Salary Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
elif income_type == "Income from Business":
    business_income = st.number_input("Enter Business Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
elif income_type == "Foreign Income":
    foreign_income = st.number_input("Enter Foreign Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
elif income_type == "Income from Capital Gains":
    capital_type = st.selectbox("Select Capital Gain Type:", ["Securities", "Properties"])
    if capital_type == "Securities":
        capital_gains_securities = st.number_input("Enter Capital Gain from Securities (in PKR):", min_value=0.0, value=0.0, step=1000.0)
    else:
        capital_gains_property = st.number_input("Enter Capital Gain from Properties (in PKR):", min_value=0.0, value=0.0, step=1000.0)
elif income_type == "Other Sources":
    other_source_type = st.selectbox("Select Other Source Type:", ["Sukuk Investments", "Dividend Income", "Prizes and Winnings", "Profit on Debt"])
    if other_source_type == "Sukuk Investments":
        sukuk_income = st.number_input("Enter Sukuk Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
    elif other_source_type == "Dividend Income":
        dividend_income = st.number_input("Enter Dividend Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
    elif other_source_type == "Prizes and Winnings":
        prizes_winnings = st.number_input("Enter Prizes and Winnings (in PKR):", min_value=0.0, value=0.0, step=1000.0)
    elif other_source_type == "Profit on Debt":
        profit_on_debt = st.number_input("Enter Profit on Debt (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Tax Calculation
if st.button("📊 Calculate Tax"):
    total_income = (
        salary_income + business_income + foreign_income + 
        capital_gains_securities + capital_gains_property + sukuk_income +
        dividend_income + prizes_winnings + profit_on_debt
    )
    tax = 0
    tax_breakdown = []

    # Salary Income Slabs
    if salary_income > 0:
        if salary_income <= 600000:
            tax_breakdown.append("Salary Income: Tax-Free")
        elif salary_income <= 1200000:
            tax += (salary_income - 600000) * 0.05
            tax_breakdown.append(f"Salary Income: 5% on PKR {salary_income - 600000}")
        elif salary_income <= 2200000:
            tax += 30000 + (salary_income - 1200000) * 0.15
            tax_breakdown.append(f"Salary Income: PKR 30,000 + 15% on PKR {salary_income - 1200000}")
        elif salary_income <= 3200000:
            tax += 180000 + (salary_income - 2200000) * 0.25
            tax_breakdown.append(f"Salary Income: PKR 180,000 + 25% on PKR {salary_income - 2200000}")
        elif salary_income <= 4100000:
            tax += 430000 + (salary_income - 3200000) * 0.3
            tax_breakdown.append(f"Salary Income: PKR 430,000 + 30% on PKR {salary_income - 3200000}")
        else:
            tax += 700000 + (salary_income - 4100000) * 0.35
            tax_breakdown.append(f"Salary Income: PKR 700,000 + 35% on PKR {salary_income - 4100000}")

    # Business Income Slabs
    if business_income > 0:
        if business_income <= 600000:
            tax_breakdown.append("Business Income: Tax-Free")
        elif business_income <= 1200000:
            tax += (business_income - 600000) * 0.05
            tax_breakdown.append(f"Business Income: 5% on PKR {business_income - 600000}")
        elif business_income <= 2200000:
            tax += 30000 + (business_income - 1200000) * 0.15
            tax_breakdown.append(f"Business Income: PKR 30,000 + 15% on PKR {business_income - 1200000}")
        elif business_income <= 3200000:
            tax += 180000 + (business_income - 2200000) * 0.25
            tax_breakdown.append(f"Business Income: PKR 180,000 + 25% on PKR {business_income - 2200000}")
        elif business_income <= 4100000:
            tax += 430000 + (business_income - 3200000) * 0.3
            tax_breakdown.append(f"Business Income: PKR 430,000 + 30% on PKR {business_income - 3200000}")
        else:
            tax += 700000 + (business_income - 4100000) * 0.35
            tax_breakdown.append(f"Business Income: PKR 700,000 + 35% on PKR {business_income - 4100000}")

    # Foreign Income Tax
    if foreign_income > 0:
        tax += foreign_income * 0.01
        tax_breakdown.append(f"Foreign Income: 1% on PKR {foreign_income}")

    # Capital Gains Tax
    if capital_gains_securities > 0:
        tax += capital_gains_securities * 0.125
        tax_breakdown.append(f"Capital Gains (Securities): 12.5% on PKR {capital_gains_securities}")
    if capital_gains_property > 0:
        tax += capital_gains_property * 0.15
        tax_breakdown.append(f"Capital Gains (Properties): 15% on PKR {capital_gains_property}")

    # Other Sources Tax
    if sukuk_income > 0:
        tax += sukuk_income * 0.1
        tax_breakdown.append(f"Sukuk Income: 10% on PKR {sukuk_income}")
    if dividend_income > 0:
        tax += dividend_income * 0.15
        tax_breakdown.append(f"Dividend Income: 15% on PKR {dividend_income}")
    if prizes_winnings > 0:
        tax += prizes_winnings * 0.2
        tax_breakdown.append(f"Prizes and Winnings: 20% on PKR {prizes_winnings}")
    if profit_on_debt > 0:
        tax += profit_on_debt * 0.15
        tax_breakdown.append(f"Profit on Debt: 15% on PKR {profit_on_debt}")

    # Display Results
    st.success(f"Your total income: PKR {total_income}")
    st.success(f"Your estimated tax: PKR {tax}")

    # Visualize Tax Breakdown
    breakdown_data = {
        "Salary": salary_income, "Business": business_income, "Foreign": foreign_income,
        "Cap. Gains (Securities)": capital_gains_securities, "Cap. Gains (Properties)": capital_gains_property,
        "Sukuk": sukuk_income, "Dividend": dividend_income, "Prizes": prizes_winnings,
        "Debt": profit_on_debt
    }

    fig, ax = plt.subplots()
    ax.bar(breakdown_data.keys(), breakdown_data.values())
    ax.set_title("Income Breakdown")
    ax.set_ylabel("Amount (PKR)")
    st.pyplot(fig)

# Feedback Section
st.header("📝 Feedback")
feedback = st.text_area("Is anything missing or needed to calculate? Provide your feedback below:")
if st.button("Submit Feedback"):
    if feedback:
        st.success("Thank you for your feedback! We will use it to improve the system.")
    else:
        st.warning("Please enter feedback before submitting.")

# Sidebar
with st.sidebar:
    st.header("🛠️ Settings")
    theme_toggle = st.checkbox("Enable Dark Mode")
    st.write("Customize your app appearance and settings.")
