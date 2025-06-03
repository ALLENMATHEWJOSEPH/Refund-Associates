import streamlit as st
from datetime import datetime, timedelta

# Function to add months to a date
def add_months(date, months):
    new_month = date.month + months
    new_year = date.year + new_month // 12
    new_month = new_month % 12
    day = min(date.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][new_month-1])  # Handle end of month
    return datetime(new_year, new_month, day)

# Function to format date as yyyy-mm-dd
def format_date(date):
    return date.strftime("%Y-%m-%d")

# Streamlit Interface
st.title("CRA Filing Deadline Calculator for First Nations")

# Input fields
filing_code = st.selectbox("Select Filing Code", ["PSB", "Code 1A", "Code 8"])
filer_status = st.selectbox("Filer Status", ["Filer", "Non-Filer"])
frequency = st.selectbox("Select Filing Frequency", ["Monthly", "Quarterly", "Annually"])
fiscal_start = st.date_input("Select Fiscal Year Start Date", value=datetime(2025, 4, 1))
start_year = st.selectbox("Select Starting Year", [2024, 2025, 2026])

# Button to calculate the deadlines
if st.button("Calculate Deadlines"):
    # Convert input fiscal start to a date
    fiscal_start_date = datetime(fiscal_start.year, fiscal_start.month, fiscal_start.day)
    
    # Logic to calculate the periods and deadlines
    periods = []
    period_count = 12 if frequency == "Monthly" else 4 if frequency == "Quarterly" else 1
    current_start = fiscal_start_date.replace(year=start_year)
    
    for i in range(period_count):
        start = current_start
        if frequency == "Monthly":
            end = add_months(start, 1) - timedelta(days=1)
        elif frequency == "Quarterly":
            end = add_months(start, 3) - timedelta(days=1)
        else:  # Annually
            end = start.replace(year=start.year + 1) - timedelta(days=1)

        # Deadline for filing is 3 months after the period end
        deadline = end + timedelta(days=90)

        periods.append({
            "Period Start": format_date(start),
            "Period End": format_date(end),
            "Filing Deadline": format_date(deadline),
            "Latest Allowed Filing Date": format_date(deadline)
        })

        # Update current start for the next period
        current_start = end + timedelta(days=1)
    
    # Show the results in a table
    st.write("### Filing Periods and Deadlines")
    st.write(f"**Filing Code:** {filing_code}")
    st.write(f"**Filer Status:** {filer_status}")
    st.write(f"**Filing Frequency:** {frequency}")
    
    # Display results in a table
    df = pd.DataFrame(periods)
    st.write(df)
    
    # Optionally: Provide CSV download link
    st.download_button(
        label="Download CSV",
        data=df.to_csv(index=False),
        file_name="filing_deadlines.csv",
        mime="text/csv"
    )

