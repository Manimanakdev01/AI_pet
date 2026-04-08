import streamlit as st

st.title("📸 ESP32-CAM LIVE STREAM")

ip = st.text_input("Enter Camera Stream URL", "http://192.168.29.248:81/stream")

if st.button("START"):
    st.image(ip)
