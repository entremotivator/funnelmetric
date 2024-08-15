import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Initialize platforms and metrics
platforms = [
    "Facebook", "Instagram (IG)", "Twitter", "Threads", "Pinterest", 
    "TikTok", "YouTube", "LinkedIn", "Fanbase", "Facebook Group"
]
metrics = [
    "Posts", "Engagement", "Clicks", "Views", "Appointments", "Show-ups",
    "Closings", "Email Opens", "Recovery Actions", "Referrals", "Retargets"
]

# Generate demo data for 90 days
def generate_demo_data():
    data = {}
    start_date = datetime.today()
    for platform in platforms:
        platform_data = {}
        for metric in metrics:
            # Create realistic demo data with variation
            base_value = random.randint(50, 150)  # Base value for variation
            platform_data[metric] = [
                {
                    "Date": (start_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                    "Value": int(base_value + random.gauss(0, 20))  # Gaussian distribution for variability
                }
                for i in range(90)
            ]
        data[platform] = platform_data
    return data

# Data to DataFrame
def generate_platform_df(platform_data):
    df = pd.DataFrame({metric: [entry["Value"] for entry in platform_data[metric]] for metric in platform_data})
    df['Date'] = pd.to_datetime([entry["Date"] for entry in platform_data[metrics[0]]])
    df.index = df['Date']
    # Ensure only numeric data is summed
    numeric_df = df.select_dtypes(include=[np.number])
    df['Total'] = numeric_df.sum(axis=1)
    df['Average'] = numeric_df.mean(axis=1)
    return df

# Load Data (Simulated Persistence)
def load_data():
    if 'data' not in st.session_state:
        st.session_state['data'] = generate_demo_data()
    return st.session_state['data']

# Save Data (Simulated Persistence)
def save_data(data):
    st.session_state['data'] = data

# Main App
def main():
    st.title("90-Day Funnel Tracking System")

    data = load_data()

    # Dashboard Overview
    st.header("Dashboard Overview")

    # Display all metrics without date filtering
    st.subheader("All Metrics Overview")
    
    # Sum up metrics across all platforms for the entire period
    summary = pd.DataFrame(columns=metrics)
    for platform in platforms:
        if platform in data:
            platform_df = generate_platform_df(data[platform])
            summary.loc[platform] = platform_df[metrics].sum()
        else:
            st.warning(f"No data available for {platform}")

    st.dataframe(summary)

    # Detailed Platform Data
    st.sidebar.header("Platform Data")
    selected_platform = st.sidebar.selectbox("Select a Platform", platforms)

    st.subheader(f"Tracking Data for {selected_platform}")
    if selected_platform in data:
        platform_df = generate_platform_df(data[selected_platform])
        st.dataframe(platform_df)
    else:
        st.warning(f"No data available for {selected_platform}")

    # Plot multiple metric trends over 90 days
    st.subheader("Metric Trends")
    metrics_to_plot = st.multiselect("Select Metrics to Plot", metrics, default=metrics[:3])
    if selected_platform in data:
        platform_df = generate_platform_df(data[selected_platform])
        st.line_chart(platform_df[metrics_to_plot])
    else:
        st.warning(f"No data available for {selected_platform}")

    # Provide option to enter or update data for each day and metric
    st.sidebar.header("Update Data")
    day = st.sidebar.slider("Select Day", 1, 90, 1)

    if selected_platform in data:
        platform_df = generate_platform_df(data[selected_platform])
        for metric in metrics:
            value = st.sidebar.number_input(f"Enter value for {metric} on Day {day}", 0, 100, key=f"{selected_platform}_{metric}_{day}")
            platform_df.at[platform_df.index[day-1], metric] = value

        # Save and update the data (mocked for demo purposes)
        if st.sidebar.button("Save Data"):
            data[selected_platform] = platform_df.to_dict(orient='list')
            save_data(data)
            st.success("Data updated successfully!")

    # Export data as CSV
    st.sidebar.header("Export Data")
    if st.sidebar.button("Download Data as CSV"):
        export_df = pd.concat([generate_platform_df(data[platform]) for platform in platforms], keys=platforms)
        export_df.to_csv("funnel_tracking_data.csv")
        st.sidebar.success("Data exported successfully! Check your download folder.")

    # Data Import
    st.sidebar.header("Import Data")
    uploaded_file = st.sidebar.file_uploader("Upload your data", type=["csv"])
    if uploaded_file:
        imported_data = pd.read_csv(uploaded_file)
        st.sidebar.success("Data imported successfully!")
        # Here you would merge the imported data with existing data

    # Send Email Reports (Mocked)
    st.sidebar.header("Notifications")
    if st.sidebar.button("Send Daily Report"):
        st.sidebar.success("Daily report sent!")

    if st.sidebar.button("Send Weekly Report"):
        st.sidebar.success("Weekly report sent!")

    # Additional Insights and Analytics
    st.subheader("Additional Insights")
    st.write("Engagement Analysis: Average engagement per platform, top-performing days, and metrics.")

    if selected_platform in data:
        top_performers = {platform: generate_platform_df(data[platform])['Engagement'].mean() for platform in platforms}
        sorted_platforms = sorted(top_performers.items(), key=lambda x: x[1], reverse=True)

        st.write(f"Top Performing Platform: {sorted_platforms[0][0]} with average engagement of {sorted_platforms[0][1]:.2f}")

    st.write("Here, you can add more charts or analysis, like identifying top-performing platforms, days with the highest engagement, etc.")

if __name__ == "__main__":
    main()
