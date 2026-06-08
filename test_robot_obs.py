from lerobot_robot_ur5e.ur5e import UR5E
from lerobot_robot_ur5e.config_ur5e import UR5EConfig

robot = UR5E(
    UR5EConfig(
        ip="192.168.1.101"
    )
)

robot.connect()

obs = robot.get_observation()

print("\n=== OBS KEYS ===")
print(obs.keys())

print("\n=== TACTILE ===")
print(type(obs["tactile"]))
print(obs["tactile"].shape)

print("\n=== LEFT ===")
print(obs["tactile"][0].sum())

print("\n=== RIGHT ===")
print(obs["tactile"][1].sum())

robot.disconnect()
