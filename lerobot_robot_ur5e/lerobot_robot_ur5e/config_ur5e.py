from dataclasses import dataclass, field

from lerobot.cameras.realsense.configuration_realsense import (
    RealSenseCameraConfig,
)

from lerobot.robots import RobotConfig


@RobotConfig.register_subclass("ur5e")
@dataclass
class UR5EConfig(RobotConfig):
    ip: str

    cameras: dict = field(
        default_factory=lambda: {
            "external": RealSenseCameraConfig(
                serial_number_or_name="425122300243",
                width=640,
                height=480,
                fps=30,
            ),

            "wrist": RealSenseCameraConfig(
                serial_number_or_name="419222300600",
                width=640,
                height=480,
                fps=30,
            ),
        }
    )