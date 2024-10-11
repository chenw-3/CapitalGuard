import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to calculate future value with inflation
def calculate_with_inflation(current_value, inflation_rate, years):
    return current_value * ((1 + inflation_rate) ** years)

# App Title
st.title("Captial Guard")

# Description
st.header("This app will help you gain a better understanding of where you stand financially based on your monthly earnings vs expenses!")

# Step 1: Input Monthly Income
st.header("Step 1: Enter your monthly income")
monthly_income = st.number_input("Enter your total monthly income (in $)", min_value=0)
annual_income = monthly_income * 12

# Step 2: Input Monthly Expenses
st.header("Step 2: Enter your monthly expenses")
expenses = {
    "Housing (rent/mortgage)": st.number_input("Housing (rent/mortgage)", min_value=0),
    "Utilities (electricity, water, etc.)": st.number_input("Utilities (electricity, water, etc.)", min_value=0),
    "Groceries": st.number_input("Groceries", min_value=0),
    "Transportation": st.number_input("Transportation", min_value=0),
    "Entertainment": st.number_input("Entertainment", min_value=0),
    "Savings": st.number_input("Savings", min_value=0),
    "Other expenses": st.number_input("Other expenses", min_value=0)
}

# Calculate total expenses
total_expenses = sum(expenses.values())

# Step 3: Enter Family Information for Insurance Recommendation
st.header("Step 3: Enter your family information for insurance recommendation")

# Number of dependents
dependents = st.number_input("Number of dependents (e.g., spouse, children, etc.)", min_value=0)

# Ages of dependents (optional)
dependent_ages = st.text_input("Enter the ages of dependents (comma-separated)", '')

# Existing insurance coverage (optional)
existing_coverage = st.number_input("Existing life insurance coverage (in $)", min_value=0)

# Ask user how many years ahead they want to consider inflation for
years_to_inflate = st.number_input("How many years into the future should inflation be considered?", min_value=1, max_value=50, step=1, value=20)

# Step 4: Insurance Recommendation Logic
st.header("Insurance Recommendation")

# Recommended life insurance = 10x annual income (Level Calculation)
recommended_insurance_level = annual_income * 10  # Using 10x as a basic rule of thumb

# Recommended life insurance adjusted for inflation (3% annual inflation)
inflation_rate = 0.03
recommended_insurance_inflation = calculate_with_inflation(recommended_insurance_level, inflation_rate, years_to_inflate)

# Display life insurance recommendations
if dependents > 0:
    st.write(f"**Level Calculation:** Based on your income and {dependents} dependent(s), we recommend you have at least ${recommended_insurance_level:,.2f} in life insurance coverage.")
    st.write(f"**Inflation-Adjusted Calculation:** Considering 3% annual inflation over {years_to_inflate} years, we recommend ${recommended_insurance_inflation:,.2f} in life insurance to cover future needs.")
else:
    st.write(f"**Level Calculation:** Based on your income, we recommend you have at least ${recommended_insurance_level:,.2f} in life insurance coverage.")
    st.write(f"**Inflation-Adjusted Calculation:** Considering 3% annual inflation over {years_to_inflate} years, we recommend ${recommended_insurance_inflation:,.2f} in life insurance to cover future needs.")

# Compare with existing coverage
if existing_coverage > 0:
    if existing_coverage < recommended_insurance_inflation:
        st.warning(f"Your current life insurance coverage of ${existing_coverage:,.2f} is less than the inflation-adjust")


# Step 5: Show Results and Budget Comparison
st.header("Step 4: Your Results")

# Calculate recommended spending based on 50/30/20 rule
recommended_essentials = 0.5 * monthly_income
recommended_discretionary = 0.3 * monthly_income
recommended_savings = 0.2 * monthly_income

# Calculate actual spending categories
actual_essentials = expenses["Housing (rent/mortgage)"] + expenses["Utilities (electricity, water, etc.)"] + expenses["Groceries"] + expenses["Transportation"]
actual_discretionary = expenses["Entertainment"] + expenses["Other expenses"]
actual_savings = expenses["Savings"]

# Display comparison
st.subheader("Comparison to recommended budget breakdown:")
comparison_df = pd.DataFrame({
    "Category": ["Essentials", "Discretionary", "Savings"],
    "Recommended Amount ($)": [recommended_essentials, recommended_discretionary, recommended_savings],
    "Your Spending ($)": [actual_essentials, actual_discretionary, actual_savings]
})
st.write(comparison_df)

# Visual Comparison
st.subheader("Visual Comparison")
fig, ax = plt.subplots()
ax.bar(comparison_df["Category"], comparison_df["Recommended Amount ($)"], label="Recommended", alpha=0.6)
ax.bar(comparison_df["Category"], comparison_df["Your Spending ($)"], label="Your Spending", alpha=0.6)
ax.set_ylabel("Amount ($)")
ax.set_title("Recommended vs Actual Spending")
ax.legend()

st.pyplot(fig)

# Check if you're over or under budget
st.subheader("Analysis")
if total_expenses > monthly_income:
    st.error(f"Warning: You are over budget by ${total_expenses - monthly_income:.2f}. Consider adjusting your spending.")
else:
    st.success(f"Good job! You are under budget by ${monthly_income - total_expenses:.2f}.")

# Breakdown of spending
st.subheader("Your Spending Breakdown:")
spending_breakdown = pd.DataFrame({
    "Category": list(expenses.keys()),
    "Amount ($)": list(expenses.values())
})
st.write(spending_breakdown)
