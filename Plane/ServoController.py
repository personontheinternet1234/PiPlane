from time import time
import board
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from time import sleep
import math
import threading
MIN_THROTTLE = 204
MAX_THROTTLE = 410

class ServoController:

    def __init__(self):
        self.pca = PCA9685(busio.I2C(board.SCL, board.SDA))
        self.pca.deinit()
        self.pca.frequency = 50

        self.right_flap = servo.Servo(self.pca.channels[0])
        self.left_flap = servo.Servo(self.pca.channels[1])
        self.rudder = servo.Servo(self.pca.channels[2])

        self.camera_pitch = servo.Servo(self.pca.channels[4])
        self.camera_yaw = servo.Servo(self.pca.channels[5])

        self.motor = self.pca.channels[15]
        self.motor.duty_cycle = int(204 * 65536 / 4096)
        self.throttle = 204

        self.servos = [self.right_flap, self.left_flap, self.rudder, self.camera_pitch, self.camera_yaw]

        self.coefficient_product = 6

        self.recover_right_flap = True
        self.recover_left_flap = True
        self.recover_rudder = True
        self.right_flap_last_update = time()
        self.left_flap_last_update = time()
        self.rudder_last_update = time()

        self.lock = threading.Lock()

    def start_threads(self):
        threading.Thread(target=self.normalize_servo_angles).start()

    def setup_servos(self):
        for servo in self.servos:
            self.zero(servo)

    def normalize_servo_angles(self):
        while True:
            sleep(0.001)

            if (self.recover_right_flap):
                if self.right_flap.angle > 90:
                    self.change_servo_angle(self.right_flap, -2)
                elif self.right_flap.angle < 90:
                    self.change_servo_angle(self.right_flap, 2)
            elif (time() - self.right_flap_last_update) > 0.10:
                self.recover_right_flap = True

            if (self.recover_left_flap):
                if self.left_flap.angle > 90:
                    self.change_servo_angle(self.left_flap, -2)
                elif self.left_flap.angle < 90:
                    self.change_servo_angle(self.left_flap, 2)
            elif (time() - self.left_flap_last_update) > 0.10:
                self.recover_left_flap = True

            if (self.recover_rudder):
                if self.rudder.angle > 90:
                    self.change_servo_angle(self.rudder, -2)
                elif self.rudder.angle < 90:
                    self.change_servo_angle(self.rudder, 2)
            elif (time() - self.rudder_last_update) > 0.10:
                self.recover_rudder = True
    
    def apply_motion_packet(self, delta_pitch, delta_yaw, delta_roll):
        right_flap_delta = delta_pitch + -1 * delta_roll
        left_flap_delta = -1 * delta_pitch + -1 * delta_roll
        rudder_delta = delta_yaw

        self.change_servo_angle(self.right_flap, right_flap_delta)
        self.change_servo_angle(self.left_flap, left_flap_delta)
        self.change_servo_angle(self.rudder, rudder_delta)

        if (right_flap_delta == 0):
            self.recover_right_flap = True
        else:
            self.recover_right_flap = False
            self.right_flap_last_update = time()

        if (left_flap_delta == 0):
            self.recover_left_flap = True
        else:
            self.recover_left_flap = False
            self.left_flap_last_update = time()

        if (rudder_delta == 0):
            self.recover_rudder = True
        else:
            self.recover_rudder = False
            self.rudder_last_update = time()

    def apply_camera_rotation_packet(self, delta_camera_pitch, delta_camera_yaw):
        self.change_servo_angle(self.camera_pitch, delta_camera_pitch)
        self.change_servo_angle(self.camera_yaw, delta_camera_yaw)
    
    def apply_throttle_packet(self, delta_throttle):
        self.set_throttle(self.throttle + delta_throttle)

    def zero(self, servo):
        servo.angle = 90

    def change_servo_angle(self, servo:servo.Servo, value:float):
        with self.lock:
            if value > 0 and (servo.angle + value) < 180:
                servo.angle = servo.angle + value
            if value < 0 and (servo.angle + value) > 0:
                servo.angle = servo.angle + value

    def set_throttle(self, power):
        if MIN_THROTTLE <= power <= MAX_THROTTLE:
            duty_cycle = int(power * 65536 / 4096)
            self.motor.duty_cycle = duty_cycle
            self.throttle = power
            print(f"New throttle: {self.throttle}")
        else:
            print(f"Throttle power must be between {MIN_THROTTLE} and {MAX_THROTTLE}. Currently {self.throttle}")

    def stop_motor(self):
        stop_value = int(MIN_THROTTLE * 65536 / 4096)
        self.motor.duty_cycle = stop_value
        self.throttle = MIN_THROTTLE

    def dance(self):
        self.setup_servos()
        for i in range(3):
            for servo in self.servos:
                self.change_servo_angle(servo, 30)
            sleep(1)
        self.setup_servos()

