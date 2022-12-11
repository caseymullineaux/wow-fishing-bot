import cv2 as cv
import numpy as np
import pyautogui
import time
import os


class FishingAgent:
    def __init__(self, main_agent) -> None:
        path = os.getcwd()

        self.main_agent = main_agent
        self.fishing_target = cv.imread(
            "F:\\source\\personal\\caseymullineaux.github.com\\wow-fishing-bot\\fishing\\assets\\fishing_target.png"
        )
        self.fishing_thread = None

    def cast_lure(self):
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
            print("Searching for lure ...")
            lure_location = cv.matchTemplate(
                frame, self.fishing_target, cv.TM_CCOEFF_NORMED
            )
            lure_location_array = np.array(lure_location)

            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location_array)
            print(max_loc)
            self.move_to_lure(max_loc)

        # cv.imshow("Match template",lure_location_array)
        # cv.waitKey(0)

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
        print(f'Pixel:{pixel}')
        while True:
            watch_pixel = self.main_agent.frame_HSV[coordinates[1], coordinates[0]] # take just a slice of the image (y,x)
            time.sleep(0.1)
            print(f'Watch Pixel:{watch_pixel}')
            movement_threshold = -40

            # if self.main_agent.zone == "Valdrakken" and self.main_agent.time_of_day == "night":
            # look at the H value (in HSV) and compare change to how much the bobber needs to move to determine a bite
            if watch_pixel[0] <= pixel[0] +  movement_threshold: 
                print(f"Bite detected! {watch_pixel[0]} <= {pixel[0] + movement_threshold}")
                self.pull_line()
                break

            if time.time() - watch_time >= fishing_timeout:
                print("Fishing timed out")
                self.pull_line()
                break

    def pull_line(self):
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
