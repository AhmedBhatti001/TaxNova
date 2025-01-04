import streamlit as st
import requests

# Title and Introduction
st.title("TaxNova: Tax Assessment and Guidance App")
st.write("This app provides an enhanced tax calculation and allows users to provide feedback for continuous improvement.")

# Input Form
st.header("Enter Your Income Details")

# Salary Income
st.subheader("Salary Income")
salary_income = st.number_input("Enter Salary Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Dividend Income
st.subheader("Dividend Income")
dividend_income = st.number_input("Enter Dividend Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Profit on Debt
st.subheader("Profit on Debt")
profit_on_debt = st.number_input("Enter Profit on Debt (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Sukuk Investments
st.subheader("Sukuk Investments")
sukuk_income = st.number_input("Enter Sukuk Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Property Income
st.subheader("Income from Property")
property_income = st.number_input("Enter Property Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Prizes and Winnings
st.subheader("Prizes and Winnings")
prizes_winnings = st.number_input("Enter Prizes and Winnings (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Brokerage and Commission
st.subheader("Brokerage & Commission")
brokerage_commission = st.number_input("Enter Brokerage & Commission Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)

# Custom Income Sources
st.subheader("Add Custom Income Sources")
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

if st.button("Calculate Tax"):
    # Tax Calculation Logic
    total_income = (
        salary_income + dividend_income + profit_on_debt + sukuk_income + 
        property_income + prizes_winnings + brokerage_commission
    )
    total_custom_tax = 0

    # Calculate Tax for Custom Sources
    for source in custom_sources:
        total_income += source['amount']
        total_custom_tax += (source['amount'] * source['tax_rate'] / 100)

    taxable_income = max(total_income, 0)
    tax = total_custom_tax
    tax_breakdown = []

    # Tax Slabs and Rules
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

    # Dividend Income Rules
    if dividend_income > 0:
        tax += dividend_income * 0.15
        tax_breakdown.append(f"Dividend Income: 15% on PKR {dividend_income}")

    # Profit on Debt Rules
    if profit_on_debt > 0:
        tax += profit_on_debt * 0.15
        tax_breakdown.append(f"Profit on Debt: 15% on PKR {profit_on_debt}")

    # Sukuk Investments Rules
    if sukuk_income > 0:
        tax += sukuk_income * 0.1
        tax_breakdown.append(f"Sukuk Income: 10% on PKR {sukuk_income}")

    # Property Income Rules
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

    # Prizes and Winnings Rules
    if prizes_winnings > 0:
        tax += prizes_winnings * 0.2
        tax_breakdown.append(f"Prizes and Winnings: 20% on PKR {prizes_winnings}")

    # Brokerage and Commission Rules
    if brokerage_commission > 0:
        tax += brokerage_commission * 0.1
        tax_breakdown.append(f"Brokerage and Commission: 10% on PKR {brokerage_commission}")

    # Display Results
    st.write(f"Your total income: PKR {total_income}")
    st.write(f"Your estimated tax: PKR {tax}")
    st.write("Breakdown:")
    for line in tax_breakdown:
        st.write(f"- {line}")

# Feedback Section
st.header("Feedback")
feedback = st.text_area("Is anything missing or needed to calculate? Provide your feedback below:")
if st.button("Submit Feedback"):
    if feedback:
        # Here, the feedback could be logged to a database or sent via email
        st.success("Thank you for your feedback! We will use it to improve the system.")
    else:
        st.warning("Please enter feedback before submitting.")

# Placeholder for Future Additions
st.sidebar.title("Future Additions")
st.sidebar.write("1. Advanced tax exemptions.")
st.sidebar.write("2. Multi-language support.")
st.sidebar.write("3. RAG-based guidance.")
st.sidebar.write("4. Integration with official tax portals.")
