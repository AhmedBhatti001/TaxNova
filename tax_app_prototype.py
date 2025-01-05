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

# Ensure each category can add multiple items dynamically without overwriting previous selections
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
            if st.button("Add Salary Income", key="add_salary"):
                tax = calculate_salary_tax(salary_income)
                st.session_state["selected_items"]["Income Sources"].append(("Salary", salary_income, tax))
                st.success("Salary income added successfully.")
        elif income_main_categories == "Income from Business":
            business_income = st.number_input("Enter Business Income (in PKR):", min_value=0, value=0, step=1000)
            business_type = st.selectbox("Select Business Type:", ["Corporate", "Small Company", "Sole Proprietorship"])
            if st.button("Add Business Income", key="add_business"):
                tax = calculate_business_tax(business_income, business_type)
                st.session_state["selected_items"]["Income Sources"].append(("Business", business_income, tax))
                st.success("Business income added successfully.")
        elif income_main_categories == "Capital Gains":
            gains_income = st.number_input("Enter Capital Gains (in PKR):", min_value=0, value=0, step=1000)
            holding_period = st.number_input("Enter Holding Period (in years):", min_value=0, value=1, step=1)
            if st.button("Add Capital Gains", key="add_capital_gains"):
                tax = calculate_capital_gains_tax(gains_income, holding_period)
                st.session_state["selected_items"]["Income Sources"].append(("Capital Gains", gains_income, tax))
                st.success("Capital gains added successfully.")

    elif selected_main_category == "Deductions":
        selected_deduction = st.multiselect("Select Deductions:", [
            "Charitable Donations", "Education Expenses", "Medical Expenses", "Zakat Contributions",
            "Housing Loan Interest", "Depreciation", "Advertising Costs", "Employee Contributions", "Custom Input"
        ])
        for selection in selected_deduction:
            if selection == "Custom Input":
                custom_name = st.text_input("Enter Custom Deduction Name:")
                custom_value = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
                if st.button(f"Add Custom Deduction", key=f"add_{custom_name}_deduction"):
                    st.session_state["selected_items"]["Deductions"].append((custom_name, custom_value))
                    st.success(f"Custom deduction {custom_name} added successfully.")
            else:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_deduction")
                if st.button(f"Add {selection}", key=f"add_{selection}_deduction"):
                    st.session_state["selected_items"]["Deductions"].append((selection, value))
                    st.success(f"Deduction {selection} added successfully.")

    elif selected_main_category == "Tax Credits":
        selected_credit = st.multiselect("Select Tax Credits:", [
            "Investment in Housing", "Foreign Taxes Paid", "R&D Expenses", "Renewable Energy Investment",
            "Pension Contributions", "Education Loans", "Disabled Persons", "Women Entrepreneurs",
            "IT and Startups", "Green Investments", "Welfare Projects", "Custom Input"
        ])
        for selection in selected_credit:
            if selection == "Custom Input":
                custom_name = st.text_input("Enter Custom Tax Credit Name:")
                custom_value = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
                if st.button(f"Add Custom Tax Credit", key=f"add_{custom_name}_credit"):
                    st.session_state["selected_items"]["Tax Credits"].append((custom_name, custom_value))
                    st.success(f"Custom tax credit {custom_name} added successfully.")
            else:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_credit")
                if st.button(f"Add {selection}", key=f"add_{selection}_credit"):
                    st.session_state["selected_items"]["Tax Credits"].append((selection, value))
                    st.success(f"Tax credit {selection} added successfully.")

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
