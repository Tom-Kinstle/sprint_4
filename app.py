import streamlit as st
import pandas as pd
import plotly.express as pl

df = pd.read_csv('vehicles_us.csv')


st.markdown("<h1 style='text-align: center;'>EDA Car Advertisement</h1>", unsafe_allow_html=True)
st.markdown('**Discovery of sales and customer trends in vehicle purchases.**')

#upload = st.file_uploader('Upload file here')
#st.write(df.info())
#Clean data
df['date_posted'] = pd.to_datetime(df['date_posted'])
df['model_year'] = df['model_year'].fillna(9999).astype(int)
df['odometer'] = df['odometer'].fillna(999999).astype(int)
df['paint_color'] = df['paint_color'].astype('str', errors='ignore')
#drop unessary columns and rows
df = df.drop(['cylinders', 'fuel', 'transmission', 'is_4wd'], axis=1)
df = df.drop_duplicates()
# drop duplicate values
df['type'] = df['type'].replace({'pickup': 'truck'})
df['type'] = df['type'].replace({'offroad': 'SUV'})

df_clean =df

st.write(df_clean.head())
st.markdown("<h1 style='text-align: center;'>Modeling data</h1>", unsafe_allow_html=True)

#average price by vehicle type
avg_type = df.groupby('type')['price'].mean().reset_index()
avg_type = avg_type.sort_values(by='price', ascending=True)

# average price by model year
avg_year = df.groupby('model_year')['price'].mean().reset_index()

# removed extreme values for year to prevent data being skewed
avg_year = avg_year[(avg_year['model_year'] <= 2020) & (avg_year['model_year'] >= 1995)]

# average price by condition 
avg_condition = df.groupby('condition')['price'].mean().reset_index()
avg_condition = avg_condition.sort_values(by='price', ascending=True)
# Create bar charts
fig1 = pl.bar(avg_type, x='type', y='price', title='Average Price by Vehicle Type',  color_discrete_sequence=['#33ccff'], labels={'type': 'Vehicle Type', 'price': 'Average Price'})
fig1.update_traces(marker_line_color='black', marker_line_width=1.5)

fig2 = pl.bar(avg_year, x='model_year', y='price', title='Average Price by Model Year',  color_discrete_sequence=['#8585e0'], labels={'model_year': 'Model Year', 'price': 'Average Price'})
fig2.update_traces(marker_line_color='black', marker_line_width=1.5)

fig3 = pl.bar(avg_condition, x='condition', y='price', title='Average Price by Condition',  color_discrete_sequence=['#b300b3'], labels={'model_year': 'Model Year', 'price': 'Average Price'})
fig3.update_traces(marker_line_color='black', marker_line_width=1.5)


st.plotly_chart(fig3)
st.plotly_chart(fig1)
st.plotly_chart(fig2)


# average days listed by type
avg_days_listed_type = df.groupby('type')['days_listed'].mean().reset_index()
avg_days_listed_type = avg_days_listed_type[avg_days_listed_type['type'] != 'other']
# average days listed by model year
avg_year_days = df.groupby('model_year')['days_listed'].mean().reset_index()
avg_year_days = avg_year_days.sort_values(by='days_listed', ascending=False)
avg_days_listed_year = avg_year_days.groupby('model_year')['days_listed'].mean().reset_index()
avg_days_listed_year = avg_days_listed_year[(avg_days_listed_year['model_year'] <= 2020) & (avg_days_listed_year['model_year'] >= 1995)]

# average days listed by color
avg_days_listed_color = df.groupby('paint_color')['days_listed'].mean().reset_index()

# average days listed by condition
avg_days_listed_condition = df.groupby('condition')['days_listed'].mean().reset_index()

# create scatter plots
fig1 = pl.scatter(avg_days_listed_type, x='type', y='days_listed', title='Average Days Listed by Vehicle Type', labels={'days_listed': 'Days Listed', 'type': 'Vehicle Type'})
fig1.update_traces(marker=dict(size=30, color='#33ccff'))
fig1.update_traces(marker_line_color='black', marker_line_width=2.5)

fig2 = pl.scatter(avg_days_listed_year, x='model_year', y='days_listed', title='Average Days Listed by Model Year', labels={'days_listed': 'Days Listed', 'model_year': 'Model Year'})
fig2.update_traces(marker=dict(size=30, color='#8585e0'))
fig2.update_traces(marker_line_color='black', marker_line_width=2.5)

fig3 = pl.scatter(avg_days_listed_color, x='paint_color', y='days_listed', title='Average Days Listed by Paint Color', labels={'days_listed': 'Days Listed', 'paint_color': 'Paint Color'})
fig3.update_traces(marker=dict(size=30, color='#ff0066', line=dict(color='black', width=2.5)))

# Create scatter plot for average days listed by condition
fig4 = pl.scatter(avg_days_listed_condition, x='condition', y='days_listed', title='Average Days Listed by Condition', labels={'days_listed': 'Days Listed', 'condition': 'Vehicle Condition'})
fig4.update_traces(marker=dict(size=30, color= '#ffff00', line=dict(color='black', width=2.5)))

st.plotly_chart(fig4)
st.plotly_chart(fig3)
st.plotly_chart(fig1)
st.plotly_chart(fig2)




#if st.checkbox('Show Average Days Listed by Vehicle Type'):
    #st.plotly_chart(fig1)

#if st.checkbox('Show Average Days Listed by Model Year'):
    #st.plotly_chart(fig2)

#if st.checkbox('Show Average Days Listed by Paint Color'):
    #st.plotly_chart(fig3)

#if st.checkbox('Show Average Days Listed by Condition'):
    #st.plotly_chart(fig4)

 # Filter average days listed by prices, for vehicles less than 60 days
avg_days_listed_price = df.groupby('price')['days_listed'].mean().reset_index()
avg_days_listed_price = avg_days_listed_price[avg_days_listed_price['days_listed'] <= 60]

# distribution of vehicles price more than 20,000 by days, and less 60 days
avg_days_listed_price_above_20000 = avg_days_listed_price[avg_days_listed_price['price'] >= 20000]

# distribution of vehicles price less than 20,000 by days, and less 60 days
avg_days_listed_price_below_20000 = avg_days_listed_price[avg_days_listed_price['price'] < 20000]

# create histograms
fig1 = pl.histogram(avg_days_listed_price_above_20000, x='days_listed', nbins=30, title='Average Days Vehicles Listed Above 20,000 Dollars', labels={'days_listed': 'Average Days Listed'}, color_discrete_sequence=['#33ccff'])

fig1.update_traces(marker_line_color='black', marker_line_width=1.5)
fig1.update_yaxes(range=[0, 160])

fig2 = pl.histogram(avg_days_listed_price_below_20000, x='days_listed', nbins=30, title='Average Days Vehicles Listed Below 20,000 Dollars', labels={'days_listed': 'Average Days Listed'}, color_discrete_sequence=['#8585e0'])

fig2.update_traces(marker_line_color='black', marker_line_width=1.5)
fig1.update_yaxes(range=[0, 160])   

if st.checkbox('Show Average Days Vehicles Listed Above 20,000 Dollars'):
    st.plotly_chart(fig1)

if st.checkbox('Show Average Days Vehicles Listed Below 20,000 Dollars'):
    st.plotly_chart(fig2)