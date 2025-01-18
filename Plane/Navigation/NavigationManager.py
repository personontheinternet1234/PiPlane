import threading
import queue
import math

class Waypoint:

    def __init__(self, latitude:float, longitude:float):
        self.latitude = latitude
        self.longitude = longitude


class NavigationManager:

    def __init__(self, servoController, imu, gps):
        self.fix = None
        self.waypoints = []
        self.current_waypoint = None
        self.servoController = servoController
        self.imu = imu
        self.gps = gps

    def start_threads(self):
        threading.Thread(target=self.seek_waypoint).start()

    def seek_waypoint(self):
        while True:
            if len(self.waypoints) > 0:
                self.current_waypoint = self.waypoints[0]
                desired_heading = math.atan2((self.current_waypoint.latitude - self.gps.latitude) / (self.current_waypoint.longitude - self.gps.longitude))
                rudder_angle = self.imu.tiltCompensatedHeading - desired_heading
                self.servoController.change_servo_angle(self.servoController.rudder, rudder_angle)

                if self.check_achieved_location(self.current_waypoint):
                    self.waypoints = self.waypoints.pop(0)

    def check_achieved_location(self, waypoint):
        threshold = 0.0001
        if abs(self.gps.latitude - waypoint.latitude) < threshold and abs(self.gps.longitude - waypoint.longitude) < threshold:
            return True
                
    def add_waypoint(self, waypoint:tuple):
        self.waypoints.append(waypoint)