import os
import cv2 as cv
import time
from emailing import send_email
import glob
from threading import Thread

video = cv.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

def clean():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status = 0
    check, frame = video.read()


    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_frame_gaus = cv.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gaus

    delta_frame = cv.absdiff(first_frame, gray_frame_gaus)

    thresh_frame = cv.threshold(delta_frame, 60, 255, cv.THRESH_BINARY)[1]
    dil_frame = cv.dilate(thresh_frame, None, iterations=2)
    cv.imshow("My video", dil_frame)

    contours, check = cv.findContours(dil_frame, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv.contourArea(contour)<5000:
            continue
        x, y, w, h = cv.boundingRect(contour)
        rectangle = cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            images_with_object = all_images[index]

    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(images_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=clean)
        clean_thread.daemon = True

        email_thread.start()


    cv.imshow("My video", frame)
    key = cv.waitKey(1)

    if key == ord("x"):
        break

video.release()
clean_thread.start()