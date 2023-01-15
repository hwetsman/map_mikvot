

import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium


# pays = countries.get('USA').alpha2.lower()
st.set_page_config(layout="wide")
# url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
data = pd.read_csv('map_data.csv')

st.write(data.head())
era_dict = {'Hellenistic': -100, 'Early Roman 1': -50, 'Early Roman 2': 70,
            'Middle Roman': 135, 'Late Roman': 250, 'Byzantine': 350, 'Islamic': 650}
# data = pd.DataFrame({'lat': [31.7857, 31.9, 32.2, 31.6],
#                      'lon': [35.2007, 35.1007, 35.15, 35.2],
#                      'name': ['mikvah1', 'mikvah2', 'mikvah3', 'mikvah4'],
#                      'year': [-130, -125, -25, 25]})
# lines = data.shape[0]
# get user inputs
undated = st.sidebar.radio('Include undated mikvaot?', ['Yes', 'No'])
zlevel = st.sidebar.slider('Choose level of zoom', min_value=0, max_value=10, value=8)
era = st.select_slider('Choose an Era', list(era_dict.keys()))

st.title(era)

undated_df = data[data['Earliest'].isnull()]
# data = data[data['year'] <= year]
if era == 'Byzantine':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in ['Islamic']])]
    # st.write(df.shape)
elif era == 'Late Roman':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in [
        'Islamic', 'Byzantine']])]
    # st.write(df.shape)
elif era == 'Middle Roman':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in [
        'Islamic', 'Byzantine', 'Late Roman']])]
    # st.write(df.shape)
elif era == 'Early Roman 2':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in
                                     ['Islamic', 'Byzantine', 'Late Roman', 'Middle Roman']])]
    # st.write(df.shape)
elif era == 'Early Roman 1':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in
                                     ['Islamic', 'Byzantine', 'Late Roman', 'Middle Roman', 'Early Roman 2']])]
    # st.write(df.shape)
elif era == 'Hellenistic':
    df = data[data['Earliest'].isin([x for x in list(era_dict.keys()) if x not in
                                     ['Islamic', 'Byzantine', 'Late Roman', 'Middle Roman', 'Early Roman 2', 'Early Roman 1']])]
    # st.write(df.shape)
else:
    df = data.copy()
if undated == 'Yes':
    df = df.append(undated_df)


m = folium.Map(location=[31.7857, 35.2007], zoom_start=zlevel, tiles='Stamen Watercolor')

# Add a marker to the map
for i, r in data.iterrows():
    lat = data.loc[i, 'lat']
    long = data.loc[i, 'lon']
    name = data.loc[i, 'name']
    # marker = folium.Marker([lat, long], popup=name).add_to(m)
    marker = folium.CircleMarker(location=[lat, long], popup=name, color='red', radius=1).add_to(m)

    # Add hover text to the marker
    # hover = folium.Html(f'<b>{name}</b>', script=True)
    # st.write(hover)
    # marker.add_child(hover)
    # st.write(marker)
    # marker.add_to(m)
    # st.write(m)
# st.pydeck_chart(m._repr_html_())
st_data = st_folium(m)
# st.write(m)


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
