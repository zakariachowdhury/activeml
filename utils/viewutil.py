import streamlit as st

def section_title(text):
    st.markdown(f'*{text}*')

def view_data(df, checkbox_key=None):
    if df is not None:
        section_title('Shape')
        st.write(df.shape)

        section_title('Head')
        st.write(df[:5])

        if st.checkbox("View All", key=checkbox_key):
            st.write(df)

def st_plot(plot):
    try:
        st.pyplot(plot.get_figure(), clear_figure=True)
    except Exception as e:
        st.error(e)

def st_round(x, precision=3):
    st.write(round(x, precision))