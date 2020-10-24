from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt
import seaborn as sns

APP_TITLE = "EDA"
SAMPLE_DATA_URL = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'

@st.cache
def load_data(url, nrows=None):
    data = pd.read_csv(url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def st_plot(plot):
    st.pyplot(plot.get_figure(), clear_figure=True)

def main():
    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_TITLE)

    with st.beta_expander("Data"):
        url = st.text_input('Data URL (csv):', SAMPLE_DATA_URL)
    
    if len(url):
        df = load_data(url)

        with st.beta_expander("Basic Stats"):
            '*Shape:*'
            df.shape

            '*Head:*'
            df[:5]

            '*Tail:*'
            df[-5:]

            '*Info:*'
            buffer = io.StringIO()
            df.info(buf=buffer)
            st.text(buffer.getvalue())

            '*Data Types:*'
            dtypes = df.dtypes.rename('Total')
            dtypes

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
            st_plot(sns.heatmap(cov, annot=True))

            '*Correlation:*'
            corr = df.corr()
            corr
            st_plot(sns.heatmap(corr, annot=True))
        
        with st.beta_expander('Categorical Columns:'):
            categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
            categorical_columns
            for col in categorical_columns:
                count = df[col].value_counts()
                count

                st_plot(sns.countplot(df[col]))

        with st.beta_expander('Numerical Columns:'):
            nummeric_columns = df.select_dtypes(include=np.number).columns.tolist()
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