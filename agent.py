import streamlit as st
import cv2
import numpy as np
import requests

st.title("🤖 AI Vision Control Panel")

ip = st.text_input("Enter Stream URL", "http://192.168.29.248:81/stream")

run = st.button("START")

frame_placeholder = st.empty()
text_placeholder = st.empty()

if run:
    while True:
        try:
            # 🔥 direct HTTP fetch
            stream = requests.get(ip, stream=True)
            bytes_data = bytes()

            for chunk in stream.iter_content(chunk_size=1024):
                bytes_data += chunk

                a = bytes_data.find(b'\xff\xd8')
                b = bytes_data.find(b'\xff\xd9')

                if a != -1 and b != -1:
                    jpg = bytes_data[a:b+2]
                    bytes_data = bytes_data[b+2:]

                    frame = cv2.imdecode(
                        np.frombuffer(jpg, dtype=np.uint8),
                        cv2.IMREAD_COLOR
                    )

                    # ---- RED DETECTION ----
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

                    lower_red1 = np.array([0,120,70])
                    upper_red1 = np.array([10,255,255])
                    lower_red2 = np.array([170,120,70])
                    upper_red2 = np.array([180,255,255])

                    mask = cv2.inRange(hsv, lower_red1, upper_red1) + \
                           cv2.inRange(hsv, lower_red2, upper_red2)

                    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                    direction = "CENTER"

                    for cnt in contours:
                        if cv2.contourArea(cnt) > 500:
                            x,y,w,h = cv2.boundingRect(cnt)
                            cx = x + w//2

                            if cx < frame.shape[1]//3:
                                direction = "LEFT"
                            elif cx > 2*frame.shape[1]//3:
                                direction = "RIGHT"

                            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

                    frame_placeholder.image(frame, channels="BGR")
                    text_placeholder.markdown(f"### Direction: {direction}")

        except:
            st.warning("Reconnecting...")
            continue