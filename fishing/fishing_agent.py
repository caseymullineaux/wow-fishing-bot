import cv2 as cv
import numpy as np
import pyautogui
import time
import os



class FishingAgent:
    def __init__(self, main_agent) -> None:
        path = os.getcwd()
        
        self.main_agent = main_agent
        self.fishing_target = cv.imread("F:\\source\\personal\\caseymullineaux.github.com\\wow-fishing-bot\\fishing\\assets\\fishing_target.png")
        self.fishing_thread = None

    def cast_lure(self):
        print("Casting  ...")
        pyautogui.press('num1')
        time.sleep(2)
        self.find_lure()
    
    def find_lure(self):
        if self.main_agent.frame is not None:
            frame =self.main_agent.frame
            print("Searching for lure ...")
            lure_location = cv.matchTemplate(
                frame, 
                self.fishing_target,
                cv.TM_CCOEFF_NORMED
                )
            lure_location_array = np.array(lure_location)

            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(lure_location_array)
            print(max_loc)
            x = max_loc[0]
            y = max_loc[1]
            self.move_to_lure(x, y)



        # cv.imshow("Match template",lure_location_array)
        # cv.waitKey(0)
    

    def move_to_lure(self, x, y):
        pyautogui.moveTo(x, y, 1, pyautogui.easeOutQuad)

    def watch_lure(self):
        pass

    def pull_line(self):
        pass

    def run(self):
        while True:
            self.cast_lure()
            time.sleep(5)

# if __name__ == "__main__":
#     main_agent = None
#     fishing_agent = FishingAgent(main_agent)
#     fishing_agent.run()