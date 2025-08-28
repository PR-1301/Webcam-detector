import cv2 as cv
import streamlit as st
from datetime import datetime

st.title("Motion detector")
start = st.button("Start Camera")


if start:
    streamlit_image = st.image([])
    camera = cv.VideoCapture(0)

    now = datetime.now()

    while True:
        check, frame = camera.read()
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        cv.putText(img=frame, text=now.strftime("%A") , org=(50, 50),
                   fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=2, color= (0,0,0), thickness=2,
                   lineType=cv.LINE_AA)

        cv.putText(img=frame, text=now.strftime("%H:%M:%S"), org=(50, 80),
                   fontFace=cv.FONT_HERSHEY_PLAIN, fontScale=1, color=(0, 0, 0), thickness=2,
                   lineType=cv.LINE_AA)

        streamlit_image.image(frame)
