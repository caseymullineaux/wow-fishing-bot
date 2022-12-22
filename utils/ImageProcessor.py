import cv2
from mss import mss
import time
import numpy as np
from PIL import Image

def find_middle(coordinates) -> tuple:
    '''
    Finds the middle of a square given its x, y (top left) and w, h
    '''
    x, y, w, h = coordinates
    middle = (int((w-x)/2+x), int(h/2+y))
    return middle

def find_image(haystack: cv2.Mat, needle: cv2.Mat, threshold:float, debug:bool=False)-> dict | None:
        '''
        Finds an image (needle) within another image (haystack) 
        and retuns the x,y (top left) and w, h of a bounding area that surrounds the detection
        '''

        # convert the images to HSV because it's easier to match images
        haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2HSV)
        needle = cv2.cvtColor(needle, cv2.COLOR_BGR2HSV)
        # haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
        # needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
        # do a template match
        match = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)

        # get coordinates of best and worst match
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match)

        # compare against threshold
        if max_val < threshold:
            if debug:
                print(f"Match did not pass threshold: {round(max_val,2)}/{threshold}")
            return
        
        h = needle.shape[0]
        w = needle.shape[1]
        x = max_loc[0]
        y = max_loc[1]
        coordinates = (x, y, w, h)

        # if debug:
        #     middle = find_middle(coordinates)
        #     print(f"Match found: {round(max_val,2)}/{threshold} @ {middle}")
            
        #     # draw a rectangle around the match
        #     cv2.rectangle(haystack, (x,y), (x+w,y+h), (255,255,0), 1)       
        #     cv2.imshow("match", haystack)     
        #     cv2.imshow("bobber", needle)
            
        # return coordinates of the match
        return{"x":x,"y": y,"w": w,"h": h}

def capture_screen(monitor, debug=False)-> np.ndarray:
    with mss() as screenshot:
        # while True:
        img = screenshot.grab(monitor=monitor) # captures in BGR
        image = Image.frombytes("RGB", img.size, img.rgb)

    return np.array(image)


def find_edges(screenshot: cv2.Mat):
    """
    Accepts a screenshot a black and white image of detected edges
    """
    gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny


def region_of_interest(screenshot: cv2.Mat):
    """
    Accepts a screenshot and returns a black and white image of detected edges
    within a specified area of interest
    """
    image = find_edges(screenshot)

    # create a region using the x/y of four points on a rectangle based on screen pixel dimensions
    bottom_right = (2000,1000)
    bottom_left = (500,1000)
    top_left = (500,400)
    top_right = (2000,400)
    region = np.array([[[bottom_right, bottom_left, top_left, top_right]]])

    # create a mask by starting with a black image same dimsions as the screenshot
    # and filling the region rectangle with white
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, region, 255)

    # cut out everything outside the region of interest
    # and return the mask
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


def label_bobber(image, mask):
    """

    """
    image = np.copy(image)
    # Each individual contour is a Numpy array of (x,y) coordinates of boundary points of the object
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find the contour with the largest area (to ignore sparkles etc)
    bobber_contour = max(contours, key=cv2.contourArea)

    # draw outlines on all the contours
    contour_mask =cv2.drawContours(image, bobber_contour, -1, 255, 2)

    # for contour in contours:
        # create a bounding rectangle for the contour
    (x, y, w, h) = cv2.boundingRect(bobber_contour)

    # draw a rectangle around the corners
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)


    # put a dot in the middle
    cX = np.int32(x + (w/2))
    cY = np.int32(y + (h/2))
    cv2.circle(image, (cX, cY), 5, (255,255,255), -1, 1)

    # keep the centerpoint
    # center.append([cX,cY])

    # add some text for flavor
    cv2.putText(image, "bobber", (cX-25, cY-25), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

    return image
