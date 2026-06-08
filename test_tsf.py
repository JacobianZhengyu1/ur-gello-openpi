import time
import numpy as np

from lerobot_robot_ur5e.tactile.tsf85 import TSF85

sensor = TSF85()
sensor.connect()

while True:

    tactile = sensor.read()

    print(
        "L =", tactile[0].sum(),
        "R =", tactile[1].sum(),
    )

    time.sleep(0.1)