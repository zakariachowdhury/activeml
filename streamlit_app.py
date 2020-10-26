from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

APP_TITLE = "Exploratory Data Analysis"

GROUP_BASIC = 'Basic Analysis'
GROUP_CATEGORICAL = 'Categorical Analysis'
GROUP_NUMERICAL = 'Numerical Analysis'
GROUP_BIVARIATE = 'Bivariate Analysis'
GROUP_MULTIVARIATE = 'Multivariate Analysis'
GROUP_MAP = 'Map View'

ANALYSIS_GROUP = [
    GROUP_BASIC,
    GROUP_CATEGORICAL,
    GROUP_NUMERICAL,
    GROUP_BIVARIATE,
    GROUP_MULTIVARIATE,
    GROUP_MAP
]

DATA_SOURCE_FILE = "File"
DATA_SOURCE_URL = "URL"
DATA_SOURCE_DEMO = "Demo"
DATA_SOURCES = [
    DATA_SOURCE_FILE,
    DATA_SOURCE_URL,
    DATA_SOURCE_DEMO
]

DATA_MAX_N_ROWS = 100000
DATA_CSV_SEPERATORS = [',', ';', ':', '|', r'\t']

DEMO_DATASETS = {
    '': {
        'url': ''
    },
    'Iris': {
        'url': 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv',
        'nrows': 150,
        'sep': ','
    },
    'Uber': {
        'url': 'https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz',
        'nrows': 10000,
        'sep': ','
    },
    'US Sate Population': {
        'url': 'https://raw.githubusercontent.com/jakevdp/data-USstates/master/state-population.csv',
        'nrows': 3000,
        'sep': ','
    }
}

MAPBOX_STYLES = ['light-v10', 'dark-v10', 'streets-v11', 'satellite-v9', 'satellite-streets-v11']

@st.cache
def load_data(file, nrows=None, sep=','):
    data = pd.read_csv(file, nrows=nrows, sep=sep)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def view_data(df, checkbox_key=None):
    if df is not None:
        section_title('Shape')
        df.shape

        section_title('Head')
        df[:5]

        if st.checkbox("View All", key=checkbox_key):
            df

def st_plot(plot):
    try:
        st.pyplot(plot.get_figure(), clear_figure=True)
    except Exception as e:
        st.error(e)

def section_title(text):
    st.markdown(f'*{text}*:')

def view_map(data, lat_col, lon_col, lat, lon, zoom, style_name):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/"+style_name,
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=[lon_col, lat_col],
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))

def main():
    df = None
    selected_analysis_group = []
    categorical_columns = None
    nummeric_columns = None
    date_columns = None

    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_TITLE)

    with st.beta_expander("Load Data", True):
        dataset_source = st.selectbox('Data Source:', DATA_SOURCES)
        
        file = None
        nrows = DATA_MAX_N_ROWS

        if dataset_source == DATA_SOURCE_DEMO:
            dataset_name = st.selectbox('Demo Dataset:', list(DEMO_DATASETS.keys()))
            if len(dataset_name):
                file = DEMO_DATASETS[dataset_name]['url']
                nrows = DEMO_DATASETS[dataset_name]['nrows']
                sep = DEMO_DATASETS[dataset_name]['sep']

        if dataset_source != DATA_SOURCE_DEMO:
            col1, col2 = st.beta_columns(2)
            with col1:
                nrows = st.number_input('Number of Rows:', value=nrows)
            with col2:
                sep = st.selectbox('Sepetator:', DATA_CSV_SEPERATORS)
                sep = sep if len(sep) else ','
            nrows = nrows if nrows else None

        if dataset_source == DATA_SOURCE_FILE:
            file = st.file_uploader("Upload File:", type=['csv', 'tsv', 'txt'])

        if dataset_source == DATA_SOURCE_URL:
            file = st.text_input('Dataset URL (csv):')
            if len(file) == 0:
                file = None

        if file is not None:
            try:
                df = load_data(file, nrows, sep)
                view_data(df, 'file')
            except Exception as e:
                st.error(e)
                st.stop()
    
    if df is not None and len(df):
        with st.beta_expander("Process Data"):
            columns = st.multiselect('Columns:', list(df.columns), list(df.columns))
            df = df[columns]
            
            cat_col = df.select_dtypes(include=['object']).columns.tolist()
            num_col = df.select_dtypes(include=np.number).columns.tolist()
            
            date_columns = st.multiselect('Date Columns:', cat_col)
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    st.error(f'Column \'{col}\' cannot be converted to date/time')

            if cat_col is not None and date_columns is not None:
                cat_col = list(set(cat_col) - set(date_columns))

            categorical_columns = st.multiselect('Categorical Columns:', columns, cat_col)
            nummeric_columns = st.multiselect('Numerical Columns:', num_col, num_col)

            section_title('Operations')

            if st.checkbox('Drop Null Values'):
                df.dropna(inplace=True)

            if st.checkbox('Drop Duplicates'):
                df.drop_duplicates(inplace=True)

            if st.checkbox('Reset Index'):
                df.reset_index(drop=True, inplace=True)

            view_data(df, "process")

        with st.sidebar.beta_expander("Analysis", True):
            for group in ANALYSIS_GROUP:
                if st.checkbox(group):
                    selected_analysis_group.append(group)

        if GROUP_BASIC in selected_analysis_group:
            with st.beta_expander(GROUP_BASIC, True):
                section_title('Info')
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())

                section_title('Data Types')
                dtypes = df.dtypes.rename('Total')
                dtypes

                if len(df.columns):
                    section_title('Describe')
                    desc = df.describe().T
                    desc

                section_title('Missing Values')
                isnull = df.isnull().sum().rename('Total')
                isnull

                section_title('Skew')
                skew = df.skew()
                skew
                
                section_title('Covariance')
                cov = df.cov()
                cov
                if len(cov):
                    st_plot(sns.heatmap(cov, annot=True))

                section_title('Correlation')
                corr = df.corr()
                corr
                if len(corr):
                    st_plot(sns.heatmap(corr, annot=True))
        
        if GROUP_CATEGORICAL in selected_analysis_group:
            with st.beta_expander(GROUP_CATEGORICAL, True):
                for col in categorical_columns:
                    section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        count = df[col].value_counts()
                        count

                    with col2:
                        st_plot(sns.countplot(df[col]))

        if GROUP_NUMERICAL in selected_analysis_group:
            with st.beta_expander(GROUP_NUMERICAL, True):
                for col in nummeric_columns:
                    section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        desc = df[col].describe()
                        desc
                    with col2:
                        try:
                            st_plot(sns.distplot(df[col]))
                        except Exception as e:
                            st.error(e)

        if GROUP_BIVARIATE in selected_analysis_group:
            with st.beta_expander(GROUP_BIVARIATE, True):
                for cat_col in categorical_columns:
                    for num_col in nummeric_columns:
                        if cat_col != num_col:
                            col1, col2 = st.beta_columns(2)
                            with col1:
                                desc = df[num_col].describe()
                                desc
                            
                            with col2:
                                st_plot(sns.swarmplot(x=df[cat_col], y=df[num_col]))

                for cat_col in categorical_columns:
                    for num_col in nummeric_columns:
                        if cat_col != num_col:
                            st_plot(sns.boxplot(x=df[cat_col], y=df[num_col]))

        if GROUP_MULTIVARIATE in selected_analysis_group:
            with st.beta_expander(GROUP_MULTIVARIATE, True):
                for x in nummeric_columns:
                    for y in nummeric_columns:
                        if x != y:
                            for z in categorical_columns:
                                st_plot(sns.scatterplot(df[x], df[y], df[z]))

        if GROUP_MAP in selected_analysis_group:
            with st.beta_expander(GROUP_MAP, True):
                lat_col = None
                lon_col = None

                col1, col2, col3 = st.beta_columns(3)
                with col1:
                    lat_col = st.selectbox('Latitude Column', [None] + nummeric_columns)
                with col2:
                    lon_col = st.selectbox('Longitude Column', [None] + nummeric_columns)
                with col3:
                    map_style = st.selectbox('Style', MAPBOX_STYLES)

                if lat_col is not None and lon_col is not None:
                    midpoint = (np.average(df[lat_col]), np.average(df[lon_col]))
                    view_map(df, lat_col, lon_col, midpoint[0], midpoint[1], 11, map_style)

main()