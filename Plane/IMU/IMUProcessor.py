#!/usr/bin/python
import time
import math
import IMU.BerryIMU as BerryIMU
import datetime
import os
import sys
import threading

class IMUProcessor:

    def __init__(self):
        self.RAD_TO_DEG = 57.29578
        self.M_PI = 3.14159265358979323846
        self.G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
        self.AA =  0.40      # Complementary filter constant

        ################# Compass Calibration values ############
        # Use calibrateBerryIMU.py to get calibration values
        # Calibrating the compass isnt mandatory, however a calibrated
        # compass will result in a more accurate heading values.
        self.magXmin =  0
        self.magYmin =  0
        self.magZmin =  0
        self.magXmax =  0
        self.magYmax =  0
        self.magZmax =  0
        ############### END Calibration offsets #################

        self.gyroXangle = 0.0
        self.gyroYangle = 0.0
        self.gyroZangle = 0.0
        self.CFangleX = 0.0  # matters
        self.CFangleY = 0.0  # matters

        self.AccXangle = None
        self.AccYangle = None

        self.a = None
        self.ACCx = None
        self.ACCy = None
        self.ACCz = None
        self.GYRx = None
        self.GYRy = None
        self.GYRz = None
        self.MAGx = None
        self.MAGy = None
        self.MAGz = None

        self.pitch = None  # matters
        self.heading = None  # matters; yaw
        self.roll = None  # matters
    
        
    def start_threads(self):
        threading.Thread(target=self.run).start()

    def setup(self):
        BerryIMU.detectIMU()     #Detect if BerryIMU is connected.
        if(BerryIMU.BerryIMUversion == 99):
            print(" No BerryIMU found... exiting ")
            sys.exit()
        BerryIMU.initIMU()       #Initialise the accelerometer, gyroscope and compass

        self.a = datetime.datetime.now()

    def run(self):
        while True:
            #Read the accelerometer,gyroscope and magnetometer values
            self.ACCx = BerryIMU.readACCx()
            self.ACCy = BerryIMU.readACCy()
            self.ACCz = BerryIMU.readACCz()
            self.GYRx = BerryIMU.readGYRx()
            self.GYRy = BerryIMU.readGYRy()
            self.GYRz = BerryIMU.readGYRz()
            self.MAGx = BerryIMU.readMAGx()
            self.MAGy = BerryIMU.readMAGy()
            self.MAGz = BerryIMU.readMAGz()

            #Apply compass calibration
            self.MAGx -= (self.magXmin + self.magXmax) / 2
            self.MAGy -= (self.magYmin + self.magYmax) / 2
            self.MAGz -= (self.magZmin + self.magZmax) / 2

            ##Calculate loop Period(LP). How long between Gyro Reads
            self.b = datetime.datetime.now() - self.a
            self.a = datetime.datetime.now()
            LP = self.b.microseconds/(1000000*1.0)
            outputString = "Loop Time %5.2f " % ( LP )

            #Convert Gyro raw to degrees per second
            rate_gyr_x = self.GYRx * self.G_GAIN
            rate_gyr_y = self.GYRy * self.G_GAIN
            rate_gyr_z = self.GYRz * self.G_GAIN

            #Calculate the angles from the gyro.
            self.gyroXangle += rate_gyr_x*LP
            self.gyroYangle += rate_gyr_y*LP
            self.gyroZangle += rate_gyr_z*LP

            #Convert Accelerometer values to degrees
            self.AccXangle = (math.atan2(self.ACCy,self.ACCz) * self.RAD_TO_DEG)
            self.AccYangle = (math.atan2(self.ACCz,self.ACCx) + self.M_PI) * self.RAD_TO_DEG

            #convert the values to -180 and +180
            if self.AccYangle > 90:
                self.AccYangle -= 270.0
            else:
                self.AccYangle += 90.0

            #Complementary filter used to combine the accelerometer and gyro values.
            self.CFangleX = self.AA * (self.CFangleX + rate_gyr_x*LP) + (1 - self.AA) * self.AccXangle
            self.CFangleY = self.AA * (self.CFangleY + rate_gyr_y*LP) + (1 - self.AA) * self.AccYangle

            #Calculate heading
            self.heading = 180 * math.atan2(self.MAGy, self.MAGx) / self.M_PI

            #Only have our heading between 0 and 360
            if self.heading < 0:
                self.heading += 360

            ##################### START Tilt Compensation ########################

            #Normalize accelerometer raw values.
            accXnorm = self.ACCx / math.sqrt(self.ACCx * self.ACCx + self.ACCy * self.ACCy + self.ACCz * self.ACCz)
            accYnorm = self.ACCy / math.sqrt(self.ACCx * self.ACCx + self.ACCy * self.ACCy + self.ACCz * self.ACCz)

            #Calculate pitch and roll
            self.pitch = math.asin(accXnorm)
            self.roll = -math.asin(accYnorm/math.cos(self.pitch))

            #Calculate the new tilt compensated values
            #The compass and accelerometer are orientated differently on the the BerryIMUv1, v2 and v3.
            #This needs to be taken into consideration when performing the calculations

            #X compensation
            if(BerryIMU.BerryIMUversion == 1 or BerryIMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
                magXcomp = self.MAGx * math.cos(self.pitch) + self.MAGz * math.sin(self.pitch)
            else:                                                                #LSM9DS1
                magXcomp = self.MAGx * math.cos(self.pitch) - self.MAGz * math.sin(self.pitch)

            #Y compensation
            if(BerryIMU.BerryIMUversion == 1 or BerryIMU.BerryIMUversion == 3):            #LSM9DS0 and (LSM6DSL & LIS2MDL)
                magYcomp = self.MAGx * math.sin(self.roll) * math.sin(self.pitch) + self.MAGy * math.cos(self.roll) - self.MAGz * math.sin(self.roll)*math.cos(self.pitch)
            else:                                                                #LSM9DS1
                magYcomp = self.MAGx * math.sin(self.roll) * math.sin(self.pitch) + self.MAGy*math.cos(self.roll) + self.MAGz * math.sin(self.roll)*math.cos(self.pitch)

            #Calculate tilt compensated heading
            tiltCompensatedHeading = 180 * math.atan2(magYcomp, magXcomp) / self.M_PI

            if tiltCompensatedHeading < 0:
                tiltCompensatedHeading += 360

            ##################### END Tilt Compensation ########################


            if 0:                       #Change to '0' to stop showing the angles from the accelerometer
                outputString += "#  ACCX Angle %5.2f ACCY Angle %5.2f  #  " % (self.AccXangle, self.AccYangle)

            if 0:                       #Change to '0' to stop  showing the angles from the gyro
                outputString +="\t# GRYX Angle %5.2f  GYRY Angle %5.2f  GYRZ Angle %5.2f # " % (self.gyroXangle, self.gyroYangle, self.gyroZangle)

            if 1:                       #Change to '0' to stop  showing the angles from the complementary filter
                outputString +="\t#  CFangleX Angle %5.2f   CFangleY Angle %5.2f  #" % (self.CFangleX, self.CFangleY)

            if 1:                       #Change to '0' to stop  showing the heading
                outputString +="\t# HEADING %5.2f  tiltCompensatedHeading %5.2f #" % (self.heading, tiltCompensatedHeading)


            print(outputString)

            #slow program down a bit, makes the output more readable
            time.sleep(0.03)

