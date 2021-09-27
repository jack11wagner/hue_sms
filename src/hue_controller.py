import rgbxy
from phue import Bridge, PhueException
import name_converter
from rgbxy import Converter
from name_converter import clean_name
import logging
from getRedisColor import getColor

logging.basicConfig(level=logging.INFO,filename="hue_log.log",
                    format="%(asctime)s:%(levelname)s:%(message)s"	)

saturation_val = 0
branch_value = 0
# IP_address = '192.168.4.64'
IP_address = '172.31.229.35'


class HueController:

    def __init__(self):
        self.bridge = None
        self.light = None
        self.name_to_color = name_converter.NameConverter()

    def connect(self):
        if self.light is not None:
            return

        self.bridge = Bridge(IP_address)
        self.bridge.connect()
        logging.info("Server was successfully able to connect to the bridge")
        self.light = self.bridge.lights[0]

