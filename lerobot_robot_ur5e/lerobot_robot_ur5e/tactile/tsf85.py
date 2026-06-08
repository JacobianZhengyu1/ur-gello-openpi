import time
import serial
import numpy as np

from .protocol import UsbPacketParser


class TSF85:
    """
    Robotiq TSF-85 tactile sensor.

    Returns:
        tactile.shape == (2, 4, 7)

    tactile[0] -> finger 0
    tactile[1] -> finger 1
    """

    def __init__(
        self,
        port="/dev/ttyACM0",
        baudrate=115200,
    ):
        self.port = port
        self.baudrate = baudrate

        self.ser = None
        self.parser = None

    def connect(self):

        print(f"[TSF85] Opening {self.port}")

        self.ser = serial.Serial(
            self.port,
            self.baudrate,
            timeout=0.01,
        )

        self.parser = UsbPacketParser()

        # Same initialization as official quick_connect.py
        self.ser.dtr = True
        self.ser.rts = False

        time.sleep(0.2)

        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.parser.buffer.clear()

        print("[TSF85] Starting autosend")

        cmd = self.parser.create_autosend_command(1)

        self.ser.write(cmd)
        self.ser.flush()

        time.sleep(0.2)

        print("[TSF85] Connected")

    def disconnect(self):

        if self.ser is not None:

            try:
                cmd = self.parser.create_autosend_command(0)

                self.ser.write(cmd)
                self.ser.flush()

            except Exception:
                pass

            self.ser.close()

        print("[TSF85] Disconnected")

    def _update_parser(self):

        waiting = self.ser.in_waiting

        if waiting <= 0:
            return

        data = self.ser.read(waiting)

        packets = self.parser.feed_bytes(data)

        for packet in packets:
            try:
                self.parser.parse_sensor_packet(packet)
            except Exception:
                pass

    def read(self):

        self._update_parser()

        sensor_data = self.parser.get_sensor_data()

        finger0 = np.array(
            sensor_data.fingers[0].static_tactile,
            dtype=np.float32,
        )

        finger1 = np.array(
            sensor_data.fingers[1].static_tactile,
            dtype=np.float32,
        )

        # 28 taxels
        if finger0.size != 28:
            finger0 = np.zeros(28, dtype=np.float32)

        if finger1.size != 28:
            finger1 = np.zeros(28, dtype=np.float32)

        finger0 = finger0.reshape(4, 7)
        finger1 = finger1.reshape(4, 7)

        tactile = np.stack(
            [finger0, finger1],
            axis=0,
        )

        return tactile