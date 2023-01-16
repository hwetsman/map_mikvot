

from pyproj import Transformer
from pyproj import CRS
import pyproj
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium


def Get_Lat_Long(x, y):
    lat, long = transformer.transform(x, y)
    return lat, long


# set streamlit options
st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

# set israel grid to lat/long fudge factors and Transformer settings
transformer = Transformer.from_crs("EPSG:6991", "EPSG:4326")
israel_long_fudge = .52
israel_lat_fudge = 4.51

# get data
data = pd.read_csv('new_map_data.csv')
data.rename(columns={'Map Ref. Point (Long.)': 'x',
                     'Map Ref. Point (Lat.)': 'y',
                     'No.': 'num'}, inplace=True)
data['Persian'] = 0

# create sidebar instructions
st.sidebar.write('Instructions for using this site:')
instructions = """\nFrom this sidebar, choose the level of zoom, the era to map, and whether or not you would like to include undated mikvot."""
st.sidebar.write(instructions)

# create good OIG coordinates
data['x'] = data.x*100
data['y'] = data.y*100

# create era dict
era_dict = {'Persian': -540, 'Hellenistic': -330, 'Early Roman 1': -50, 'Early Roman 2': 70,
            'Middle Roman': 135, 'Late Roman': 250, 'Byzantine': 350, 'Islamic': 650}

# iterate data to transform to lat/long
for i, r in data.iterrows():
    x = data.loc[i, 'x']
    y = data.loc[i, 'y']
    latitude, longitude = Get_Lat_Long(x, y)
    data.loc[i, 'longitude'] = longitude + israel_long_fudge
    data.loc[i, 'latitude'] = latitude + israel_lat_fudge

data.rename(columns={'lat': 'old_lat', 'long': 'old_long'}, inplace=True)
data.rename(columns={'latitude': 'lat', 'longitude': 'long'}, inplace=True)

# get user inputs
undated = st.sidebar.radio('Include undated mikvot?', ['No', 'Yes'])
zlevel = st.sidebar.slider('Choose level of zoom', min_value=0, max_value=10, value=8)
era = st.sidebar.select_slider('Choose an Era', list(era_dict.keys()))
st.sidebar.write('\nData from Dr Yonatan Adler, Ariel University, Israel')
# col1.title(era)

undated_df = data[data['Period'].isnull()]
# st.write(undated_df.shape)
# data = data[data['year'] <= year]
if era == 'Byzantine':
    df = data[data['Byz'] == 1]
    col2.title('The Byzantine Period')
    col2.write('\nThe Byzantine period dates from years 350 to 650 of the common era.')
    # st.write(df.shape)
elif era == 'Late Roman':
    df = data[data['LR'] == 1]
    col2.title('The Late Roman Period')
    col2.write('\nThe Late Roman period dates from years 250 to 350 of the common era.')
    # st.write(df.shape)
elif era == 'Middle Roman':
    df = data[data['MR'] == 1]
    col2.title('The Middle Roman Period')
    col2.write('\nThe Middle Roman period dates from years 135 to 250 of the common era.')
    # st.write(df.shape)
elif era == 'Early Roman 2':
    df = data[data['ER II'] == 1]
    col2.title('The Early Roman Period 2')
    col2.write('\nThe second half of the Early Roman period dates from destruction of the Temple in year 70 to year 135 of the common era.')
    # st.write(df.shape)
elif era == 'Early Roman 1':
    df = data[data['ER I'] == 1]
    col2.title('The Early Roman Period 1')
    col2.write('\nThe first half of the Early Roman period dates from 50 years befor the common era to the destruction of the Temple in the year 70 of the common era.')
elif era == 'Hellenistic':
    col2.title('The Hellenistic Period')
    df = data[data['Hel'] == 1]
    col2.write('\nThe Hellenistic period dates from years 100 to 50 before the common era.')
elif era == 'Persian':
    col2.title('The Persian Period')
    df = data[data['Persian'] == 1]
    col2.write('\nThe Persian period dates from about year 540 to year 100 before the common era. There are no mikvot dated to this period.')
else:
    df = data[data['Islm'] == 1]
    col2.title('The Islamic Period')
    col2.write('\nThe Islamic period is after year 650 of the common era.')

# else:
#     df = data.copy()
if undated == 'Yes':
    df = df.append(undated_df)
# st.write(df.shape)


m = folium.Map(location=[31.7857, 35.2007], zoom_start=zlevel,
               tiles='cartodb positron')  # tiles='Stamen Watercolor')

# Add a marker to the map
for i, r in df.iterrows():
    lat = df.loc[i, 'lat']
    long = df.loc[i, 'long']
    name = df.loc[i, 'num']
    marker = folium.CircleMarker(location=[lat, long], popup=name, color='red', radius=1).add_to(m)

with col1:
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
