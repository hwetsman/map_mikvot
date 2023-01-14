import matplotlib.animation as ani
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from iso3166 import countries
import matplotlib.image as mpimg
import streamlit as st


# pays = countries.get('USA').alpha2.lower()

# url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
# data = pd.read_csv('map_data.csv')
data = pd.DataFrame({'lat': [29.95, 29.9, 30.0, 29.97], 'lon': [-90.0, -
                    89.96, -90.1, -90.05], 'name': ['mikvah1', 'mikvah2', 'mikvah3', 'mikvah4'],
                    'year': [-130, -125, -25, 25]})
lines = data.shape[0]
print(data)
zlevel = st.sidebar.slider('Choose level of zoom', min_value=0, max_value=10, value=7)
year = st.sidebar.slider('Choose year to view', min_value=-250, max_value=150, value=0)
data = data[data['year'] <= year]
st.map(data=data, zoom=zlevel, use_container_width=True)

# data['Year'] = pd.to_datetime(data['Year'], format='%Y')
# data.set_index('Year', inplace=True)
# data = data.resample('M').mean().interpolate()
# data.reset_index(inplace=True, drop=False)
# data.Year = data.Year.astype(str)
# data['Date'] = data.Year.str[0:4].astype(int)
# data.drop('Year', inplace=True, axis=1)
# data = data[['Date','GBP %', 'USD %', 'FRF %', 'DEM %', 'JPY %', 'EUR %', 'Other %',
#              'RMB %', 'Gold %', 'Check', 'ALL FX %', 'OTHER FX %   (JPY, Other, RMB)']
# print(data)
# data.rename(columns={'Date': 'Year', 'GBP %': 'Sterling', 'USD %': 'Dollar', 'FRF %': 'Franc', 'DEM %': 'D-Mark',
#                      'JPY %': 'Yen', 'EUR %': 'Euro', 'Other %': 'Other FX', 'RMB %': 'Yuan', 'Gold %': 'Gold', 'OTHER FX % (JPY, Other, RMB)': 'Other FX'}, inplace=True)
# asset_colors = {'Sterling': 'blue', 'Dollar': 'blue', 'Franc': 'blue', 'D-Mark': 'blue', 'Yen': 'blue',
#                 'Euro': 'blue', 'Other FX': 'blue', 'Yuan': 'blue', 'Gold': 'goldenrod'}
#
# data = data.drop(['ALL FX %', 'OTHER FX %   (JPY, Other, RMB)', 'Check'], axis=1)
# data.insert(0, 'Year', data.pop('Year'))
# print(data)
# print(data.columns)
# 1/0
# non_labels = ['Check']
# labels = [x for x in data.columns if x not in non_labels]
# print(data)
# data['Check'] = data.sum(axis=1)-data.Year
# fig, ax = plt.subplots(figsize=(17, 7))
# df = data[labels]
#
# print(df)
#
# plt.xticks(rotation=45, ha="right", rotation_mode="anchor")  # rotate the x-axis values
# plt.subplots_adjust(bottom=0.2, top=0.9)  # ensuring the dates (on the x-axis) fit in the screen
# left, width = .25, .6
# bottom, height = .18, .5
# right = left + width
# top = bottom + height


# def buildmebarchart(i=int):
#     # plt.legend(df.columns)
#     ax.clear()  # clear last year
#     data = df.loc[i]  # select the next year's data
#     year = data.values[0]  # get year
#     data = data[1:].sort_values()  # drop year and put values in order
#     max_x = data.values.max()
#     plt.suptitle('Global International Reserves in Percentages')
#     ax.text(right, bottom, int(year),
#             horizontalalignment='right',
#             verticalalignment='bottom',
#             transform=ax.transAxes, font='Avenir', fontsize=100, c='lightgray', fontweight='bold')
#     ax.text(right, bottom-.25, '100%',
#             horizontalalignment='right',
#             verticalalignment='bottom',
#             transform=ax.transAxes, font='Avenir', fontsize=100, c='lightgray', fontweight='bold')
#     for i, v in enumerate(data):
#         ax.text(v+.001, i-.02, str(f'-{round(100*v,1)}%'), color='black', font='Avenir')
#     vlines = [.1, .2, .3, .4, .5, .6, .7]
#     lines = [x for x in vlines if x < max_x]
#     plt.vlines(lines, 0, 8, color='black')
#     plt.barh(data.index, data.values, label=data.index,
#              color=[asset_colors[key]for key in data.index])
#
#
# animator = ani.FuncAnimation(fig, buildmebarchart, interval=288)
#
# plt.show()
