import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from astropy.timeseries import LombScargle

# --- PAGE CONFIG AND TITLE --- #
st.set_page_config(page_title = "V603 Aql 2021 Campaign Data", layout = "wide")
st.title("V603 Aql 2021 campaign data")

# --- CACHING FOR DATA SET LOADING --- #
@st.cache_data
def get_data(filename):
    camp_data = pd.read_excel(filename)

    return camp_data

camp_data = get_data('aavso2021Camp.xlsx')

# --- DATA SET INFORMATION --- #
intro_para = "The 2021 Oberserving Campaign on the cataclysmic variable star V603 Aql ran over the months of May, June and July. This data set is the most comprehensive ever collected for this object, containing over 74,000 individual observations. This app displays the data in full and allows the user to view data selected by date, filter and observer."
st.write(intro_para)

# --- SELECT DATA BY DATE RANGE --- #
st.subheader("Plot 1: Select the date range")
start_date, end_date = st.select_slider("Use the date slider to select the data timeframe", options=camp_data['JD'], value=(camp_data['JD'].min(), camp_data['JD'].max()), label_visibility='hidden')

# --- CREATE DATA FRAME FOR DATE SELECTION --- #
filt_data = camp_data[(camp_data['JD'] >= start_date) & (camp_data['JD'] <= end_date)]

# --- PLOT DATA BY DATE AND MAGNITUDE --- #
x = filt_data['JD']
y = filt_data['Magnitude']
total_obs = filt_data['Magnitude'].size

fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x, y, ',', color='r')
plt.xlabel("Julian Date")
plt.ylabel("Magnitude")
st.pyplot(fig)
st.write(f"Total Observations for date range: {total_obs}")

st.subheader("Plot 2: All data for selected filter")
# --- SELECT DATA BY OBSERVING FILTER --- # 
obs_filter = st.selectbox('Plot 2 Filter Selector', options=camp_data['Band'].unique(), label_visibility="hidden")
filter_data = camp_data[camp_data['Band'] == obs_filter]
# --- PLOT FILTER DATA BY JD AND MAG --- #
x1 = filter_data['JD']
y1 = filter_data['Magnitude']
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x1, y1, 'o', markersize=1, color='r')
plt.xlabel("Julian Date")
plt.ylabel("Magnitude")
st.pyplot(fig)

# --- INITIALISE SESSION STATE FOR DATA VISABILITY --- #
if 'show_data' not in st.session_state:
    st.session_state.show_data = False

# --- BUTTON TO TOGGLE DATA VIS --- #
if st.button("Show/Hide Filter Data Table"):
    st.session_state.show_data = not st.session_state.show_data

# --- DISPLAY DATA BASED ON SESSION STATE --- #
if st.session_state.show_data:
    st.subheader("Filter Data")
    df = pd.DataFrame(filter_data)
    st.dataframe(df)
else:
    st.write("Data table is hidden")

st.subheader("Plot 3: All data for selected observer")
# --- SELECT DATA BY OBSERVER --- # 
observer = st.selectbox('Plot 3 Observer Selector', options=camp_data['Observer Code'].unique(),label_visibility="hidden")
obs_data = camp_data[camp_data['Observer Code'] == observer]
# --- PLOT OBSERVER DATA BY JD AND MAG --- #
x2 = obs_data['JD']
y2 = obs_data['Magnitude']
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(x2, y2, 'o', markersize=1, color='r')
plt.xlabel("Julian Date")
plt.ylabel("Magnitude")
st.pyplot(fig)

# --- INITIALISE SESSION STATE FOR DATA VISABILITY --- #
if 'sh_data' not in st.session_state:
    st.session_state.sh_data = False

# --- BUTTON TO TOGGLE DATA VIS --- #
if st.button("Show/Hide Observer Data Table"):
    st.session_state.sh_data = not st.session_state.sh_data

# --- DISPLAY DATA BASED ON SESSION STATE --- #
if st.session_state.sh_data:
    st.subheader("Observer Data")
    df2 = pd.DataFrame(obs_data)
    st.dataframe(df2)
else:
    st.write("Data table is hidden")

# --- DATA ANALYSIS --- #
st.subheader("Data Analysis")
st.write("This section needs to be searchable by date, band, observer and period timeframes (Make the default search window between 0 and 3 days). Also, print the 5 most powerful periods as per thesis code")
t = obs_data["JD"]
y = obs_data["Magnitude"]

frequency, power = LombScargle(t, y).autopower()

fig, ax = plt.subplots()
ax.plot(frequency, power, color='r')
plt.xlabel("Frequency(Days)")
plt.ylabel("Power")
st.pyplot(fig)
