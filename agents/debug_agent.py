
from dataclasses import dataclass
from typing import Optional
from .main_agent import MainAgent
import cv2
from utils import ImageProcessor 



@dataclass
class DebugAgent:
    agent: MainAgent
    target_image: Optional[cv2.Mat]
    threshold: float=0.4

    def run(self) -> None:
        # cv2.namedWindow("Capture", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("Capture", 1282,720)
        # cv2.namedWindow("BW", cv2.WINDOW_NORMAL)
        # cv2.resizeWindow("BW", 1282,720)

        bobber = cv2.imread('assets/valdrakken.png')
        h = bobber.shape[0]
        w = bobber.shape[1]

        while True:
            # capture the screen
            # frame = ImageGrab.grab()
            frame = cv2.imread('assets/valdrakken_screenshot2.jpg', cv2.IMREAD_UNCHANGED)
            # self.agent.frame = np.array(frame)
            
            match = ImageProcessor.find_image(frame, bobber, self.threshold, debug=True)
            if not match:
                print("Couldn't find the bobber, trying again ...")
            else:
                print(f'I think I see a bobber!')
                 
   
            # time.sleep(5)


            # matches = find_image('assets/screenshot_2.jpg', 'assets/bobber.png', 0.6)
            # print(f"found {len(matches)} matches")
            # for match in matches:
            #     x, y, w, h = match
            #     cv2.rectangle(frame, (x,y), (x + h, y + w), (255,255,0), 1)

            # cv2.imshow("matches", frame)


            #time.sleep(10)
            # result = cv2.matchTemplate(frame, target,cv2.TM_CCOEFF_NORMED)
            # threshold = .80
            # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            # yloc, xloc = np.where(result >= threshold)
            # print(f"Matches: {len(xloc)}")
            # # print(f"Target detected: {max_loc} [Confidence: {max_val}]")

            # w = target.shape[1]
            # h = target.shape[0]
            # for (x,y) in zip(xloc, yloc):
            #     cv2.rectangle(frame, (x,y), (x + h, y + w), (255,255,0), 1)

            
            # # x = max_loc[0]
            # # y = max_loc[1]
            # # cv2.rectangle(frame, max_loc,(x + w, y + h), (255,255,0), 3 )
            # cv2.imshow("result",frame)

            # # draw a rectangle around the target
            
            # w = 20
            # h = 20
            # cv2.rectangle(frame, (x, y), (x + w, y+h), (0,255, 0), 2)

            # let result = cv.minMaxLoc(dst, mask);
            # let maxPoint = result.maxLoc;
            # let color = new cv.Scalar(255, 0, 0, 255);
            
            # cv2.imshow('canvasOutput', frame)



            # self.agent.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            # self.agent.frame = frame

            # convert the colours into something better to work with (HSV)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # cv2.imshow("Capture", frame)
            # cv2.imshow("Template", self.target_image)

            # convert image and template to grayscale
            # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # target_gray = cv2.cvtColor(self.target_image, cv2.COLOR_BGR2GRAY)
            # # cv2.imshow("output",frame_gray)
            # # cv2.imshow("target",target_gray)

            # # covert the grayscale image to binary and invert it
            # ret, binary = cv2.threshold(target_gray, 100, 255, cv2.THRESH_OTSU)
            # mask = ~binary
            # cv2.imshow("mask", mask)

            # cv2.imshow("output",inverted_binary)
            # cv2.imshow("target",self.target_image)

            # cv2.imshow("Binary Image", inverted_binary)

            # find the contours on the inverted binary image
            # contours, heirarchy = cv2.findContours(inverted_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # draw the contours
            # with_contours = cv2.drawContours(frame, contours, -1, (0,255,255), 1)
            # cv2.imshow('Detected contours', with_contours)

            # show number of contours detected
            # print(f'Total number of contours detected:{str(len(contours))}')

            # draw a bounding box around the contours
            # with_contours = None
            # for c in contours:
            #     x, y, w, h = cv2.boundingRect(c)

            #     # filter our large contours
            #     if(cv2.contourArea(c) > 100 and cv2.contourArea(c) < 300):
            #         with_contours = cv2.drawContours(frame, c, -1, (0,255,255), 1)
            #         cv2.rectangle(with_contours, (x,y), (x+w, y+h), (255,255,0), 1)
            
            # cv2.imshow("Bobber", with_contours)

            # apply template matching
            # target_location_array = np.array(match_img(frame_gray, target_gray, 0.1))
  
            # store width and height of the template

            # # # detect the target image
            # if frame is not None and self.target_image is not None:
            #     target_location = cv2.matchTemplate(frame_gray, self.target_image, cv2.TM_CCOEFF_NORMED)
            #     threshold = 0.8
            #     target_location_array = np.array(target_location)
            #     # target_location_array = np.where(target_location >= threshold)
            #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(target_location_array)
            #     match_location = max_loc
            #     print(f"Target detected: {match_location}")

            #     # draw a rectangle around the target
            #     x = max_loc[0]
            #     y = max_loc[1]
            #     w = 40
            #     h = 40
            #     cv2.rectangle(frame, (x, y), (x + w, y+h), (0,255, 0), 2)

            #     # find the centre of the square and draw a dot
            #     cX = int(x + (w /2 ))
            #     cY = int(y + (h /2 ))
            #     cv2.circle(frame, (cX, cY), 5, (255,255,255), 1)

            # #     # # write some text
            # #     # cv2.putText(self.agent.frame_HSV, "bobber", (cX -25, cY -25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255,255), 2)
            #     cv2.imshow("output", frame)
            #     target_location = cv2.matchTemplate(frame, self.target_image,cv2.TM_CCOEFF_NORMED)
            #     target_location_array = np.array(target_location)
            #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(target_location_array)
            #     print(f"Target detected: {max_loc}")

            #     # apply a blur for better edge detection
            #     self.agent.frame_HSV = cv2.GaussianBlur(self.agent.frame_HSV, (7,7), 0)

            #     # create a mask
            #     mask = cv2.inRange(self.agent.frame_HSV, min_color_match, max_color_match)

            #     # get the result of the image after we apply the mask
            #     result = cv2.bitwise_and(self.agent.frame_HSV, self.agent.frame_HSV, mask=mask)

            #     # find the contours of the object
            #     contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            #     # draw outlines on all the contours
            #     cv2.drawContours(result, contours, -1, (0,255,255),1 )

            #     for contour in contours:
            #         # create a bounding rectangle for the contour
            #         (x,y,w,h) = cv2.boundingRect(contour)

            #         # draw a rectangle around the contours
            #         cv2.rectangle(self.agent.frame, (x,y), (x+w, y+h), (0,0,255),2)
                    
            #         # put a dot in the middle
            #         cX = int(x + (w/2))
            #         cY = int(y + (h/2))
            #         cv2.circle(self.agent.frame, (cX, cY), 5, (255,255,255), -1, 1)

            #         # add some text
            #         cv2.putText(self.agent.frame, "bobber", (cX -25, cY -25), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.4, (255,255,255), 1)


            #     cv2.imshow("Result", result)

            #     # # draw a rectangle around the target
            #     # x = max_loc[0]
            #     # y = max_loc[1]
            #     # w = 20
            #     # h = 20
            #     # cv2.rectangle(self.agent.frame_HSV, (x, y), (x + w, y+h), (0,255, 0), 2)

            #     # # find the centre of the square and draw a dot
            #     # cX = int(x + (w /2 ))
            #     # cY = int(y + (h /2 ))
            #     # cv2.circle(self.agent.frame_HSV, (cX, cY), 5, (255,255,255), 1)

            #     # # write some text
            #     # cv2.putText(self.agent.frame_HSV, "bobber", (cX -25, cY -25), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255,255), 2)



            # # show the images
            # cv2.imshow("Capture", self.agent.frame)
           

            # wait for a key press
            key = cv2.waitKey(1)
            if key == ord("q"):
                # break
                print("Quitting ...")
                cv2.destroyAllWindows()
                exit(0)