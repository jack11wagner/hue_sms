import time
from phue import PhueException
from rgbxy import Converter
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from getRedisColor import getColor
from hue_controller import HueController
from name_converter import clean_name
from data_writer import writeFile, color_percent, mostRecentColors, numOfEachColor, invalidColors, first_entry_date
import random, logging, redis
from fuzzyColors import getFuzzyColor
from PIL import ImageColor

logging.basicConfig(level=logging.INFO, filename="hue_log.log",
                    format="%(asctime)s:%(levelname)s:%(message)s")

app = Flask(__name__)
controller = HueController()
file = "data.csv"


def HEX_to_RGB(hexcode_color):
    try:
        r, g, b = ImageColor.getcolor(hexcode_color, 'RGB')
        rgb_string = str(r) + ',' + str(g) + ',' + str(b)
        return rgb_string
    except ValueError:
        return None


def convert(rgb_values):
    if type(rgb_values) != str:
        (r, g, b) = rgb_values.decode("utf-8").split(',')
    else:
        (r, g, b) = rgb_values.split(',')
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
        [x, y] = converter.rgb_to_xy(r, g, b)

    return x, y, saturation_val


def get_colors_list_from_redis(database):
    list_of_colors = []
    for color in database.hgetall('color_totals').keys():
        color = color.decode('utf-8')
        list_of_colors.append(color)
    return list_of_colors


@app.route('/', methods=['POST', 'GET'])
def set_color():
    is_random = False
    is_Fuzzy = False
    is_Hex = False
    is_Rainbow = False

    database = redis.Redis(host='localhost', port=6379, db=0)

    list_of_colors = get_colors_list_from_redis(database)

    phone_number = request.values.get('From', None)
    unclean_color_name = request.values.get('Body', None)
    if unclean_color_name.startswith("#"):
        is_Hex = True
    color_name = clean_name(unclean_color_name)

    if color_name == "rainbow":
        # Adds short rainbow sequence capability for a few seconds
        is_Rainbow = True
        total_time = 15  # in seconds
        transitionTime = .25  # in seconds
        maxHue = 65535
        hueIncrement = maxHue / total_time
        try:
            controller.connect()
        except PhueException:
            logging.info("Server unable to connect to the Hue Light")
            response = MessagingResponse()
            response.message("Server unable to connect to the Hue Light")
            return str(response)

        light = controller.light
        light.transitiontime = transitionTime * 10
        light.brightness = 254
        light.saturation = 254
        # light.on = True # uncomment to turn all lights on

        hue = 0
        currTime = time.time()
        elapsed_time = time.time() - currTime
        while elapsed_time < total_time:
            light.hue = hue
            hue = (hue + hueIncrement) % maxHue
            time.sleep(transitionTime)
            elapsed_time = time.time() - currTime

        response = MessagingResponse()
        response.message("Did you enjoy the rainbow light show?")
        return str(response)

    if color_name == "black":
        response = MessagingResponse()
        response.message("Haha... please use a color that contains light.")
        return str(response)

    if color_name == "options":
        response = MessagingResponse()
        response.message("\n***Options***\n-------------------------------\n"
                         + "'Options' - list all options for Philips Light functions\n" +
                         "'Colors List' - link to list of color choices\n"
                         "'Random' - chooses a random color for the light")
        return str(response)

    if color_name == "colors list":
        response = MessagingResponse()
        response.message(
            "List of color choices:" + "https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors"
        )
        return str(response)

    try:
        controller.connect()
    except PhueException:
        logging.info("Server unable to connect to the Hue Light")
        response = MessagingResponse()
        response.message("Server unable to connect to the Hue Light")
        return str(response)

    if color_name == "random":
        is_random = True
        color_sum = int(database.get('color_sum').decode('utf-8'), base=10)
        random_int = random.randint(1, color_sum)
        color_name = list_of_colors[random_int]
        database.hincrby('color_totals', 'random', 1)
        database.incr('total', 1)
    else:
        if color_name not in list_of_colors:
            # Checking to see if color is not in list_of_colors due to possible misspelling
            fuzzy_Color = getFuzzyColor(color_name)
            if fuzzy_Color is not None:
                is_Fuzzy = True
                color_name = clean_name(fuzzy_Color)

        if color_name in list_of_colors:
            database.hincrby('color_totals', color_name, 1)
            database.incr('total', 1)

    if is_Hex:
        rgb_values = HEX_to_RGB(unclean_color_name)

    else:
        rgb_values = getColor(color_name)

    if rgb_values is None:
        logging.info("Color " + color_name + " was not recognized")
        response = MessagingResponse()
        response.message("I'm sorry, but I don't recognize the color \"{}\".".format(color_name))
        return str(response)

    [x, y, saturation_val] = convert(rgb_values)

    try:
        controller.light.xy = (x, y)
        controller.light.saturation = saturation_val
        logging.info("The light was changed to the color " + color_name)
        if is_Rainbow:
            message = "Did you enjoy the rainbow light show?"
        if is_random:
            message = "The light was changed to the color \"{}\". Random was used." \
                .format(clean_name(color_name))
        elif is_Fuzzy:
            message = "We found a color similar to what you requested... The light was changed to the color \"{}\"".format(
                clean_name(color_name))
        elif is_Hex:
            message = "You requested a Hex Color... The light was changed to the Hex \"{}\"".format(
                unclean_color_name)

        else:
            message = "The light was changed to the color \"{}\"." \
                .format(clean_name(color_name))
    except PhueException:
        logging.info("Server unable to connect to the Hue Light")
        response = MessagingResponse()
        response.message("I'm sorry, but I cannot connect to the Hue Light. Please try again later.")
        return str(response)

    if is_random:
        color_name = 'random'
    if is_Hex:
        response = MessagingResponse()
        response.message(message)
        return str(response)

    percent = color_percent(color_name)
    writeFile(file, str(phone_number), str(color_name), str(message))
    date = first_entry_date(file)
    response = MessagingResponse()
    response.message(
        message + " This entry has been chosen {:.1f}".format(percent) + "% of the time since " + date + "!")
    logging.info("Color " + color_name + " has been set by the phone number " + phone_number + ".")

    return str(response)


@app.route('/recents', methods=['GET'])
def get_most_recent():
    return mostRecentColors(file)


@app.route('/number', methods=['GET'])
def get_num_of_each():
    return numOfEachColor(file)


@app.route('/invalids', methods=['GET'])
def get_invalids():
    return invalidColors(file)


if __name__ == '__main__':
    app.run()
    logging.info("Server has been stopped")
