import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, r2_score

import viewutil

import matplotlib.pyplot as plt

LABEL_FEATURE_COLUMNS = 'Feature Columns'
LABEL_PREDICTION_COLUMN = 'Label Column'
LABEL_LEARNING_TYPE = 'Learning Type'
LABEL_ALGORITHM = 'Algorithm'
LABEL_TRAIN_SIZE = 'Train Size'
LABEL_TRAIN_MODEL = 'Train Model'
LABEL_EVALUATION_METRICS = 'Evaluate'
LABEL_R2_SCORE = 'R^2 Score'
LABEL_CONFUSION_MATRIX = 'Confusion Matrix'
LABEL_COEFFICIENTS = 'Coefficients'
LABEL_INTERCEPT = 'Intercept'

ML_TYPE_CLASSIFICATION = 'Classification'
ML_TYPE_REGRESSION = 'Regression'

ALGO_DECISION_TREE_CLASSIFIER = 'Decision Tree'
ALGO_LOGISTIC_REGRESSION = 'Logistic Regression'
ALGO_SVM = 'SVM'

ALGO_LINEAR_REGRESSION = 'Linear Regression'

ML_TYPES = {
    ML_TYPE_CLASSIFICATION: [
        ALGO_DECISION_TREE_CLASSIFIER,
        ALGO_LOGISTIC_REGRESSION,
        ALGO_SVM
    ],
    ML_TYPE_REGRESSION: [
        ALGO_LINEAR_REGRESSION
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
    train_size = st.slider(LABEL_TRAIN_SIZE, min_value=5, max_value=95, value=70, step=5)

    if len(feature_columns) and len(prediction_column) and st.checkbox(LABEL_TRAIN_MODEL):
        model = None
        X_train, X_test, y_train, y_test = train_test_split(df[feature_columns], df[prediction_column], train_size = train_size / 100, random_state = random_state)
        if algo_type == ALGO_LINEAR_REGRESSION:
            model = LinearRegression()
        elif algo_type == ALGO_LOGISTIC_REGRESSION:
            model = LogisticRegression(solver='lbfgs', multi_class='auto', random_state=random_state)
        elif algo_type == ALGO_SVM:
            model = SVC(kernel='linear', random_state=random_state)
        elif algo_type == ALGO_DECISION_TREE_CLASSIFIER:
            model = DecisionTreeClassifier(criterion='entropy')

        if model is not None:
            try:
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
            
                score = model.score(X_test, y_test)
                st.info('Accuracy: **' + str(round(score * 100, 2)) + '%**')
                
                if st.checkbox(LABEL_EVALUATION_METRICS):
                    if ml_type == ML_TYPE_REGRESSION:
                        viewutil.section_title(LABEL_R2_SCORE)
                        viewutil.st_round(r2_score(y_test, y_pred))

                        viewutil.section_title(LABEL_INTERCEPT)
                        viewutil.st_round(model.intercept_)

                        viewutil.section_title(LABEL_COEFFICIENTS)
                        st.write(model.coef_)

                        if X_test.shape[1] == 1 and len(X_test) == len(y_test):
                            plt.scatter(X_test, y_test, color="red")
                            plt.plot(X_test, y_pred, color="green")
                            plt.title("Test Data")
                            st.pyplot(plt.figure(1))

                    if ml_type == ML_TYPE_CLASSIFICATION:
                        viewutil.section_title(LABEL_CONFUSION_MATRIX)
                        st.write(pd.DataFrame(confusion_matrix(y_test, y_pred)))                    

            except Exception as e:
                st.error(e)
