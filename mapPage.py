import streamlit as st
import folium
from streamlit_folium import st_folium

def map_page():
    st.title(" דירוג שכונות ידידותיות לכלבים")

    # דירוגים לדוגמה
    neighborhood_scores = {
        "לב תל אביב": 8.5,
        "פלורנטין": 9.2,
        "רמת אביב": 7.1,
        "יפו": 6.4
    }

    selected_neighborhood = st.selectbox(
        "בחר שכונה",
        neighborhood_scores.keys()
    )

    score = neighborhood_scores[selected_neighborhood]

    st.metric(
        label="דירוג השכונה",
        value=round(score, 1)
    )

    # יצירת מפה
    m = folium.Map(
        location=[32.0853, 34.7818],  # תל אביב
        zoom_start=13
    )

    folium.Marker(
        location=[32.0853, 34.7818],
        popup=f"{selected_neighborhood}: {score}",
        tooltip=selected_neighborhood
    ).add_to(m)

    st_folium(m, width=700, height=500)
