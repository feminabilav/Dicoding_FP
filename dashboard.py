import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")


def create_bymonth(df):
    bymonth = day_df.loc[(day_df["yr"]==1)].groupby(by="mnth").cnt.sum().reset_index()

    bymonth["mnth"] = bymonth["mnth"].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
    5: 'May', 6:'June',7:'July',8:'Aug',
    9:'Sept',10:'Oct',11:'Nov',12:'Dec'
    })
    
    return bymonth

def create_byday_casual(df):
    byday_casual = day_df.groupby(by="weekday").casual.sum().reset_index()
    byday_casual["weekday"] = byday_casual["weekday"].map({
    0:'Sunday', 1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday'
    })
    
    return byday_casual

def create_byday_reg(df):
    byday_reg = day_df.groupby(by="weekday").registered.sum().reset_index()
    byday_reg["weekday"] = byday_reg["weekday"].map({
    0:'Sunday', 1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday'
    })
    
    return byday_reg

def create_byweather(df):
    byweather = hour_df.groupby(by="weathersit").cnt.mean().reset_index()
    byweather["weathersit"] = byweather["weathersit"].map({1: 'Very Good', 2: 'Good', 3: 'Bad', 4: 'Very Bad'})

    
    return byweather

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    st.image("https://raw.githubusercontent.com/feminabilav/Dicoding_FP/main/DAY.png")
    
    start_date, end_date = st.date_input(
        label='Choose Range of Date',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))] 

bymonth = create_bymonth(day_df)
byday_casual = create_byday_casual(day_df)
byday_reg = create_byday_reg(day_df)
byweather = create_byweather(hour_df)

st.header('Dicoding Final Project with Bike Sharing Dataset :technologist:')

st.subheader('User in Time')

col1, col2 = st.columns(2)
 
with col1:
    total_user_casual = byday_casual.casual.sum()
    st.metric("Total Casual User", value=total_user_casual)

    fig, ax = plt.subplots(figsize=(16, 8))
    plt.bar(byday_casual["weekday"], byday_casual["casual"])
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_title("Casual User by Days", loc="center", fontsize=20)
 
    st.pyplot(fig)
 
with col2:
    total_user_reg = byday_reg.registered.sum()
    st.metric("Total Registered User", value=total_user_reg)

    fig, ax = plt.subplots(figsize=(16, 8))
    plt.bar(byday_reg["weekday"], byday_reg["registered"])
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    ax.set_title("Registered User by Days", loc="center", fontsize=20)
 
    st.pyplot(fig)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    bymonth["mnth"],
    bymonth["cnt"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Total User per Month (2012)", loc="center", fontsize=20)
 
st.pyplot(fig)

st.subheader('User in Weather')

col1, col2, col3 = st.columns(3)
with col1:
    mean_temp = round(day_df.temp.mean(), 2)
    st.metric("Average Temperature", value=mean_temp)

with col2:
    mean_hum = round(day_df.hum.mean(), 2)
    st.metric("Average Humidity", value=mean_hum)

with col3:
    mean_wind = round(day_df.windspeed.mean(), 2)
    st.metric("Average Wind Speed", value=mean_wind)


fig, ax = plt.subplots(figsize=(16, 8))
plt.bar(byweather["weathersit"], byweather["cnt"])
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
ax.set_title("Average Hourly User by Weather", loc="center", fontsize=20)
 
st.pyplot(fig)