from dataclasses import dataclass
from PIL import Image, ImageGrab
import numpy as np
import cv2 as cv
import time
from threading import Thread
from fishing.fishing_agent import FishingAgent


class MainAgent:
    """
    The main AI of the application that controls all other agents
    """

    def __init__(self) -> None:
        self.agents = []
        self.fishing_thead = None

        self.frame = None  # BGR Image
        self.frame_HSV = None  # HSV Image

        self.zone = "Valdrakken"
        self.time_of_day = "night"

        print("MainAgent has started.")


def update_screen(agent):
    """
    Continuously captures the screen (screenshot) until the 'q' key is pressed
    """

    t0 = time.time()
    fps_report_delay = 5
    fps_report_time = time.time()

    while True:
        agent.frame = ImageGrab.grab()
        agent.frame = np.array(agent.frame)
        agent.frame = cv.cvtColor(agent.frame, cv.COLOR_RGB2BGR)
        agent.frame_HSV = cv.cvtColor(agent.frame, cv.COLOR_BGR2HSV)

        # cv.imshow("window", agent.frame)
        key = cv.waitKey(1)
        if key == ord("q"):
            break

        # Calculate the FPS
        execution_time = time.time() - t0
        if time.time() - fps_report_time >= fps_report_delay:
            print(f"FPS: {str(1/execution_time)}")
            fps_report_time = time.time()

        t0 = time.time()
        time.sleep(0.005)


def print_menu():
    print("Enter a command:")
    print("\tS\tStart the main agent")
    print("\tZ\tSet zone")
    print("\tF\tStart the fishing agent")
    print("\tQ\tQuit")


if __name__ == "__main__":
    main_agent = MainAgent()

    # update_screen()

    print_menu()
    while True:
        user_input = str.lower(input()).strip()

        if user_input == "s":
            update_screen_thread = Thread(
                target=update_screen,
                args=(main_agent,),
                name="screenshot_thread",
                daemon=True,
            )
            update_screen_thread.start()
            print("Thread started")

        elif user_input == "z":
            pass

        elif user_input == "f":
            fishing_agent = FishingAgent(main_agent)
            fishing_agent.run()

        elif user_input == "q":
            print("Quitting ...")
            cv.destroyAllWindows()

        else:
            print("Invalid selection")
            print_menu()
