from dataclasses import dataclass
from typing import Optional
import numpy as np
from cv2 import Mat

@dataclass
class MainAgent:
    """
    The main AI of the application that controls all other agents
    """
    agents: list
    frame: Optional[Mat]
    frame_HSV: Optional[Mat]
    time_of_day: str = 'night'
    zone: str = 'Valdrakken'

    def __init__(self) -> None:
        # self.agents = []
        # self.fishing_thead = None

        # self.frame = None  # BGR Image
        # self.frame_HSV = None  # HSV Image

        # self.zone = "Valdrakken"
        # self.time_of_day = "night"

        print("MainAgent has started.")