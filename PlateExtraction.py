# -*- coding: utf-8 -*-
import cv2
import matplotlib.pyplot as plt

def plot_images(img1, img2, title1="", title2=""):
    fig = plt.figure(figsize=[15,15])
    ax2 = fig.add_subplot(122)
    ax2.imshow(img2, cmap="gray")
    ax2.set(xticks=[], yticks=[], title=title2)

def extraction(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur = cv2.bilateralFilter(gray, 11, 90, 90)

    edges = cv2.Canny(blur, 30, 200)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:40]

    plate = None
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)

            aspect_ratio = w / float(h)
            if 2 < aspect_ratio < 6:  
                plate = image[y:y+h, x:x+w]
                break

    return plate
