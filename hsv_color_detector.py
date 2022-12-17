import cv2
import numpy as np

frame = cv2.imread('assets/screenshot_2.jpg')

# Create a slider bar to get the HSV values needed to detect the color


def trackbar_callback(x):
    pass

init_low_hue = 0
init_low_sat = 0
init_low_val = 160
init_high_hue = 111
init_high_sat = 255
init_high_val = 255

cv2.namedWindow("Values")
cv2.createTrackbar("Lower Hue", "Values", init_low_hue, 179, trackbar_callback)
cv2.createTrackbar("Lower Saturation", "Values", init_low_sat, 255, trackbar_callback)
cv2.createTrackbar("Lower Value", "Values", init_low_val, 255, trackbar_callback)
cv2.createTrackbar("Upper Hue", "Values", init_high_hue, 179, trackbar_callback)
cv2.createTrackbar("Upper Saturation", "Values", init_high_sat, 255, trackbar_callback)
cv2.createTrackbar("Upper Value", "Values", init_high_val, 255, trackbar_callback)

while True:
    # _, frame = cap.read()

    # convert the frame to HSV (Hue, Saturation, Value) color format
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get the values from the trackbar
    lower_hue = cv2.getTrackbarPos("Lower Hue", "Values")
    lower_saturation = cv2.getTrackbarPos("Lower Saturation", "Values")
    lower_value = cv2.getTrackbarPos("Lower Value", "Values")
    upper_hue = cv2.getTrackbarPos("Upper Hue", "Values")
    upper_saturation = cv2.getTrackbarPos("Upper Saturation", "Values")
    upper_value = cv2.getTrackbarPos("Upper Value", "Values")

    # create a range for the colour we want to detect
    low_blue = np.array([lower_hue, lower_saturation, lower_value])
    high_blue = np.array([upper_hue, upper_saturation, upper_value])

    # create a mask
    mask = cv2.inRange(hsv_frame, low_blue, high_blue)

    # get the result of the image after applying the mask
    # (bitwise operation)
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xff == ord('q'):
        print(
            f"min_blue = np.array([{lower_hue}, {lower_saturation}, {lower_value}])")
        print(
            f"max_blue = np.array([{upper_hue}, {upper_saturation}, {upper_value}])")

        break
cv2.destroyAllWindows()