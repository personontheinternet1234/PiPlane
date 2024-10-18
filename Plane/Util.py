from gpiozero import AngularServo


def zero(servo):
    servo.angle = 0


def change_servo_angle(servo, value):
    if value > 0 and servo.angle < 90:
        servo.angle += value
    elif value < 0 and servo.angle > -90:
        servo.angle += value




