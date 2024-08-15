import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Initialize platforms and metrics
platforms = [f"Platform {i+1}" for i in range(10)]
metrics = [
    "Posts", "Engagement", "Clicks", "Views", "Appointments", "Show-ups",
    "Closings", "Email Opens", "Recovery Actions", "Referrals", "Retargets"
]

# Generate demo data for 31 days
def generate_demo_data():
    data = {}
    start_date = datetime.today()
    for platform in platforms:
        platform_data = {}
        for metric in metrics:
            platform_data[metric] = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d'), random.randint(0, 100)] for i in range(31)
        data[platform] = platform_data
    return data

# Data to DataFrame
def generate_platform_df(platform_data):
    df = pd.DataFrame(platform_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.index = df['Date']
    df['Total'] = df.sum(axis=1)
    df['Average'] = df.mean(axis=1)
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
    st.title("31-Day Funnel Tracking System")

    data = load_data()

    # Dashboard Overview
    st.header("Dashboard Overview")

    # Summary statistics with date range filtering
    st.subheader("Summary Statistics")
    start_date = st.date_input("Start Date", datetime.today() - timedelta(days=30))
    end_date = st.date_input("End Date", datetime.today())

    filtered_data = {platform: generate_platform_df(data[platform]).loc[start_date:end_date] for platform in platforms}

    total_posts = sum(filtered_data[platform]['Posts'].sum() for platform in platforms)
    total_engagement = sum(filtered_data[platform]['Engagement'].sum() for platform in platforms)
    total_clicks = sum(filtered_data[platform]['Clicks'].sum() for platform in platforms)
    total_views = sum(filtered_data[platform]['Views'].sum() for platform in platforms)

    st.write(f"**Total Posts**: {total_posts}")
    st.write(f"**Total Engagement**: {total_engagement}")
    st.write(f"**Total Clicks**: {total_clicks}")
    st.write(f"**Total Views**: {total_views}")

    # Platform Data
    st.sidebar.header("Platform Data")
    selected_platform = st.sidebar.selectbox("Select a Platform", platforms)

    st.subheader(f"Tracking Data for {selected_platform}")
    platform_df = generate_platform_df(data[selected_platform])
    st.dataframe(platform_df)

    # Plot multiple metric trends over 31 days
    st.subheader("Metric Trends")
    metrics_to_plot = st.multiselect("Select Metrics to Plot", metrics, default=metrics[:3])
    st.line_chart(platform_df[metrics_to_plot])

    # Heatmap for Engagement
    st.subheader("Engagement Heatmap")
    engagement_heatmap_data = platform_df.pivot_table(values='Engagement', index=platform_df.index, columns=platform_df.columns, fill_value=0)
    st.heatmap(engagement_heatmap_data)

    # Provide option to enter or update data for each day and metric
    st.sidebar.header("Update Data")
    day = st.sidebar.slider("Select Day", 1, 31, 1)

    for metric in metrics:
        value = st.sidebar.number_input(f"Enter value for {metric} on Day {day}", 0, 100, key=f"{selected_platform}_{metric}_{day}")
        platform_df.at[f"Day {day}", metric] = value

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

    top_performers = {platform: platform_df['Engagement'].mean() for platform in platforms}
    sorted_platforms = sorted(top_performers.items(), key=lambda x: x[1], reverse=True)

    st.write(f"Top Performing Platform: {sorted_platforms[0][0]} with average engagement of {sorted_platforms[0][1]:.2f}")

    st.write("Here, you can add more charts or analysis, like identifying top-performing platforms, days with the highest engagement, etc.")

if __name__ == "__main__":
    main()
