from dataclasses import dataclass
import cv2
import numpy as np
import pyautogui
import time
import os
from utils import ImageProcessor

@dataclass
class FishingAgent:
    def __init__(self, main_agent, debug: bool = False) -> None:
        self.main_agent = main_agent
        self.fishing_target = cv2.imread('assets/valdrakken.png')
        self.fishing_thread = None
        self.debug = debug

    def cast_lure(self):
        '''
        Presses the assigned hotkey to cast the fishing rod
        '''
        print("Casting  ...")
        pyautogui.press("num1")
        time.sleep(2)
        self.find_lure()

    def find_lure(self):
        """
        Scans the input screenshot for the location of the fishing target image (bobber)
        """
        if self.main_agent.frame is not None:
            frame = self.main_agent.frame
            bobber = self.fishing_target
            print("Searching for lure ...")

            lure_location = ImageProcessor.find_image(frame, bobber, 0.8, debug=self.debug)

            # lure_location = cv2.matchTemplate(
            #     frame, self.fishing_target, cv2.TM_CCOEFF_NORMED
            # )
            # lure_location_array = np.array(lure_location)

            # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(lure_location_array)
            if lure_location:
                x, y, w, h = lure_location
                coordinates = ImageProcessor.find_middle(lure_location)
                self.move_to_lure(coordinates)

        # cv2.imshow("Match template",lure_location_array)
        # cv2.waitKey(0)

    def move_to_lure(self, coordinates):
        """
        Moves the mouse cursor in a smooth motion to the location of the detected bobber
        """
        pyautogui.moveTo(coordinates[0], coordinates[1], 1, pyautogui.easeOutQuad)
        self.watch_lure(coordinates)

    def watch_lure(self, coordinates):
        """
        Monitors a single pixel of the lure location waiting for when the pixel changes
        that represents when the bobber moves
        """
        fishing_timeout = 20
        watch_time = time.time()
        pixel = self.main_agent.frame_HSV[coordinates[1], coordinates[0]] # take just a slice of the image (y,x)
        # print(f'Pixel:{pixel}')
        while True:
            watch_pixel = self.main_agent.frame_HSV[coordinates[1], coordinates[0]] # take just a slice of the image (y,x)
            time.sleep(0.1)
            # print(f'Watch Pixel:{watch_pixel}')
            movement_threshold = -40

            # if self.main_agent.zone == "Valdrakken" and self.main_agent.time_of_day == "night":
            # look at the H value (in HSV) and compare change to how much the bobber needs to move to determine a bite
            if watch_pixel[0] <= pixel[0] +  movement_threshold: 
                print(f"Bite detected! {watch_pixel[0]} <= {pixel[0] + movement_threshold}")
                self.click_bobber()
                break

            if time.time() - watch_time >= fishing_timeout:
                print("Fishing timed out")
                self.click_bobber()
                break

    def click_bobber(self):
        print("Pulling line")
        pyautogui.click(button="left")
        time.sleep(3)

    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)


# if __name__ == "__main__":
#     main_agent = None
#     fishing_agent = FishingAgent(main_agent)
#     fishing_agent.run()
