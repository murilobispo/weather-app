import streamlit as st

city_input = st.text_input(label="city-input",
                           value=None,
                           label_visibility="hidden",
                           placeholder="city")
