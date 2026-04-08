import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("📸 Camera Test")

url = "http://192.168.29.248/stream"

if st.button("GET IMAGE"):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img)
