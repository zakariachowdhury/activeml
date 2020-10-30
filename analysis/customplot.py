import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

PLOT_TYPE_BOX = 'Box'
PLOT_TYPE_COUNT = 'Count'
PLOT_TYPE_DIST = 'Distribution'
PLOT_TYPE_HISTOGRAM = 'Histogram'
PLOT_TYPE_LINE = 'Line'
PLOT_TYPE_SCATTER = 'Scatter'
PLOT_TYPE_SWARM = 'Swarm'
PLOT_TYPES = [
    PLOT_TYPE_BOX,
    PLOT_TYPE_COUNT,
    PLOT_TYPE_DIST,
    PLOT_TYPE_HISTOGRAM,
    PLOT_TYPE_LINE,
    PLOT_TYPE_SCATTER,
    PLOT_TYPE_SWARM
]

LABEL_PLOT_TYPE = 'Plot Type'
LABEL_X = 'X'
LABEL_Y = 'Y'
LABEL_Z = 'Hue'

def st_plot(plot):
    try:
        st.pyplot(plot.get_figure(), clear_figure=True)
    except Exception as e:
        st.error(e)

def generate_plot_view(df):
    x = y = z = None
    plot_type = st.selectbox(LABEL_PLOT_TYPE, PLOT_TYPES)
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        x = st.selectbox(LABEL_X, [None] + list(df.columns))
    with col2:
        if plot_type not in [PLOT_TYPE_COUNT, PLOT_TYPE_DIST, PLOT_TYPE_HISTOGRAM]:
            y = st.selectbox(LABEL_Y, [None] + list(df.columns))
    with col3:
        if plot_type not in [PLOT_TYPE_COUNT, PLOT_TYPE_DIST, PLOT_TYPE_HISTOGRAM]:
            z = st.selectbox(LABEL_Z, [None] + list(df.columns))

    try:
        if plot_type == PLOT_TYPE_BOX:
            st_plot(sns.boxplot(x=x, y=y, hue=z, data=df))
        elif plot_type == PLOT_TYPE_COUNT:
            st_plot(sns.countplot(x=x, data=df))
        elif plot_type == PLOT_TYPE_DIST:
            st_plot(sns.distplot(df[x]))        
        elif plot_type == PLOT_TYPE_HISTOGRAM:
            st_plot(sns.histplot(df[x]))
        elif plot_type == PLOT_TYPE_LINE:
            st_plot(sns.lineplot(x=x, y=y, hue=z, data=df))
        elif plot_type == PLOT_TYPE_SCATTER:
            st_plot(sns.scatterplot(x=x, y=y, hue=z, data=df))
        elif plot_type == PLOT_TYPE_SWARM:
            st_plot(sns.swarmplot(x=x, y=y, hue=z, data=df))
    except Exception as e:
        if str(e) != "None":
            st.error(e)