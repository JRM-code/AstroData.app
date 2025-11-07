import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 

#Page config and headers
st.set_page_config(page_title = "V603 Aql 2021 Campaign Data", layout = "wide")
st.header("V603 Aql 2021 campaign data")
st.sidebar.title("Data Selectors")

#Read in campaign data from xlsx file
camp_data = pd.read_excel('aavso2021Camp.xlsx')

intro_para = "The 2021 Oberserving Campaign on the cataclysmic variable star V603 Aql ran over the months of May, June and July. This data set is the most comprehensive ever collected for this object, containing over 74,000 individual observations. This app displays the data in full and allows the user to view data selected by date, filter and observer."
st.write(intro_para)

#Select date range for campaign data
st.subheader("Plot 1: Select the date range")
start_date, end_date = st.select_slider("Use the date slider to select the data timeframe", options=camp_data['JD'], value=(camp_data['JD'].min(), camp_data['JD'].max()), label_visibility='hidden')

#Filter the DataFrame based on the selected range
filt_data = camp_data[(camp_data['JD'] >= start_date) & (camp_data['JD'] <= end_date)]

x = filt_data['JD']
y = filt_data['Magnitude']

#Plot filtered JD and Magnitude
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x, y, ',', color='r')
st.pyplot(fig)

#Select data by filter 
obs_filter = st.sidebar.selectbox('Plot 2 Filter Selector', options=camp_data['Band'].unique())
filter_data = camp_data[camp_data['Band'] == obs_filter]

x1 = filter_data['JD']
y1 = filter_data['Magnitude']

#Plot filter type JD and Magnitude
st.subheader("Plot 2: All data for selected filter")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x1, y1, 'o', markersize=1, color='r')
st.pyplot(fig)

# Initialize session state for data visibility
if 'show_data' not in st.session_state:
    st.session_state.show_data = False

# Create a button to toggle data visibility
if st.button("Show/Hide Filter Data Table"):
    st.session_state.show_data = not st.session_state.show_data

# Conditionally display data based on session state
if st.session_state.show_data:
    st.subheader("Filter Data")
    df = pd.DataFrame(filter_data)
    st.dataframe(df)
else:
    st.write("Data table is hidden")

#Select data by observer
observer = st.sidebar.selectbox('Plot 3 Observer Selector', options=camp_data['Observer Code'].unique())
obs_data = camp_data[camp_data['Observer Code'] == observer]

x2 = obs_data['JD']
y2 = obs_data['Magnitude']

#Plot filtered JD and Magnitude
st.subheader("Plot 3: All data for selected observer")
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x2, y2, 'o', markersize=1, color='r')
st.pyplot(fig)

# Initialize session state for data visibility
if 'sh_data' not in st.session_state:
    st.session_state.sh_data = False

# Create a button to toggle data visibility
if st.button("Show/Hide Observer Data Table"):
    st.session_state.sh_data = not st.session_state.sh_data

# Conditionally display data based on session state
if st.session_state.sh_data:
    st.subheader("Observer Data")
    df2 = pd.DataFrame(obs_data)
    st.dataframe(df2)
else:
    st.write("Data table is hidden")