from ServoController import ServoController
from PlaneReceiver import PlaneReceiver
import Util


if __name__ == "__main__":
    servoController = ServoController()
    servoController.setup_servos()
    # servoController.dance()

    ip = "192.168.1.14"
    planeReceiver = PlaneReceiver(ip, 5559, servoController)
    planeReceiver.start_threads()


