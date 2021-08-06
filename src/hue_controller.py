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

    def set_color(self, color_name, is_random):
        try:
            self.connect()
        except PhueException:
            logging.info("Server unable to connect to the Hue Light")
            return "I'm sorry, but I cannot connect to the Hue Light." \
                   "Please try again later."

        rgb_values = getColor(color_name)

        if rgb_values is None:
            logging.info("Color " + color_name + " was not recognized")
            return "I'm sorry, but I don't recognize " \
                   "the color \"{}\".".format(color_name)

        (r, g, b) = rgb_values.decode("utf-8").split(',')
        r = int(r)
        g = int(g)
        b = int(b)

        converter = Converter()
        print(r, " ", g, " ", b)
        if r == 255 and b == 255 and g == 255:
            saturation_val = 0
            [x, y] = converter.rgb_to_xy(r, g, b)
        else:
            saturation_val = 255
            correction_value = 1.3
            [x, y] = converter.rgb_to_xy(r, g, b)
        try:
            self.light.xy = (x, y)
            self.light.saturation = saturation_val
            logging.info("The light was changed to the color " + color_name)
            if is_random:
                return "The light was changed to the color \"{}\". Random was used." \
                    .format(clean_name(color_name))
            else:
                return "The light was changed to the color \"{}\"."\
                .format(clean_name(color_name))
        except PhueException:
            logging.info("Server unable to connect to the Hue Light")
            return "I'm sorry, but I cannot connect to the Hue Light." \
                   "Please try again later."
