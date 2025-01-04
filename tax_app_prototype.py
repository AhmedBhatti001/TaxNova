import streamlit as st
import requests
import matplotlib.pyplot as plt

# Title and Introduction
st.markdown("# 🏦 TaxNova: Tax Assessment and Guidance App")
st.write("This app provides an enhanced tax calculation and allows users to provide feedback for continuous improvement.")

# Input Form
st.header("📄 Enter Your Income Details")

# Organize Inputs into Columns
col1, col2 = st.columns(2)
with col1:
    st.subheader("💰 Salary Income")
    salary_income = st.number_input("Enter Salary Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

    st.subheader("📈 Dividend Income")
    dividend_income = st.number_input("Enter Dividend Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

    st.subheader("💵 Profit on Debt")
    profit_on_debt = st.number_input("Enter Profit on Debt (in PKR):", min_value=0.0, value=0.0, step=1000.0)

with col2:
    st.subheader("📊 Sukuk Investments")
    sukuk_income = st.number_input("Enter Sukuk Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

    st.subheader("🏠 Income from Property")
    property_income = st.number_input("Enter Property Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

    st.subheader("🎉 Prizes and Winnings")
    prizes_winnings = st.number_input("Enter Prizes and Winnings (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Custom Income Sources
st.subheader("➕ Add Custom Income Sources")
custom_sources = []
custom_income = st.text_input("Custom Income Source Name:")
custom_amount = st.number_input("Amount (in PKR) for Custom Source:", min_value=0.0, value=0.0, step=1000.0)
custom_tax_rate = st.number_input("Tax Rate (%) for Custom Source:", min_value=0.0, value=0.0, step=1.0)

if st.button("Add Custom Source"):
    if custom_income and custom_amount > 0 and custom_tax_rate > 0:
        custom_sources.append({"source": custom_income, "amount": custom_amount, "tax_rate": custom_tax_rate})
        st.success(f"Added {custom_income} with amount {custom_amount} PKR and tax rate {custom_tax_rate}%.")

# Display Added Custom Sources
if custom_sources:
    st.write("### Custom Income Sources")
    for idx, source in enumerate(custom_sources):
        st.write(f"{idx+1}. {source['source']} - Amount: PKR {source['amount']}, Tax Rate: {source['tax_rate']}%")

# Tax Calculation
if st.button("📊 Calculate Tax"):
    total_income = (
        salary_income + dividend_income + profit_on_debt + sukuk_income + 
        property_income + prizes_winnings
    )
    total_custom_tax = 0

    for source in custom_sources:
        total_income += source['amount']
        total_custom_tax += (source['amount'] * source['tax_rate'] / 100)

    taxable_income = max(total_income, 0)
    tax = total_custom_tax
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

    # Dividend Income
    if dividend_income > 0:
        tax += dividend_income * 0.15
        tax_breakdown.append(f"Dividend Income: 15% on PKR {dividend_income}")

    # Profit on Debt
    if profit_on_debt > 0:
        tax += profit_on_debt * 0.15
        tax_breakdown.append(f"Profit on Debt: 15% on PKR {profit_on_debt}")

    # Sukuk Investments
    if sukuk_income > 0:
        tax += sukuk_income * 0.1
        tax_breakdown.append(f"Sukuk Income: 10% on PKR {sukuk_income}")

    # Property Income
    if property_income > 0:
        if property_income <= 300000:
            tax_breakdown.append("Property Income: Tax-Free")
        elif property_income <= 600000:
            tax += (property_income - 300000) * 0.05
            tax_breakdown.append(f"Property Income: 5% on PKR {property_income - 300000}")
        elif property_income <= 2000000:
            tax += 15000 + (property_income - 600000) * 0.1
            tax_breakdown.append(f"Property Income: PKR 15,000 + 10% on PKR {property_income - 600000}")
        else:
            tax += 155000 + (property_income - 2000000) * 0.25
            tax_breakdown.append(f"Property Income: PKR 155,000 + 25% on PKR {property_income - 2000000}")

    # Prizes and Winnings
    if prizes_winnings > 0:
        tax += prizes_winnings * 0.2
        tax_breakdown.append(f"Prizes and Winnings: 20% on PKR {prizes_winnings}")

    # Display Results
    st.success(f"Your total income: PKR {total_income}")
    st.success(f"Your estimated tax: PKR {tax}")

    # Visualize Tax Breakdown
    breakdown_data = {
        "Salary": salary_income, "Dividend": dividend_income,
        "Debt": profit_on_debt, "Sukuk": sukuk_income,
        "Property": property_income, "Winnings": prizes_winnings
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
