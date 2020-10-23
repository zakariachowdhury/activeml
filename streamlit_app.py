from numpy.lib.utils import info
import streamlit as st
import pandas as pd
import io

APP_TITLE = "EDA"
SAMPLE_DATA_URL = 'https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'

@st.cache
def load_data(url, nrows=None):
    data = pd.read_csv(url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


def main():
    st.beta_set_page_config(
        page_title=APP_TITLE,
        page_icon="📊",
        layout="centered",
        initial_sidebar_state="auto")

    st.title(APP_TITLE)

    url = st.text_input('Data URL (csv):', SAMPLE_DATA_URL)
    df = load_data(url)

    '**Shape:**'
    df.shape

    '**Head:**'
    df[:5]

    '**Tail:**'
    df[-5:]

    '**Info:**'
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    '**Describe:**'
    desc = df.describe()
    desc

main()