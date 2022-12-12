import cv2


def find_middle(coordinates) -> tuple:
    '''
    Finds the middle of a square given its x, y (top left) and w, h
    '''
    x, y, w, h = coordinates
    middle = (int((w-x)/2+x), int(h/2+y))
    return middle


def find_image(haystack: cv2.Mat, needle: cv2.Mat, threshold:float, debug:bool=False)-> tuple | None:
        '''
        Finds an image (needle) within another image (haystack) 
        and retuns the x,y (top left) and w, h of a bounding area that surrounds the detection
        '''

        # convert the images to HSV because it's easier to match images
        # haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2HSV)
        # needle = cv2.cvtColor(needle, cv2.COLOR_BGR2HSV)
        haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
        needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
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

        if debug:
            middle = find_middle(coordinates)
            print(f"Match found: {round(max_val,2)}/{threshold} @ {middle}")
            
            # draw a rectangle around the match
            cv2.rectangle(haystack, (x,y), (x+w,y+h), (255,255,0), 1)       
            cv2.imshow("match", haystack)     
            cv2.imshow("bobber", needle)
            
        # return coordinates of the match
        return(x,y,w,h)


