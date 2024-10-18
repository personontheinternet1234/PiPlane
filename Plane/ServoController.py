from gpiozero import AngularServo
from time import sleep
import Util


class ServoController:

    def __init__(self):
        self.servos = {}

    def setup_servos(self):
        self.servos["rightFlap"] = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
        # self.servos["rightFlap"] = AngularServo(19, min_pulse_width=0.0006, max_pulse_width=0.0023)

        for servo in self.servos.values():
            Util.zero(servo)

    def dance(self):
        for servo in self.servos.values():
            for i in range(3):
                Util.zero(servo)
                sleep(1)
                Util.change_servo_angle(servo, 50)
                sleep(1)
                Util.zero(servo)
                sleep(1)
                Util.change_servo_angle(servo, -50)
                sleep(1)

    def increase_pitch(self):
        self.servos["rightFlap"]

