import streamlit as st
from mapPage import map_page

st.set_page_config(
    page_title="דירוג שכונות לכלבים",
    layout="centered"
)

if "page" not in st.session_state:
    st.session_state.page = "home"

# דף פתיחה 
if st.session_state.page == "home":

    st.markdown(
        """
        <div style="direction: rtl; text-align: right;">
            <h1>דירוג שכונות לכלבים בתל אביב</h1>
            <p style="font-size:18px;">
            מערכת לחישוב ודירוג רמת הידידותיות של שכונות לכלבים
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("▶ התחל", use_container_width=True):
            st.session_state.page = "map"

# עמוד מפה 
elif st.session_state.page == "map":
    map_page()
