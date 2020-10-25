from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns

APP_TITLE = "Exploratory Data Analysis"
SAMPLE_DATA_URL = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'

GROUP_BASIC = 'Basic Analysis'
GROUP_CATEGORICAL = 'Categorical Analysis'
GROUP_NUMERICAL = 'Numerical Analysis'
GROUP_BIVARIATE = 'Bivariate Analysis'
GROUP_MULTIVARIATE = 'Multivariate Analysis'

groups = [
    GROUP_BASIC,
    GROUP_CATEGORICAL,
    GROUP_NUMERICAL,
    GROUP_BIVARIATE,
    GROUP_MULTIVARIATE
]

@st.cache
def load_data(url, nrows=None, sep=','):
    data = pd.read_csv(url, nrows=nrows, sep=sep)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def st_plot(plot):
    st.pyplot(plot.get_figure(), clear_figure=True)

def section_title(text):
    st.markdown(f'*{text}*:')

def main():
    df = None
    selected_groups = []
    categorical_columns = None
    nummeric_columns = None

    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_TITLE)
    st.text('Enter your dataset csv url below to get started.')

    with st.beta_expander("Data", True):
        col1, col2 = st.beta_columns(2)
        with col1:
            nrows = st.number_input('Number of Rows:', value=100)
        with col2:
            sep = st.text_input('Sepetator:', ',')
            sep = sep if len(sep) else ','
        nrows = nrows if nrows else None
        url = st.text_input('Dataset URL (csv):', SAMPLE_DATA_URL)

        if len(url):
            try:
                df = load_data(url, nrows, sep)
            except Exception as e:
                st.error(e)
                st.stop()

            columns = st.multiselect('Columns:', list(df.columns), list(df.columns))
            df = df[columns]
            
            cat_col = df.select_dtypes(include=['object']).columns.tolist()
            num_col = df.select_dtypes(include=np.number).columns.tolist()

            categorical_columns = st.multiselect('Categorical Columns:', columns, cat_col)
            nummeric_columns = st.multiselect('Numerical Columns:', num_col, num_col)
            date_columns = st.multiselect('Date Columns:', categorical_columns)
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    st.error(f'Column \'{col}\' cannot be converted to datetime')

            section_title('Shape')
            df.shape

            section_title('Head')
            df[:5]

            if st.checkbox("View All"):
                df
    
    if df is not None and len(df):
        with st.sidebar.beta_expander("Groups", True):
            for group in groups:
                if st.checkbox(group):
                    selected_groups.append(group)

        if GROUP_BASIC in selected_groups:
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
        
        if GROUP_CATEGORICAL in selected_groups:
            with st.beta_expander(GROUP_CATEGORICAL, True):
                for col in categorical_columns:
                    section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        count = df[col].value_counts()
                        count

                    with col2:
                        st_plot(sns.countplot(df[col]))

        if GROUP_NUMERICAL in selected_groups:
            with st.beta_expander(GROUP_NUMERICAL, True):
                for col in nummeric_columns:
                    section_title(col)
                    col1, col2 = st.beta_columns(2)
                    with col1:
                        desc = df[col].describe()
                        desc
                    with col2:
                        st_plot(sns.distplot(df[col]))

        if GROUP_BIVARIATE in selected_groups:
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

        if GROUP_MULTIVARIATE in selected_groups:
            with st.beta_expander(GROUP_MULTIVARIATE, True):
                for x in nummeric_columns:
                    for y in nummeric_columns:
                        if x != y:
                            for z in categorical_columns:
                                st_plot(sns.scatterplot(df[x], df[y], df[z]))

    

main()