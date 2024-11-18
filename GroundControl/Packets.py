import json


class MotionPacket:


    def __init__(self, delta_pitch, delta_yaw, delta_roll):
        self.delta_pitch = delta_pitch
        self.delta_yaw = delta_yaw
        self.delta_roll = delta_roll

    def encode(self):
        return ("{\"motion\": " +
                "{\"delta_pitch\": " + str(self.delta_pitch)
                + ",\"delta_yaw\": " + str(self.delta_yaw)
                + ",\"delta_roll\": " + str(self.delta_roll) + "}}").encode("utf-8")


class TestPacket:


    def __init__(self):
        pass

    def encode(self):
        return ("{\"flag\": {\"lol i had to make this it was hard :( if you found this reply to the email\": " + str(1) + "}}").encode("utf-8")


