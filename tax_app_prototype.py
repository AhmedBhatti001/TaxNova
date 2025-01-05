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
        .highlight {
            color: red;
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

# Function to calculate salary tax
def calculate_salary_tax(income):
    slabs = [
        {"limit": 600000, "rate": 0},
        {"limit": 1200000, "rate": 0.05, "base_tax": 0},
        {"limit": 2200000, "rate": 0.15, "base_tax": 30000},
        {"limit": 3200000, "rate": 0.25, "base_tax": 180000},
        {"limit": 4100000, "rate": 0.30, "base_tax": 430000},
        {"limit": float("inf"), "rate": 0.35, "base_tax": 700000},
    ]
    for slab in slabs:
        if income <= slab["limit"]:
            previous_limit = slabs[slabs.index(slab) - 1]["limit"] if slabs.index(slab) > 0 else 0
            return slab.get("base_tax", 0) + (income - previous_limit) * slab["rate"]

# Function to dynamically handle income source selections
def handle_income_sources():
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
            tax = calculate_salary_tax(business_income)  # Adjust logic for specific business type
            st.session_state["selected_items"]["Income Sources"].append(("Business", business_income, tax))
            st.success("Business income added successfully.")
    elif income_main_categories == "Income from Property":
        property_income = st.selectbox("Select Property Income Type:", [
            "Rental Income from Residential Properties", "Rental Income from Commercial Properties",
            "Leasing Income", "Subletting Income"
        ])
        property_value = st.number_input(f"Enter amount for {property_income} (in PKR):", min_value=0, value=0, step=1000)
        if st.button(f"Add {property_income}", key=f"add_{property_income}"):
            st.session_state["selected_items"]["Income Sources"].append((property_income, property_value, 0))
            st.success(f"{property_income} added successfully.")
    elif income_main_categories == "Capital Gains":
        gains_income = st.number_input("Enter Capital Gains (in PKR):", min_value=0, value=0, step=1000)
        holding_period = st.number_input("Enter Holding Period (in years):", min_value=0, value=1, step=1)
        if st.button("Add Capital Gains", key="add_capital_gains"):
            tax = calculate_salary_tax(gains_income)  # Adjust logic for capital gains tax
            st.session_state["selected_items"]["Income Sources"].append(("Capital Gains", gains_income, tax))
            st.success("Capital gains added successfully.")
    elif income_main_categories == "Income from Other Sources":
        other_income = st.selectbox("Select Other Income Type:", [
            "Interest Income", "Dividend Income", "Royalty Income", "Prize Money"
        ])
        other_value = st.number_input(f"Enter amount for {other_income} (in PKR):", min_value=0, value=0, step=1000)
        if st.button(f"Add {other_income}", key=f"add_{other_income}"):
            st.session_state["selected_items"]["Income Sources"].append((other_income, other_value, 0))
            st.success(f"{other_income} added successfully.")
    elif income_main_categories == "Foreign Income":
        foreign_income = st.selectbox("Select Foreign Income Type:", [
            "Salaries Earned Abroad", "Business Income from Foreign Operations",
            "Dividends and Interest Earned Overseas", "Foreign Rental Income"
        ])
        foreign_value = st.number_input(f"Enter amount for {foreign_income} (in PKR):", min_value=0, value=0, step=1000)
        if st.button(f"Add {foreign_income}", key=f"add_{foreign_income}"):
            st.session_state["selected_items"]["Income Sources"].append((foreign_income, foreign_value, 0))
            st.success(f"{foreign_income} added successfully.")

# Function to dynamically handle deductions
def handle_deductions():
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

# Function to dynamically handle tax credits
def handle_tax_credits():
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

# Display selected items
def display_selected_items():
    st.markdown('<h2 class="header">Selected Items Summary</h2>', unsafe_allow_html=True)
    st.write("### Income Sources:")
    for item, value, tax in st.session_state["selected_items"]["Income Sources"]:
        st.markdown(f"<span class='highlight'>- {item}: PKR {value} | Tax: PKR {tax}</span>", unsafe_allow_html=True)
    st.write("### Deductions:")
    for item, value in st.session_state["selected_items"]["Deductions"]:
        st.markdown(f"<span class='highlight'>- {item}: PKR {value}</span>", unsafe_allow_html=True)
    st.write("### Tax Credits:")
    for item, value in st.session_state["selected_items"]["Tax Credits"]:
        st.markdown(f"<span class='highlight'>- {item}: PKR {value}</span>", unsafe_allow_html=True)

# Main function
def main():
    set_styles()
    st.markdown('<h1 class="header">🏦 TaxNova: Comprehensive Tax App</h1>', unsafe_allow_html=True)
    st.write("This app calculates your taxes with a detailed breakdown of income sources, deductions, and tax credits.")

    selected_main_category = st.selectbox("Select Main Category:", ["Income Sources", "Deductions", "Tax Credits"])

    if selected_main_category == "Income Sources":
        handle_income_sources()
    elif selected_main_category == "Deductions":
        handle_deductions()
    elif selected_main_category == "Tax Credits":
        handle_tax_credits()

    display_selected_items()

if __name__ == "__main__":
    main()
