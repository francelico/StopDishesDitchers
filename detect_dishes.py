import cv2
from copy import deepcopy
import os
import numpy as np

def detect_dishes():

    script_dir = os.path.dirname(os.path.realpath(__file__))
    folder = script_dir + '/output'

    # maybe move out of function
    dish_cam_id = 1
    video_capture = cv2.VideoCapture(dish_cam_id)
    circle_sensitivity = 60
    min_rad = 0
    max_rad = 100

    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Crop image:
    img = frame #!TODO: add cropping here

    img_crop_or = deepcopy(img) #making deep copy of frame

    img_blur = cv2.GaussianBlur(img, (9, 9), 2, 2)
    cv2.imwrite(os.path.join(folder, 'blurred.jpg'), img_blur) #!DEBUG/DEMO

    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(folder, 'gray.jpg'), img_gray) #!DEBUG/DEMO

    #print("Detecting circles in blurred and greyed image")
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 20,
                            param1=100,
                            param2=circle_sensitivity,
                            minRadius=min_rad,
                            maxRadius=max_rad)
    
    if circles is not None:
        dish_count = 0
        print "Dishes Found!"
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(img_crop_or, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(img_crop_or, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            dish_count += 1
            print "Dish count:%s" % (str(dish_count))

    cv2.imwrite(os.path.join(folder, 'detected.jpg'), img_crop_or)
    
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_dishes()