
import multiprocessing
import pyautogui
import time
from mss import mss
import cv2
import numpy as np

class ScreenCaptureAgent:
    def __init__(self) -> None:
        self.img = None
        self.capture_process = None
        self.fps = None
        self.enable_preview = True

        # get the dimensions of the screen
        self.w, self.h = pyautogui.size()
        print(f"Screen resolution: w:{str(self.w)} h:{str(self.h)}")

        # define the screen capture area as the entire screen
        self.monitor = { "top":0, "left":0, "width": self.w, "height": self.h}

    def capture_screen(self):
        fps_report_time = time.time()
        fps_report_delay = 1

        frame_count = 0
        with mss() as screenshot:
            while True:
                self.img = screenshot.grab(monitor=self.monitor) # captures in BGR
                frame_count += 1
                self.img = np.array(self.img)

                if self.enable_preview:
                    # scale the image down
                    scale_pct = 50
                    scale_w = int(self.img.shape[1] * scale_pct / 100)
                    scale_h = int(self.img.shape[0] * scale_pct / 100)
                    small_img = cv2.resize(self.img, (scale_w,scale_h))

                    
                    # key = cv2.waitKey(1) # wait for 1ms so the image can be rendered
                    # if key == ord('q'):
                    #     break

                    elapsed_time = time.time() - fps_report_time
                    if elapsed_time >= fps_report_delay:
                        self.fps = (frame_count / elapsed_time)
                        fps_text = f"FPS: {self.fps}"
                        cv2.putText(
                            small_img,
                            fps_text,
                            (25,50),
                            cv2.FONT_HERSHEY_DUPLEX,
                            1,
                            (0,255,255),
                            1,
                            cv2.LINE_AA
                        )

                    # display the screenshot in a new window
                    cv2.imshow("Computer Vision", small_img)
                    cv2.waitKey(1)
            
if __name__ == "__main__":
    screen_agent = ScreenCaptureAgent()
    screen_agent.capture_screen()
    # screen_agent.capture_process = multiprocessing.Process(
    #         target=screen_agent.capture_screen, 
    #         args=(),
    #         name="WowFishBot: Screen capture process"
    #     )
    # screen_agent.capture_process.start()

