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

# Dropdown for hierarchical selection with custom input option
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
        if income_main_categories == "Custom Input":
            custom_name = st.text_input("Enter Custom Income Name:")
            custom_value = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
            if st.button("Add Custom Income"):
                st.session_state["selected_items"]["Income Sources"].append((custom_name, custom_value))
        elif income_main_categories == "Salary":
            selected_salary = st.multiselect("Select Salary Components:", [
                "Basic Salary", "Bonuses", "Gratuity", "Leave Encashment", "Perquisites", "Benefits in Kind"
            ])
            for selection in selected_salary:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_income")
                if st.button(f"Add {selection}", key=f"add_{selection}"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))
        elif income_main_categories == "Income from Business":
            selected_business = st.multiselect("Select Business Income Type:", [
                "Sole Proprietorship Income", "Partnership Income", "Corporate Business Income", 
                "Profits from Manufacturing"
            ])
            for selection in selected_business:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_business")
                if st.button(f"Add {selection}", key=f"add_{selection}_business"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))
        elif income_main_categories == "Income from Property":
            selected_property = st.multiselect("Select Property Income Type:", [
                "Rental Income from Residential Properties", "Rental Income from Commercial Properties", 
                "Leasing Income", "Subletting Income"
            ])
            for selection in selected_property:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_property")
                if st.button(f"Add {selection}", key=f"add_{selection}_property"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))
        elif income_main_categories == "Capital Gains":
            selected_gains = st.multiselect("Select Capital Gains Type:", [
                "Gains on Sale of Real Estate", "Gains on Sale of Stocks", "Gains on Sale of Bonds"
            ])
            for selection in selected_gains:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_gains")
                if st.button(f"Add {selection}", key=f"add_{selection}_gains"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))
        elif income_main_categories == "Income from Other Sources":
            selected_others = st.multiselect("Select Other Income Type:", [
                "Interest Income", "Dividend Income", "Royalty Income", "Prize Money"
            ])
            for selection in selected_others:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_others")
                if st.button(f"Add {selection}", key=f"add_{selection}_others"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))
        elif income_main_categories == "Foreign Income":
            selected_foreign = st.multiselect("Select Foreign Income Type:", [
                "Salaries Earned Abroad", "Business Income from Foreign Operations", 
                "Dividends and Interest Earned Overseas", "Foreign Rental Income"
            ])
            for selection in selected_foreign:
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_foreign")
                if st.button(f"Add {selection}", key=f"add_{selection}_foreign"):
                    st.session_state["selected_items"]["Income Sources"].append((selection, value))

    elif selected_main_category == "Deductions":
        selected_deduction = st.multiselect("Select Deductions:", [
            "Charitable Donations", "Education Expenses", "Medical Expenses", "Zakat Contributions",
            "Housing Loan Interest", "Depreciation", "Advertising Costs", "Employee Contributions", "Custom Input"
        ])
        if "Custom Input" in selected_deduction:
            custom_name = st.text_input("Enter Custom Deduction Name:")
            custom_value = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
            if st.button("Add Custom Deduction"):
                st.session_state["selected_items"]["Deductions"].append((custom_name, custom_value))
        for selection in selected_deduction:
            if selection != "Custom Input":
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_deduction")
                if st.button(f"Add {selection}", key=f"add_{selection}_deduction"):
                    st.session_state["selected_items"]["Deductions"].append((selection, value))

    elif selected_main_category == "Tax Credits":
        selected_credit = st.multiselect("Select Tax Credits:", [
            "Investment in Housing", "Foreign Taxes Paid", "R&D Expenses", "Renewable Energy Investment",
            "Pension Contributions", "Education Loans", "Disabled Persons", "Women Entrepreneurs",
            "IT and Startups", "Green Investments", "Welfare Projects", "Custom Input"
        ])
        if "Custom Input" in selected_credit:
            custom_name = st.text_input("Enter Custom Tax Credit Name:")
            custom_value = st.number_input(f"Enter amount for {custom_name} (in PKR):", min_value=0, value=0, step=1000)
            if st.button("Add Custom Tax Credit"):
                st.session_state["selected_items"]["Tax Credits"].append((custom_name, custom_value))
        for selection in selected_credit:
            if selection != "Custom Input":
                value = st.number_input(f"Enter amount for {selection} (in PKR):", min_value=0, value=0, step=1000, key=f"{selection}_credit")
                if st.button(f"Add {selection}", key=f"add_{selection}_credit"):
                    st.session_state["selected_items"]["Tax Credits"].append((selection, value))

# Calculate taxes
def calculate_tax():
    total_income = sum(value for _, value in st.session_state["selected_items"]["Income Sources"])
    total_deductions = sum(value for _, value in st.session_state["selected_items"]["Deductions"])
    total_credits = sum(value for _, value in st.session_state["selected_items"]["Tax Credits"])

    taxable_income = max(total_income - total_deductions, 0)
    tax_payable_before_credits = taxable_income * 0.10  # Example flat tax rate
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
    for item, value in st.session_state["selected_items"]["Income Sources"]:
        st.write(f"- {item}: PKR {value}")

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
