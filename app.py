import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Weather App", 
                   layout="centered")

def show_temperature(id):
    st.write("lat: ",id["lat"])
    st.write("lon: ",id["lon"])

def show_city_options(city):
    headers={"User-Agent": "weather-app (github.com/murilobispo)"}
    url = f"https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&accept-language=en&q={city}"

    try:
        response = requests.get(url,headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()
        pills_container = st.empty()
        if not data:
            st.warning("CIty not found")
        else:
            df = pd.json_normalize(data)
            df = df[df["addresstype"].isin(["city", "municipality", "town"])].reset_index(drop=True)
            if df.empty:
                st.warning("Enter only cities")
            elif len(df) == 1:
                show_temperature(df.iloc[0])
            else:
                options = (df["name"] + ", " + df["address.state"] + ", " + df["address.country"]).tolist()
                with pills_container:
                    selected = st.pills(label="Do you mean:", 
                                        options=options, 
                                        selection_mode="single",
                                        )
                    if selected:
                        pills_container.empty()
                        show_city_options(selected)

    except requests.exceptions.RequestException as e:
        st.error(f"Error {e}")

city_input = st.text_input(label="city-input",
                           key="city-input",
                           value=None,
                           label_visibility="hidden",
                           placeholder="city"
                           )
if city_input:
    show_city_options(city_input)

#metric = st.metric(label="Temperature", 
                #value="70 °F", )
