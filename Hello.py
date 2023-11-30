# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():

    # Load Bike Sharing Dataset
    bike_hour_df = pd.read_csv("data/hour.csv")
    bike_day_df = pd.read_csv("data/day.csv")



    # Helper function to create daily dataframe
    def create_daily_df(df):
        daily_df = df.groupby("dteday").agg({
            "cnt": "sum",
            "temp": "mean",
            "hum": "mean",
            "windspeed": "mean"
        }).reset_index()
        return daily_df


    # Prepare dataframes
    daily_df = create_daily_df(bike_day_df)

    # Streamlit App
    st.title("Bike Sharing Dataset Dashboard")

    daily_df['dteday'] = pd.to_datetime(daily_df['dteday'])

    # Sidebar with date range selection
    min_date = daily_df["dteday"].min()
    max_date = daily_df["dteday"].max()

    with st.sidebar:
        st.image("https://user-images.githubusercontent.com/33750251/64987392-f9eead80-d8c0-11e9-84a9-e2a4a7f624db.png")
        start_date, end_date = st.date_input(
            label='Date Range',
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

    # Filter data based on selected date range
    filtered_df = daily_df[(daily_df["dteday"] >= str(start_date)) & (daily_df["dteday"] <= str(end_date))]

    # Plot total bike rentals over time
    st.header('Bike Rentals Over Time')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(filtered_df["dteday"], filtered_df["cnt"], marker='o', linewidth=2, color="#90CAF9")
    ax.set_xlabel("Date")
    ax.set_ylabel("Total Bike Rentals")
    ax.set_title("Total Bike Rentals Over Time")
    st.pyplot(fig)

    # Plot temperature, humidity, and windspeed trends
    st.header('Weather Trends')
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(filtered_df["dteday"], filtered_df["temp"], label="Temperature", marker='o')
    ax.plot(filtered_df["dteday"], filtered_df["hum"], label="Humidity", marker='o')
    ax.plot(filtered_df["dteday"], filtered_df["windspeed"], label="Windspeed", marker='o')

    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized Values")
    ax.set_title("Weather Trends Over Time")
    ax.legend()
    st.pyplot(fig)

    # Display dataset characteristics
    st.header('Dataset Characteristics')
    st.write("Number of records:", len(bike_day_df))
    st.write("Columns:", bike_day_df.columns.tolist())
    st.write("Sample data:", bike_day_df.head())

    # Add any other analysis or visualizations you need

    # Finally, display the app
    st.caption('Copyright © Dicoding 2023')



if __name__ == "__main__":
    run()
