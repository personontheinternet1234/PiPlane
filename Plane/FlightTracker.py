import threading
import datetime

class FlightTracker:

    def __init__(self, imu, gps):
        self.imu = imu
        self.gps = gps

        self.data_file = f"{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))}.csv"
        with open(self.data_file, 'a') as file:
            file.write(f"time,pitch,heading,roll,latitude,longitude")

    def start_threads(self):
        threading.Thread(target=self.log).start()

    def log(self):
        while True:
            with open(self.data_file, 'a') as file:
                file.write(f"{datetime.datetime.now().strftime()},{self.imu.pitch},{self.imu.tiltCompensatedHeading},{self.imu.roll},{self.gps.latitude},{self.gps.longitude}")
                # file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')},pitch,heading,roll,latitude,longitude\n")

if __name__ == "__main__":
    f = FlightTracker("","")
    f.start_threads()


