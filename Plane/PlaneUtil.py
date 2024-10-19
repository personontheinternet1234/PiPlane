from gpiozero import AngularServo


class ServoWrapper:

    def __init__(self, servo, angle):
        self.servo = servo
        self.angle = angle


def zero(servo_wrapper):
    servo_wrapper.servo.angle = 0
    servo_wrapper.angle = 0


def change_servo_wrapper_angle(servo_wrapper, value):
    servo = servo_wrapper.servo
    if value > 0 and (servo.angle + value) < 90:
        servo.angle += value
        servo_wrapper.angle += value
    elif value < 0 and (servo.angle + value) > -90:
        servo.angle += value
        servo_wrapper.angle += value



