import pyrobotiqgripper as rq

gripper = rq.RobotiqGripper(
    connection_type=rq.GRIPPER_MODE_RTU_VIA_TCP,
    tcp_host="192.168.1.101"
)

gripper.connect()

gripper.open()
