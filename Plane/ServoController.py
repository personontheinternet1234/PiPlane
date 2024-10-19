from gpiozero import AngularServo
from time import sleep
from PlaneUtil import zero, change_servo_angle


class ServoController:

    def __init__(self):
        self.servos = {}

    def setup_servos(self):
        self.servos["rightFlap"] = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
        # self.servos["leftFlap"] = AngularServo(19, min_pulse_width=0.0006, max_pulse_width=0.0023)
        # self.servos["rudder"] = AngularServo(20, min_pulse_width=0.0006, max_pulse_width=0.0023)

        for servo in self.servos.values():
            zero(servo)

    def dance(self):
        for servo in self.servos.values():
            for i in range(3):
                zero(servo)
                sleep(1)
                change_servo_angle(servo, 50)
                sleep(1)
                zero(servo)
                sleep(1)
                change_servo_angle(servo, -50)
                sleep(1)

    def change_pitch(self, value):
        # positive value for up, negative for down
        change_servo_angle(self.servos["rightFlap"], -1 * value)
        change_servo_angle(self.servos["leftFlap"], -1 * value)

    def change_yaw(self, value):
        # negative value for left, positive for right
        change_servo_angle(self.servos["rudder"], -1 * value)

    def change_roll(self, value):
        # positive for whichever side you want to roll, so pass +value to roll right, -value to roll left
        change_servo_angle(self.servos["rightFlap"], value)
        change_servo_angle(self.servos["leftFlap"], -1 * value)

