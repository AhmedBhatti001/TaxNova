import streamlit as st
import requests

# Title and Introduction
st.title("TaxNova: Tax Assessment and Guidance App")
st.write("This app provides an enhanced tax calculation and AI-driven Q&A for tax-related queries.")

# Input Form
st.header("Enter Your Income Details")
salary_income = st.number_input("Salary Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
business_income = st.number_input("Business Income (in PKR):", min_value=0.0, value=0.0, step=1000.0)
exemptions = st.number_input("Exemptions (in PKR):", min_value=0.0, value=0.0, step=1000.0)

if st.button("Calculate Tax"):
    # Enhanced Tax Calculation Logic
    total_income = salary_income + business_income
    taxable_income = max(total_income - exemptions, 0)
    tax = 0
    tax_breakdown = ""

    if taxable_income <= 600000:
        tax = 0
        tax_breakdown = "Income below PKR 600,000 is tax-free."
    elif taxable_income <= 1200000:
        tax = (taxable_income - 600000) * 0.05
        tax_breakdown = f"5% tax on income above PKR 600,000: PKR {tax}."
    elif taxable_income <= 2400000:
        tax = 30000 + (taxable_income - 1200000) * 0.1
        tax_breakdown = ("PKR 30,000 for the first PKR 1,200,000 plus 10% on income "
                         f"above PKR 1,200,000: PKR {tax - 30000}.")
    else:
        tax = 150000 + (taxable_income - 2400000) * 0.2
        tax_breakdown = ("PKR 150,000 for the first PKR 2,400,000 plus 20% on income "
                         f"above PKR 2,400,000: PKR {tax - 150000}.")

    st.write(f"Your total income: PKR {total_income}")
    st.write(f"Your taxable income: PKR {taxable_income}")
    st.write(f"Your estimated tax: PKR {tax}")
    st.write("Breakdown:", tax_breakdown)

# Display Tax Slabs
st.header("Tax Slabs")
st.table([
    {"Income Range": "Up to PKR 600,000", "Tax Rate": "0%"},
    {"Income Range": "PKR 600,001 - 1,200,000", "Tax Rate": "5%"},
    {"Income Range": "PKR 1,200,001 - 2,400,000", "Tax Rate": "10%"},
    {"Income Range": "Above PKR 2,400,000", "Tax Rate": "20%"},
])

# Q&A Section
st.header("Ask AI About Taxes")
user_query = st.text_input("Enter your tax-related question:")
if st.button("Get Answer"):
    # Call Hugging Face API (replace with your API details)
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased"
    headers = {"Authorization": "Bearer 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"}
    payload = {"inputs": user_query}

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        st.write("Answer:", result.get('generated_text', 'Sorry, no answer available.'))
    except Exception as e:
        st.write("Error connecting to AI service:", e)

# Placeholder for Future Additions
st.sidebar.title("Future Additions")
st.sidebar.write("1. Advanced tax exemptions.")
st.sidebar.write("2. Multi-language support.")
st.sidebar.write("3. RAG-based guidance.")
st.sidebar.write("4. Integration with official tax portals.")
