import streamlit as st
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder

import viewutil

LABEL_COLUMNS = 'Columns'
LABEL_DATE_COLUMNS = 'Date Columns'
LABEL_CATEGORICAL_COLUMNS = 'Categorical Columns'
LABEL_NUMERICAL_COLUMNS = 'Numerical Columns'
LABEL_OPERATIONS = 'Operations'
LABEL_DROP_NULL_VALUES = 'Drop Null Values'
LABEL_DROP_DUPLICATES = 'Drop Duplicates'
LABEL_RESET_INDEX = 'Reset Index'
LABEL_ENCODER = 'Encoder'
LABEL_ENCODER_TYPE = 'Encoder Type'
LABEL_ENCODER_COLUMNS = 'Encode Columns'

ENCODER_TYPE_ONE_HOT = 'One Hot Encoder'
ENCODER_TYPE_LABEL = 'Label Encoder'
ENCODERS_TYPES = [
    ENCODER_TYPE_ONE_HOT,
    ENCODER_TYPE_LABEL
]

def generate_date_process_view(df):
    columns = st.multiselect(LABEL_COLUMNS, list(df.columns), list(df.columns))
    df = df[columns]
    
    cat_col = df.select_dtypes(include=['object']).columns.tolist()
    num_col = df.select_dtypes(include=np.number).columns.tolist()
    
    date_columns = st.multiselect(LABEL_DATE_COLUMNS, cat_col)
    for col in date_columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception as e:
            st.error(f'Column \'{col}\' cannot be converted to date/time')

    if cat_col is not None and date_columns is not None:
        cat_col = list(set(cat_col) - set(date_columns))

    categorical_columns = st.multiselect(LABEL_CATEGORICAL_COLUMNS, columns, cat_col)
    nummeric_columns = st.multiselect(LABEL_NUMERICAL_COLUMNS, num_col, num_col)

    viewutil.section_title(LABEL_OPERATIONS)

    if st.checkbox(LABEL_DROP_NULL_VALUES):
        df.dropna(inplace=True)

    if st.checkbox(LABEL_DROP_DUPLICATES):
        df.drop_duplicates(inplace=True)

    if st.checkbox(LABEL_RESET_INDEX):
        df.reset_index(drop=True, inplace=True)

    if st.checkbox(LABEL_ENCODER):
        encoder_type = st.selectbox(LABEL_ENCODER_TYPE, ENCODERS_TYPES)
        encode_columns = st.multiselect(LABEL_ENCODER_COLUMNS, categorical_columns)

        if len(encode_columns):
            if encoder_type == ENCODER_TYPE_LABEL:
                df.loc[:,encode_columns] = df.loc[:,encode_columns].apply(LabelEncoder().fit_transform)
            elif encoder_type == ENCODER_TYPE_ONE_HOT:
                df = pd.get_dummies(df, columns=encode_columns, prefix=encode_columns )


    viewutil.view_data(df, "process")

    return df, categorical_columns, nummeric_columns