from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path = list(set(['eda', 'data', 'ml', 'utils'] + sys.path))

import dataprocessview
import edamapview
import edacustomplot
import mlsupervised
import viewutil
import commonutil

APP_TITLE = "ActiveML"
APP_ICON = "🔮"

SIDEBAR_GROUP_EDA = "EDA"
SIDEBAR_GROUP_ML = "ML"
SIDEBAR_GROUP_SETTINGS = "Settings"

DATA_VIEW_PROCESS = 'Process Data'

EDA_VIEW_BASIC = 'Basic Analysis'
EDA_VIEW_CATEGORICAL = 'Categorical Analysis'
EDA_VIEW_NUMERICAL = 'Numerical Analysis'
EDA_VIEW_BIVARIATE = 'Bivariate Analysis'
EDA_VIEW_MULTIVARIATE = 'Multivariate Analysis'
EDA_VIEW_MAP = 'Map View'
EDA_VIEW_CUSTOM_PLOT = 'Custom Plot'

EDA_VIEWS = [
    EDA_VIEW_BASIC,
    EDA_VIEW_CATEGORICAL,
    EDA_VIEW_NUMERICAL,
    EDA_VIEW_BIVARIATE,
    EDA_VIEW_MULTIVARIATE,
    EDA_VIEW_MAP,
    EDA_VIEW_CUSTOM_PLOT
]

ML_VIEW_SUPERVISED = 'Supervised'

ML_VIEWS = [
    ML_VIEW_SUPERVISED
]

DATA_SOURCE_FILE = "Local"
DATA_SOURCE_URL = "URL"
DATA_SOURCE_DEMO = "Demo"
DATA_SOURCES = [
    DATA_SOURCE_FILE,
    DATA_SOURCE_URL,
    DATA_SOURCE_DEMO
]

DATA_MAX_N_ROWS = 100000
DATA_CSV_SEPERATORS = [',', ';', '', '|', r'\t']

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



@st.cache
def load_data(file, nrows=None, sep=','):
    data = pd.read_csv(file, nrows=nrows, sep=sep)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data



def main():
    df = None
    selected_eda_views = []
    selected_ml_views = []
    categorical_columns = None
    nummeric_columns = None
    random_state = None

    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_ICON + ' ' + APP_TITLE)

    with st.beta_expander("Load Data", True):
        dataset_source = st.selectbox('Data Source', DATA_SOURCES)
        
        file = None
        nrows = DATA_MAX_N_ROWS
        sep = ','

        if dataset_source == DATA_SOURCE_DEMO:
            dataset_name = st.selectbox('Demo Dataset', list(DEMO_DATASETS.keys()))
            if len(dataset_name):
                file = DEMO_DATASETS[dataset_name]['url']
                nrows = DEMO_DATASETS[dataset_name]['nrows']
                sep = DEMO_DATASETS[dataset_name]['sep']

        if dataset_source != DATA_SOURCE_DEMO:
            col1, col2 = st.beta_columns(2)
            with col1:
                nrows = st.number_input('Number of Rows', value=nrows)
            with col2:
                sep = st.selectbox('Sepetator', DATA_CSV_SEPERATORS)
                sep = sep if len(sep) else ','
            nrows = nrows if nrows else None

        if dataset_source == DATA_SOURCE_FILE:
            file = st.file_uploader('Upload File', type=['csv', 'tsv', 'txt'])
            if file is not None:
                file.seek(0)

        if dataset_source == DATA_SOURCE_URL:
            file = st.text_input('Dataset URL (csv)')
            if len(file) == 0:
                file = None

        if file is not None:
            try:
                df = load_data(file, nrows, sep)
                viewutil.view_data(df, 'file')
            except Exception as e:
                st.error(e)
                st.stop()
    
    if df is not None and len(df):
        
        with st.beta_expander(DATA_VIEW_PROCESS):
            df, categorical_columns, nummeric_columns = dataprocessview.generate_date_process_view(df)

        if len(categorical_columns) == 0:
            EDA_VIEWS.remove(EDA_VIEW_CATEGORICAL)

        if len(nummeric_columns) == 0:
            EDA_VIEWS.remove(EDA_VIEW_NUMERICAL)
        
        if len(categorical_columns) == 0 or len(nummeric_columns) == 0:
            EDA_VIEWS.remove(EDA_VIEW_BIVARIATE)
            EDA_VIEWS.remove(EDA_VIEW_MULTIVARIATE)

        if commonutil.find_index_from_list(df.columns, 'lat') == -1 or commonutil.find_index_from_list(df.columns, 'lat') == -1:
            EDA_VIEWS.remove(EDA_VIEW_MAP)

        with st.sidebar.beta_expander(SIDEBAR_GROUP_EDA):
            for view in EDA_VIEWS:
                if st.checkbox(view):
                    selected_eda_views.append(view)

        with st.sidebar.beta_expander(SIDEBAR_GROUP_ML, False):
            for view in ML_VIEWS:
                if st.checkbox(view):
                    selected_ml_views.append(view)

        with st.sidebar.beta_expander(SIDEBAR_GROUP_SETTINGS, False):
            if st.checkbox("Random State", True):
                random_state = st.number_input("Random Seed", 42)

        if len(selected_eda_views):
            st.markdown('## Exploratory Data Analysis')

        if EDA_VIEW_BASIC in selected_eda_views:
            with st.beta_expander(EDA_VIEW_BASIC, True):
                viewutil.section_title('Info')
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())

                viewutil.section_title('Data Types')
                dtypes = df.dtypes.rename('Total')
                dtypes

                if len(df.columns):
                    viewutil.section_title('Describe')
                    desc = df.describe().T
                    desc

                viewutil.section_title('Missing Values')
                isnull = df.isnull().sum().rename('Total')
                isnull

                viewutil.section_title('Skew')
                skew = df.skew()
                skew
                
                viewutil.section_title('Covariance')
                cov = df.cov()
                cov
                if len(cov) and st.checkbox('Hitmap', key='cov_hitmap'):
                    viewutil.st_plot(sns.heatmap(cov, annot=True))

                viewutil.section_title('Correlation')
                corr = df.corr()
                corr
                if len(corr) and st.checkbox('Hitmap', key='corr_hitmap'):
                    viewutil.st_plot(sns.heatmap(corr, annot=True))
        
        if EDA_VIEW_CATEGORICAL in selected_eda_views:
            with st.beta_expander(EDA_VIEW_CATEGORICAL, True):
                selected_columns = st.multiselect('Columns', categorical_columns, key='cat_col')
                for col in selected_columns:
                    viewutil.section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        count = df[col].value_counts()
                        count

                    with col2:
                        viewutil.st_plot(sns.countplot(df[col]))

        if EDA_VIEW_NUMERICAL in selected_eda_views:
            with st.beta_expander(EDA_VIEW_NUMERICAL, True):
                selected_columns = st.multiselect('Columns', nummeric_columns, key='num_col')
                for col in selected_columns:
                    viewutil.section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        desc = df[col].describe()
                        desc
                    with col2:
                        try:
                            viewutil.st_plot(sns.distplot(df[col]))
                        except Exception as e:
                            st.error(e)

        if EDA_VIEW_BIVARIATE in selected_eda_views:
            with st.beta_expander(EDA_VIEW_BIVARIATE, True):
                selected_cat_columns = st.multiselect('X', categorical_columns, key='bi_cat_col')
                selected_num_columns = st.multiselect('Y', nummeric_columns, key='bi_num_col')
                for cat_col in selected_cat_columns:
                    for num_col in selected_num_columns:
                        if cat_col != num_col:
                            col1, col2 = st.beta_columns(2)
                            with col1:
                                desc = df[num_col].describe()
                                desc
                            
                            with col2:
                                viewutil.st_plot(sns.swarmplot(x=df[cat_col], y=df[num_col]))

                for cat_col in selected_cat_columns:
                    for num_col in selected_num_columns:
                        if cat_col != num_col:
                            viewutil.st_plot(sns.boxplot(x=df[cat_col], y=df[num_col]))

        if EDA_VIEW_MULTIVARIATE in selected_eda_views:
            with st.beta_expander(EDA_VIEW_MULTIVARIATE, True):
                selected_x_columns = st.multiselect('X', nummeric_columns, key='mul_num_col')
                selected_y_columns = st.multiselect('Y', nummeric_columns, key='mul_num_col')
                selected_hue_columns = st.multiselect('Hue', categorical_columns, key='mul_cat_col')
                
                for x in selected_x_columns:
                    for y in selected_y_columns:
                        if x != y:
                            for z in selected_hue_columns:
                                viewutil.st_plot(sns.scatterplot(df[x], df[y], df[z]))

        if EDA_VIEW_MAP in selected_eda_views:
            with st.beta_expander(EDA_VIEW_MAP, True):
                edamapview.generate_map_view(df)

        if EDA_VIEW_CUSTOM_PLOT in selected_eda_views:
            with st.beta_expander(EDA_VIEW_CUSTOM_PLOT, True):
                edacustomplot.generate_plot_view(df)

        if len(selected_ml_views):
            st.markdown('## Machine Learning')

        if ML_VIEW_SUPERVISED in selected_ml_views:
            with st.beta_expander(ML_VIEW_SUPERVISED, True):
                mlsupervised.generate_train_view(df, random_state)

main()