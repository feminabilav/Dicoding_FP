import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from babel.numbers import format_currency

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
    
    return byday_casual

def create_byday_reg(df):
    byday_reg = day_df.groupby(by="weekday").registered.sum().reset_index()
    
    return byday_reg

def create_byweather(df):
    byweather = hour_df.groupby(by="weathersit").cnt.mean().reset_index()
    
    return byweather

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()
 
# with st.sidebar:

#     start_date, end_date = st.date_input(
#         label='Rentang Waktu', 
#         min_value=min,
#         max_value=max,
#         value=[min, max]
#     )

# main = day_df[(day_df["dteday"] >= str(start_date)) & (day_df["dteday"] <= str(end_date))]

bymonth = create_bymonth(day_df)
byday_casual = create_byday_casual(day_df)
byday_reg = create_byday_reg(day_df)
byweather = create_byweather(hour_df)

st.header('Dicoding Final Project with Bike Sharing Dataset :technologist:')

plt.figure(figsize=(10, 5))
plt.plot(
    bymonth["mnth"],
    bymonth["cnt"],
    marker='o', 
    linewidth=2,
    color="#72BCD4"
)
plt.title("Total User per Month (2012)", loc="center", fontsize=20)

plt.show()