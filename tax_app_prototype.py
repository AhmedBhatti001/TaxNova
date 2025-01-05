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

# Initialize session state for selected items if not already initialized
if "selected_items" not in st.session_state:
    st.session_state["selected_items"] = {
        "Income Sources": [],
        "Deductions": [],
        "Tax Credits": []
    }

def calculate_salary_tax(income):
    slabs = [
        {"limit": 600000, "rate": 0},
        {"limit": 1200000, "rate": 0.05, "base_tax": 0},
        {"limit": 2200000, "rate": 0.15, "base_tax": 30000},
        {"limit": 3200000, "rate": 0.25, "base_tax": 180000},
        {"limit": 4100000, "rate": 0.30, "base_tax": 430000},
        {"limit": float("inf"), "rate": 0.35, "base_tax": 700000}
    ]
    for slab in slabs:
        if income <= slab["limit"]:
            previous_limit = slabs[slabs.index(slab) - 1]["limit"] if slabs.index(slab) > 0 else 0
            return slab.get("base_tax", 0) + (income - previous_limit) * slab["rate"]

def calculate_business_tax(income, business_type):
    if business_type == "Corporate":
        return income * 0.29  # Flat 29% tax rate
    elif business_type == "Small Company":
        return income * 0.20  # Flat 20% tax rate
    else:  # Sole proprietorship or partnerships
        return calculate_salary_tax(income)

def calculate_capital_gains_tax(income, holding_period):
    if holding_period <= 1:
        return income * 0.10
    elif holding_period <= 2:
        return income * 0.075
    elif holding_period <= 3:
        return income * 0.05
    else:
        return 0

def hierarchical_menu():
    st.markdown('<h2 class="header">Select Categories</h2>', unsafe_allow_html=True)

    selected_main_category = st.selectbox("Select Main Category:", [
        "Income Sources", "Deductions", "Tax Credits"
    ])

    if selected_main_category == "Income Sources":
        income_main_categories = st.selectbox("Select Income Type:", [
            "Salary", "Income from Business", "Income from Property", "Capital Gains", 
            "Income from Other Sources", "Foreign Income", "Custom Input"
        ])
        if income_main_categories == "Salary":
            salary_income = st.number_input("Enter Total Salary Income (in PKR):", min_value=0, value=0, step=1000)
            if st.button("Add Salary Income"):
                tax = calculate_salary_tax(salary_income)
                st.session_state["selected_items"]["Income Sources"].append(("Salary", salary_income, tax))
        elif income_main_categories == "Income from Business":
            business_income = st.number_input("Enter Business Income (in PKR):", min_value=0, value=0, step=1000)
            business_type = st.selectbox("Select Business Type:", ["Corporate", "Small Company", "Sole Proprietorship"])
            if st.button("Add Business Income"):
                tax = calculate_business_tax(business_income, business_type)
                st.session_state["selected_items"]["Income Sources"].append(("Business", business_income, tax))
        elif income_main_categories == "Capital Gains":
            gains_income = st.number_input("Enter Capital Gains (in PKR):", min_value=0, value=0, step=1000)
            holding_period = st.number_input("Enter Holding Period (in years):", min_value=0, value=1, step=1)
            if st.button("Add Capital Gains"):
                tax = calculate_capital_gains_tax(gains_income, holding_period)
                st.session_state["selected_items"]["Income Sources"].append(("Capital Gains", gains_income, tax))

# Calculate taxes
def calculate_tax():
    total_income = sum(value for _, value, _ in st.session_state["selected_items"]["Income Sources"])
    total_deductions = sum(value for _, value in st.session_state["selected_items"]["Deductions"])
    total_credits = sum(value for _, value in st.session_state["selected_items"]["Tax Credits"])

    taxable_income = max(total_income - total_deductions, 0)
    tax_payable_before_credits = sum(tax for _, _, tax in st.session_state["selected_items"]["Income Sources"])
    final_tax = max(tax_payable_before_credits - total_credits, 0)

    return total_income, total_deductions, total_credits, taxable_income, final_tax

# Main function
def main():
    set_styles()
    st.markdown('<h1 class="header">🏦 TaxNova: Comprehensive Tax App</h1>', unsafe_allow_html=True)
    st.write("This app calculates your taxes with a detailed breakdown of income sources, deductions, and tax credits.")

    hierarchical_menu()

    st.markdown('<h2 class="header">Selected Items Summary</h2>', unsafe_allow_html=True)
    st.write("### Income Sources:")
    for item, value, tax in st.session_state["selected_items"]["Income Sources"]:
        st.write(f"- {item}: PKR {value} | Tax: PKR {tax}")

    st.write("### Deductions:")
    for item, value in st.session_state["selected_items"]["Deductions"]:
        st.write(f"- {item}: PKR {value}")

    st.write("### Tax Credits:")
    for item, value in st.session_state["selected_items"]["Tax Credits"]:
        st.write(f"- {item}: PKR {value}")

    if st.button("📊 Calculate Tax"):
        total_income, total_deductions, total_credits, taxable_income, final_tax = calculate_tax()

        st.markdown('<h2 class="header">Tax Calculation Summary</h2>', unsafe_allow_html=True)
        st.write(f"**Total Income:** PKR {total_income}")
        st.write(f"**Total Deductions:** PKR {total_deductions}")
        st.write(f"**Total Tax Credits:** PKR {total_credits}")
        st.write(f"**Taxable Income:** PKR {taxable_income}")
        st.write(f"**Final Tax Payable:** PKR {final_tax}")

if __name__ == "__main__":
    main()
