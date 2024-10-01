import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style = 'dark')

def get_total_count_by_hour_df(df_hour):
  df_hour_count = df_hour.groupby(by = "hour").agg({"count_customer": ["sum"]})
  return df_hour_count

def count_by_day_df(df_day):
    df_day_count_2011 = df_day.query(str('date >= "2011-01-01" and date < "2012-12-31"'))
    return df_day_count_2011

def total_registered_df(df_day):
   df_reg = df_day.groupby(by = "date").agg({
      "registered": "sum"
    })
   df_reg = df_reg.reset_index()
   df_reg.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return df_reg

def total_casual_df(df_day):
   df_cas =  df_day.groupby(by = "date").agg({
      "casual": ["sum"]
    })
   df_cas = df_cas.reset_index()
   df_cas.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return df_cas

def sum_order (df_hour):
    df_sum_order_items = df_hour.groupby("hour").count_customer.sum().sort_values(ascending = False).reset_index()
    return df_sum_order_items

def type_of_season (df_day): 
    df_season = df_day.groupby(by = "season").count_customer.sum().reset_index() 
    return df_season

def situation_of_weather (df_day): 
    df_weather = df_day.groupby(by = "weather_situation").count_customer.sum().reset_index() 
    return df_weather

def type_of_day (df_day): 
    df_type_day = df_day.groupby(by = "type_of_day").count_customer.sum().reset_index() 
    return df_type_day

def days (df_day): 
    day_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    df_daily = df_day.groupby(by = "day").count_customer.sum().reset_index()
    df_daily["day"] = pd.Categorical(df_daily["day"], categories = day_order, ordered = True)
    return df_daily

def months (df_day): 
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    df_monthly = df_day.groupby(by = "month").count_customer.sum().reset_index()
    df_monthly["month"] = pd.Categorical(df_monthly["month"], categories = month_order, ordered = True)
    return df_monthly

df_days = pd.read_csv("C:/Users/HP/Downloads/dashboard/df_day_clean.csv")
df_hours = pd.read_csv("C:/Users/HP/Downloads/dashboard/df_hour_clean.csv")

datetime_columns = ["date"]
df_days.sort_values(by = "date", inplace = True)
df_days.reset_index(inplace = True)   

df_hours.sort_values(by = "date", inplace = True)
df_hours.reset_index(inplace = True)

for column in datetime_columns:
    df_days[column] = pd.to_datetime(df_days[column])
    df_hours[column] = pd.to_datetime(df_hours[column])

min_date_days = df_days["date"].min()
max_date_days = df_days["date"].max()

min_date_hour = df_hours["date"].min()
max_date_hour = df_hours["date"].max()

with st.sidebar:
    st.image("https://th.bing.com/th/id/OIP.5AlvCvzlu7du8A33M6LpUQAAAA?rs=1&pid=ImgDetMain")
    
    start_date, end_date = st.date_input(
        label = 'Timeline',
        min_value = min_date_days,
        max_value = max_date_days,
        value = [min_date_days, max_date_days])
  
main_df_days = df_days[(df_days["date"] >= str(start_date)) & 
                       (df_days["date"] <= str(end_date))]

main_df_hour = df_hours[(df_hours["date"] >= str(start_date)) & 
                        (df_hours["date"] <= str(end_date))]

df_hour_count = get_total_count_by_hour_df(main_df_hour)
df_day_count_2011 = count_by_day_df(main_df_days)
df_reg = total_registered_df(main_df_days)
df_cas = total_casual_df(main_df_days)
df_sum_order_items = sum_order(main_df_hour)
df_season = type_of_season(main_df_days)
df_weather = situation_of_weather(main_df_days)
df_type_day = type_of_day(main_df_days)
df_daily = days(main_df_days)
df_monthly = months(main_df_days)

# Visualisasi Data 
st.header('Bike Sharing Performance Analysis')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = df_day_count_2011.count_customer.sum()
    st.metric("Total Customer", value = total_orders)

with col2:
    total_sum = df_reg.register_sum.sum()
    st.metric("Total Registered", value = total_sum)

with col3:
    total_sum = df_cas.casual_sum.sum()
    st.metric("Total Casual", value = total_sum)

st.subheader("Performa Bisnis Penyewaan Sepeda Selama Beberapa Tahun Terakhir")
month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
monthly_counts = df_days.groupby(by=['month', 'year']).agg({'count_customer': 'sum'}).reset_index()
monthly_counts['month'] = pd.Categorical(monthly_counts['month'], categories = month_order, ordered = True)
monthly_counts.sort_values(by = ['year', 'month'], inplace = True)
fig, ax = plt.subplots(figsize=(10, 5))
for year in monthly_counts['year'].unique():
    yearly_data = monthly_counts[monthly_counts['year'] == year]
    yearly_data = yearly_data.sort_values(by = 'month')
    ax.plot(yearly_data['month'], yearly_data['count_customer'], marker = 'o', linewidth = 2, label = f'{year}')

ax.set_ylabel('Count', fontsize = 20)
ax.set_xlabel(None)
ax.tick_params(axis = 'y', labelsize = 20)
ax.tick_params(axis = 'x', labelsize = 20)
ax.legend(title = 'Year', loc = 'upper right', fontsize = 12)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Pengaruh Kondisi Cuaca dan Musim terhadap Jumlah Penyewaan Sepeda")
colors = ["pink", "skyblue", "skyblue", "skyblue"]
fig, ax = plt.subplots(figsize = (15, 10))
sns.barplot(data = df_season.sort_values(by = "season"), x = "season", y = "count_customer",
            palette = colors, ax = ax)
ax.set_title("Grafik Antar Musim", loc = "center", fontsize = 30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis = 'x', labelsize = 35)
ax.tick_params(axis = 'y', labelsize = 30)
st.pyplot(fig)

colors = ["skyblue", "skyblue", "pink"]
fig, ax = plt.subplots(figsize = (15, 10))
sns.barplot(data=df_weather.sort_values(by = "weather_situation", ascending = False), x = "weather_situation",
            y = "count_customer", palette = colors, ax = ax)
ax.set_title("Grafik Kondisi Cuaca", loc = "center", fontsize = 30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize = 35)
ax.tick_params(axis='y', labelsize = 30)
st.pyplot(fig)

st.subheader("Perbandingan Jumlah Penyewaan Sepeda antara Hari Kerja dan Akhir Pekan")
colors = ["skyblue", "pink"]
fig, ax = plt.subplots(figsize = (15, 10))
sns.barplot(data = df_type_day.sort_values(by = "type_of_day", ascending = False), x = "type_of_day",
            y = "count_customer", palette = colors, ax = ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis = 'x', labelsize = 35)
ax.tick_params(axis = 'y', labelsize = 30)
st.pyplot(fig)

st.subheader("Pengaruh Pola Waktu terhadap Jumlah Penyewaan Sepeda")
fig, axes = plt.subplots(1, 2, figsize = (10, 6))
sns.barplot(data = df_sum_order_items.head(5), x = "hour", y = "count_customer",
            palette = ["skyblue", "skyblue", "pink", "skyblue", "skyblue"], ax = axes[0], legend = False)
axes[0].set_title("Jam Operasional dengan Jumlah Penyewaan Tertinggi")
axes[0].set_xlabel("Hours")
axes[0].set_ylabel("Count")

sns.barplot(data = df_sum_order_items.tail(5), x = "hour",
            y = "count_customer", palette = ["skyblue", "skyblue", "skyblue", "pink", "skyblue"], ax = axes[1], legend = False)
axes[1].set_title("Jam Operasional dengan Jumlah Penyewaan Terendah")
axes[1].set_xlabel("Hours")
axes[1].set_ylabel("Count")
plt.tight_layout()
st.pyplot(fig)

fig, ax = plt.subplots(figsize = (15, 10))
sns.barplot(data = df_monthly.sort_values(by = "month", ascending = False), x = "month",
            y = "count_customer", palette = ["skyblue"], ax = ax)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Bulan", fontsize = 30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis = 'x', labelsize = 20)
ax.tick_params(axis = 'y', labelsize = 20)
st.pyplot(fig)

fig, ax = plt.subplots(figsize = (15, 10))
sns.barplot(data = df_daily.sort_values(by = "day", ascending = False), x = "day",
            y = "count_customer", palette = ["pink"], ax = ax)
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Hari", fontsize = 30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis = 'x', labelsize = 20)
ax.tick_params(axis = 'y', labelsize = 20)
st.pyplot(fig)

st.subheader("Perbandingan Jumlah Penyewa Registered dan Casual")
labels = "Casual", "Registered"
sizes = [18.8, 81.2] 
fig, ax = plt.subplots()
ax.pie(sizes, labels = labels, autopct = '%1.1f%%', colors = ["pink", "skyblue"], startangle = 90)
ax.axis("equal")  
st.pyplot(fig)