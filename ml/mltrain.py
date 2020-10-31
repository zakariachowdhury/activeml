import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

LABEL_FEATURE_COLUMNS = 'Feature Columns'
LABEL_PREDICTION_COLUMN = 'Label Column'
LABEL_LEARNING_TYPE = 'Learning Type'
LABEL_ALGORITHM = 'Algorithm'
LABEL_TRAIN_SIZE = 'Train Size'
LABEL_TRAIN_MODEL = 'Train Model'

ML_TYPE_CLASSIFICATION = 'Classification'
ML_TYPE_REGRESSION = 'Regression'

ALGO_LOGISTIC_REGRESSION = 'Logistic Regression'
ALGO_SVM = 'SVM'

ML_TYPES = {
    ML_TYPE_CLASSIFICATION: [
        ALGO_LOGISTIC_REGRESSION,
        ALGO_SVM
    ],
    ML_TYPE_REGRESSION: [

    ]
}

def generate_train_view(df, random_state):
    columns = list(df.columns)
    
    col1, col2 = st.beta_columns(2)
    with col1:
        ml_type = st.selectbox(LABEL_LEARNING_TYPE, list(ML_TYPES.keys()))
    with col2:
        algo_type = st.selectbox(LABEL_ALGORITHM, ML_TYPES.get(ml_type))

    feature_columns = st.multiselect(LABEL_FEATURE_COLUMNS, columns, columns[:-1])
    prediction_column = st.selectbox(LABEL_PREDICTION_COLUMN, list(set(columns) - set(feature_columns)), 0)
    train_size = st.slider(LABEL_TRAIN_SIZE, min_value=10, max_value=90, value=70, step=5)

    if st.checkbox(LABEL_TRAIN_MODEL):
        model = None
        X_train, X_test, y_train, y_test = train_test_split(df[feature_columns], df[prediction_column], train_size = train_size / 100, random_state = random_state)
        if algo_type == ALGO_LOGISTIC_REGRESSION:
            model = LogisticRegression(solver='lbfgs', multi_class='auto', random_state=random_state)
        elif algo_type == ALGO_SVM:
            model = SVC(kernel='linear', random_state=random_state)

        if model is not None and ml_type == ML_TYPE_CLASSIFICATION:
            try:
                model.fit(X_train, y_train)
            except Exception as e:
                st.error(e)
                st.stop()
            score = model.score(X_test, y_test)
            st.write('Score = ' + str(round(score, 3)))