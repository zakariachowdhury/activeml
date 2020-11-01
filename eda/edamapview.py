import streamlit as st
import numpy as np
import maputil

LABEL_LATITUDE_COLUMN = 'Latitude Column'
LABEL_LONGITUDE_COLUMN = 'Longitude Column'
LABEL_ZOOM = 'Zoom'
LABEL_PITCH = 'Pitch'
LABEL_STYLE = 'Style'
LABEL_RADIUS = 'Radius'

import commonutil

def generate_map_view(df):
    lat_col = lon_col = None
    columns = list(df.columns)
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        lat_col = st.selectbox(LABEL_LATITUDE_COLUMN, [''] + columns, commonutil.find_index_from_list(columns, 'lat') + 1)
        zoom = st.number_input(LABEL_ZOOM, 1, 20, 11)
    with col2:
        lon_col = st.selectbox(LABEL_LONGITUDE_COLUMN, [''] + columns, commonutil.find_index_from_list(columns, 'lon') + 1)
        pitch = st.number_input(LABEL_PITCH, 0, 100, 50)
    with col3:
        map_style = st.selectbox(LABEL_STYLE, maputil.get_mapbox_styles())
        radius = st.number_input(LABEL_RADIUS, 1, 1000000, 100)

    
    if lat_col is not '' and lon_col is not '':
        midpoint = (np.average(df[lat_col]), np.average(df[lon_col]))
        st.write(maputil.get_mapbox_map(df, lat_col, lon_col, midpoint[0], midpoint[1], zoom=zoom, pitch=pitch, radius=radius, style=map_style))