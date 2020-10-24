from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns

APP_TITLE = "EDA"
APP_SUBHEADER = "Exploratory Data Analysis"
SAMPLE_DATA_URL = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'

@st.cache
def load_data(url, nrows=None, sep=','):
    data = pd.read_csv(url, nrows=nrows, sep=sep)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def st_plot(plot):
    st.pyplot(plot.get_figure(), clear_figure=True)

def main():
    df = None
    categorical_columns = None
    nummeric_columns = None

    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_TITLE)
    st.subheader(APP_SUBHEADER)

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
            
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            nummeric_columns = df.select_dtypes(include=np.number).columns.tolist()

            date_columns = st.multiselect('Date Columns:', categorical_columns)
            for col in date_columns:
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception as e:
                    st.error(f'Column \'{col}\' cannot be converted to datetime')

            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

            '*Shape:*'
            df.shape

            '*Head:*'
            df[:5]

            '*Tail:*'
            df[-5:]
    
    if df is not None and len(df):
        with st.beta_expander("Basic Analysis"):
            '*Info:*'
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

            '*Data Types:*'
            dtypes = df.dtypes.rename('Total')
            dtypes

            if len(df.columns):
                '*Describe:*'
                desc = df.describe()
                desc

            '*Missing Values:*'
            isnull = df.isnull().sum().rename('Total')
            isnull

            '*Skew:*'
            skew = df.skew()
            skew
            
            '*Covariance:*'
            cov = df.cov()
            cov
            if len(cov):
                st_plot(sns.heatmap(cov, annot=True))

            '*Correlation:*'
            corr = df.corr()
            corr
            if len(corr):
                st_plot(sns.heatmap(corr, annot=True))
        
        with st.beta_expander('Categorical Columns:'):
            categorical_columns
            for col in categorical_columns:
                count = df[col].value_counts()
                count

                st_plot(sns.countplot(df[col]))

        with st.beta_expander('Numerical Columns:'):
            nummeric_columns
            for col in nummeric_columns:
                desc = df[col].describe()
                desc

                st_plot(sns.distplot(df[col]))

        with st.beta_expander('Categorical vs Numerical:'):
            for cat_col in categorical_columns:
                for num_col in nummeric_columns:
                    st_plot(sns.swarmplot(x=df[cat_col], y=df[num_col]))

            for cat_col in categorical_columns:
                for num_col in nummeric_columns:
                    st_plot(sns.boxplot(x=df[cat_col], y=df[num_col]))

        with st.beta_expander('Multivariate Analysis:'):
            for x in nummeric_columns:
                for y in nummeric_columns:
                    if x != y:
                        for z in categorical_columns:
                            st_plot(sns.scatterplot(df[x], df[y], df[z]))

    

main()