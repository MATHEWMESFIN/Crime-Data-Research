# Description: This file contains the functions to visualize the data

import streamlit as st
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
import streamlit.components.v1 as components

# A function that provides user input for the date range and crime type
def user_input(cleaned_data):
    # create a sidebar
    st.sidebar.header("User Input")
    # create a date range slider
    from_date = st.sidebar.date_input('From Date', pd.to_datetime('2014/01/01 00:00:00+00'), min_value=pd.to_datetime('2014/01/01 00:00:00+00'))
    to_date = st.sidebar.date_input('To Date', pd.to_datetime('2015/01/01 00:00:00+00'), min_value=pd.to_datetime('2015/01/01 00:00:00+00'))
    # create a dropdown menu for the crime type
    crime = st.sidebar.selectbox("Crime Type", cleaned_data['Description'].unique())
    return from_date, to_date, crime

from_date, to_date, crime = user_input(cleaned_data)

# Display the data
def display_data(cleaned_data, from_date, to_date, crime):

    # A function that focuses on the rows with 'CrimeDatetime' between the from_date and to_date
    def focus_crime_date_time_rows(data, from_date, to_date):
        # convert the from_date and to_date to str objects
        from_date = str(from_date)
        to_date = str(to_date)

        # focus on the rows with 'CrimeDatetime' between the from_date and to_date
        cleaned_data = data[data['CrimeDateTime'] > from_date]
        cleaned_data = cleaned_data[data['CrimeDateTime'] < to_date]

        return cleaned_data
    cleaned_data = focus_crime_date_time_rows(cleaned_data, from_date, to_date)

    st.write("Cleaned Data and Number of Crimes per Crime Type")
    col1, col2 = st.columns(2)
    col1.dataframe(cleaned_data)
    col2.bar_chart(cleaned_data['Description'].value_counts(), height=500)

    # A function to display a line chart of the percent of each crime to all crimes per month
    def get_crime_percents():

        # create a DataFrame for each crime description
        larceny_data = cleaned_data[cleaned_data['Description'] == 'LARCENY']
        commonAssault_data = cleaned_data[cleaned_data['Description'] == 'COMMON ASSAULT']
        burglary_data = cleaned_data[cleaned_data['Description'] == 'BURGLARY']
        homicide_data = cleaned_data[cleaned_data['Description'] == 'HOMICIDE']
        autoTheft_data = cleaned_data[cleaned_data['Description'] == 'AUTO THEFT']
        aggravatedAssault_data = cleaned_data[cleaned_data['Description'] == 'AGG. ASSAULT']
        arson_data = cleaned_data[cleaned_data['Description'] == 'ARSON']
        rape_data = cleaned_data[cleaned_data['Description'] == 'RAPE']
        robbery_data = cleaned_data[cleaned_data['Description'] == 'ROBBERY']
        shooting_data = cleaned_data[cleaned_data['Description'] == 'SHOOTING']

        # convert value_counts() to periodindex
        larceny_data['CrimeDateTime'] = pd.to_datetime(larceny_data['CrimeDateTime'])
        commonAssault_data['CrimeDateTime'] = pd.to_datetime(commonAssault_data['CrimeDateTime'])
        burglary_data['CrimeDateTime'] = pd.to_datetime(burglary_data['CrimeDateTime'])
        homicide_data['CrimeDateTime'] = pd.to_datetime(homicide_data['CrimeDateTime'])
        autoTheft_data['CrimeDateTime'] = pd.to_datetime(autoTheft_data['CrimeDateTime'])
        aggravatedAssault_data['CrimeDateTime'] = pd.to_datetime(aggravatedAssault_data['CrimeDateTime'])
        arson_data['CrimeDateTime'] = pd.to_datetime(arson_data['CrimeDateTime'])
        rape_data['CrimeDateTime'] = pd.to_datetime(rape_data['CrimeDateTime'])
        robbery_data['CrimeDateTime'] = pd.to_datetime(robbery_data['CrimeDateTime'])
        shooting_data['CrimeDateTime'] = pd.to_datetime(shooting_data['CrimeDateTime'])

        # group each crime description by day
        larceny_data = larceny_data['CrimeDateTime'].value_counts().resample('M').sum()
        commonAssault_data = commonAssault_data['CrimeDateTime'].value_counts().resample('M').sum()
        burglary_data = burglary_data['CrimeDateTime'].value_counts().resample('M').sum()
        homicide_data = homicide_data['CrimeDateTime'].value_counts().resample('M').sum()
        autoTheft_data = autoTheft_data['CrimeDateTime'].value_counts().resample('M').sum()
        aggravatedAssault_data = aggravatedAssault_data['CrimeDateTime'].value_counts().resample('M').sum()
        arson_data = arson_data['CrimeDateTime'].value_counts().resample('M').sum()
        rape_data = rape_data['CrimeDateTime'].value_counts().resample('M').sum()
        robbery_data = robbery_data['CrimeDateTime'].value_counts().resample('M').sum()
        shooting_data = shooting_data['CrimeDateTime'].value_counts().resample('M').sum()

        # convert value_counts() to periodindex
        cleaned_data['CrimeDateTime'] = pd.to_datetime(cleaned_data['CrimeDateTime'])

        # create a new DataFrame with all crimes and group by month
        all_data = cleaned_data['CrimeDateTime'].value_counts().resample('M').sum()

        # create the percent dataframe each crime to all crimes per month
        larceny_percent_data = (larceny_data / all_data) * 100
        commonAssault_percent_data = (commonAssault_data / all_data) * 100
        burglary_percent_data = (burglary_data / all_data) * 100
        homicide_percent_data = (homicide_data / all_data) * 100
        autoTheft_percent_data = (autoTheft_data / all_data) * 100
        aggravatedAssault_percent_data = (aggravatedAssault_data / all_data) * 100
        arson_percent_data = (arson_data / all_data) * 100
        rape_percent_data = (rape_data / all_data) * 100
        robbery_percent_data = (robbery_data / all_data) * 100
        shooting_percent_data = (shooting_data / all_data) * 100

        # merge all the percent DataFrames into one DataFrame
        merged_data = pd.merge(larceny_percent_data, commonAssault_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count_x': '1 - Larceny', 'count_y': '2 - Common Assault'})
        merged_data = pd.merge(merged_data, burglary_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '3 - Burglary'})
        merged_data = pd.merge(merged_data, homicide_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '8 - Homicide'})
        merged_data = pd.merge(merged_data, autoTheft_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '6 - Auto Theft'})
        merged_data = pd.merge(merged_data, aggravatedAssault_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '4 - Aggravated Assault'})
        merged_data = pd.merge(merged_data, arson_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '10 - Arson'})
        merged_data = pd.merge(merged_data, rape_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '9 - Rape'})
        merged_data = pd.merge(merged_data, robbery_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '5 - Robbery'})
        merged_data = pd.merge(merged_data, shooting_percent_data, on='CrimeDateTime')
        merged_data = merged_data.rename(columns={'count': '7 - Shooting'})

        return (merged_data)
    crime_percents = get_crime_percents()

    st.write("Number of Crimes per Month and Percent of Each Crime to All Crimes per Month")
    col1, col2 = st.columns(2)
    col1.area_chart(cleaned_data['CrimeDateTime'].value_counts().resample('M').sum())
    col2.area_chart(crime_percents)

    # create map
    crime_map = folium.Map(location=[cleaned_data['Latitude'].mean(), cleaned_data['Longitude'].mean()], zoom_start=12)

    # Create a MarkerCluster layer
    marker_cluster = plugins.MarkerCluster().add_to(crime_map)

    #used when hovering over popup
    tooltip = 'Click for more info'

    # add markers with popups for each location
    for index, row in cleaned_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Description: {row['Description']}",
            icon=folium.Icon(color='red' if row['Description'] == crime else 'blue'),
            tooltip=tooltip
        ).add_to(marker_cluster)  # Add to the MarkerCluster layer instead of the crime_map directly

    
    # display and save map as HTML file
    crime_map.save('crime_map_with_clusters.html') 

    HtmlFile = open("crime_map_with_clusters.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    components.html(source_code, height=500)
