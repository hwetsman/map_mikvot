

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

# create era dict
era_dict = {'Persian': -540, 'Hellenistic': -330, 'Early Roman 1': -50, 'Early Roman 2': 70,
            'Middle Roman': 135, 'Late Roman': 250, 'Byzantine': 350, 'Islamic': 650}

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
tile = st.sidebar.selectbox('Choose a map tile', ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'Cartodb Positron',
                                                  'Cartodb dark_matter'], index=4)
undated = st.sidebar.radio('Include undated mikvot?', ['No', 'Yes'])
zlevel = st.sidebar.slider('Choose level of zoom', min_value=0, max_value=10, value=8)
era = st.sidebar.select_slider('Choose an Era', list(era_dict.keys()))
st.sidebar.write('\nData from Dr Yonatan Adler, Ariel University, Israel')

# create good OIG coordinates
data['x'] = data.x*100
data['y'] = data.y*100

# iterate data to transform to lat/long
for i, r in data.iterrows():
    x = data.loc[i, 'x']
    y = data.loc[i, 'y']
    latitude, longitude = Get_Lat_Long(x, y)
    data.loc[i, 'long'] = longitude + israel_long_fudge
    data.loc[i, 'lat'] = latitude + israel_lat_fudge

undated_df = data[data['Period'].isnull()]

col2.write("""A mikveh (Hebrew plural: mikvot) is a Jewish ritual bath used
to restore spiritual purification. Mikvot are stepped immersion pools and quite
common in the archeological record of ancient Judea. In the ancient Near East, mikvot
 are only found at sites occupied by Judeans. As such pools are not costless to
 build and maintain, the question arises of where and when did Judeans begin to
 feel the need expend resources in order to follow biblical commandments on ritual purity.""")
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

if undated == 'Yes':
    df = df.append(undated_df)

m = folium.Map(location=[31.7857, 35.2007], zoom_start=zlevel,
               tiles=tile)

# Add markers to the map
for i, r in df.iterrows():
    lat = df.loc[i, 'lat']
    long = df.loc[i, 'long']
    name = df.loc[i, 'num']
    marker = folium.CircleMarker(location=[lat, long], popup=name, color='red', radius=1).add_to(m)

# display map
with col1:
    st_data = st_folium(m)
