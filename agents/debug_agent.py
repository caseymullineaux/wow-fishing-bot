
from dataclasses import dataclass
from typing import Optional
from .main_agent import MainAgent
import cv2
from utils import ImageProcessor 
import time
import pyautogui
from mss import mss
import numpy as np

@dataclass
class DebugAgent:
    agent: MainAgent
    target_image: Optional[cv2.Mat]
    threshold: float=0.4
    monitor_num: int = 2

    def run(self) -> None:
        bobber = cv2.imread('assets/bobber5.png')
        h = bobber.shape[0]
        w = bobber.shape[1]


        # get the dimensions of the screen
        w = mss().monitors[self.monitor_num]['width']
        h = mss().monitors[self.monitor_num]['height']
        print(f'Monitor {self.monitor_num}: {w}x{h}')


        fps_report_time = time.time()
        fps_report_delay = 1
        frame_count = 0

        with mss() as screenshot:
            # define the screen capture area as the entire screen
            mon = screenshot.monitors[self.monitor_num]
            monitor = { "top":mon["top"], "left":mon["left"], "width": mon["width"], "height": mon["height"], "mon": self.monitor_num}


            while True:
                
                # capture the screen
                frame = cv2.imread('assets/valdrakken_screenshot.jpg', cv2.IMREAD_UNCHANGED)
                # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                # capture the screen
                # frame = np.array(screenshot.grab(monitor=monitor))
                frame_count += 1
                
                match = ImageProcessor.find_image(frame, bobber, self.threshold, debug=True)
                if not match:
                    print("Couldn't find the bobber, trying again ...")
                else:
                    print(f'I think I see a bobber!')

                    # draw a rectangle around the bobber
                    # middle = ImageProcessor.find_middle(match)
            
                     # draw a rectangle around the match
                    cv2.rectangle(frame, (match['x'], match['y']), (match['x']+match['w'],match['y']+match['h']), (255,255,0), 3)       

                # scale the image down for display
                scale_pct = 50
                scale_w = int(frame.shape[1] * scale_pct / 100)
                scale_h = int(frame.shape[0] * scale_pct / 100)
                small_img = cv2.resize(frame, (scale_w,scale_h))

                
                # display the FPS
                elapsed_time = time.time() - fps_report_time
                if elapsed_time >= fps_report_delay:
                    fps = (frame_count / elapsed_time)
                    fps_text = f"FPS: {fps}"
                    cv2.putText(
                        small_img,
                        fps_text,
                        (25,50),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1,
                        (255,0,255),
                        1,
                        cv2.LINE_AA
                    )

                # display the screenshot in a new window
                cv2.imshow("Computer Vision", small_img)

                # wait for a key press
                key = cv2.waitKey(1)
                if key == ord("q"):
                    # break
                    print("Quitting ...")
                    cv2.destroyAllWindows()
                    exit(0)

if __name__ == "__main__":
    main_agent = MainAgent()
    debug_agent = DebugAgent(main_agent, None)
    debug_agent.run()
