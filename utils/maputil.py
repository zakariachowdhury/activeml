import pydeck as pdk

MAPBOX_STYLES = ['light-v10', 'dark-v10', 'streets-v11', 'satellite-v9', 'satellite-streets-v11']

def get_mapbox_styles():
    return MAPBOX_STYLES

def get_mapbox_map(data, lat_col, lon_col, lat, lon, zoom=11, pitch=50, radius=100, style=MAPBOX_STYLES[0]):
    return pdk.Deck(
        map_style="mapbox://styles/mapbox/" + style,
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": pitch,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=[lon_col, lat_col],
                radius=radius,
                elevation_scale=4 if pitch > 0 else 0,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    )