import threading
import queue
import math

class NavigationManager:

    def __init__(self, servoController, imu, gps):
        self.fix = None
        self.waypoints = queue.Queue()
        self.servoController = servoController
        self.imu = imu
        self.gps = gps

    def start_threads(self):
        threading.Thread(target=self.seek_waypoint).start()

    def seek_waypoint(self):
        while True:
            if self.waypoints.qsize > 0:
                waypoint = self.waypoints.get_nowait()
                desired_heading = math.atan((waypoint[0] - self.gps.latitude) / (waypoint[1] - self.gps.longitude))
                rudder_angle = self.imu.tiltCompensatedHeading - desired_heading
                self.servoController.change_servo_angle(self.servoController.rudder, rudder_angle)
                self.waypoints.task_done()
                
    def add_waypoint(self, waypoint:tuple):
        self.waypoints.put(waypoint)