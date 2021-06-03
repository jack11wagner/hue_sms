from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from hue_controller import HueController
from name_converter import clean_name
from data_writer import writeFile,colorPercent,mostRecentColors,numOfEachColor,invalidColors,firstEntryDate
import random
import logging

logging.basicConfig(level=logging.INFO,filename="hue_log.log",
                    format="%(asctime)s:%(levelname)s:%(message)s"	)

app = Flask(__name__)
controller = HueController()
file = "data.csv"

@app.route('/', methods=['POST', 'GET'])
def set_color():
    phone_number = request.values.get('From', None)
    color_name = request.values.get('Body', None)
    color_name = clean_name(color_name)

    if color_name == "black":
        response = MessagingResponse()
        response.message("Haha... please use a color that contains light.")
        return str(response)

    if color_name == "options":
        response = MessagingResponse()
        response.message("\n***Options***\n-------------------------------\n"
                         +"'Options' - list all options for Philips Light functions\n"+
                         "'Colors List' - link to list of color choices\n"
                         "'Random' - chooses a random color for the light")
        return str(response)
    if color_name == "colors list":
        response = MessagingResponse()
        response.message(
                "List of color choices:" + "https://en.wikipedia.org/wiki/List_of_Crayola_crayon_colors"
                )
        return str(response)

    if color_name == "random":
        colors_file = open("colors.csv")
        randomint = random.randint(1, 162)
        i = 0
        for line in colors_file:
            line = line.strip()
            name, r, g, b = line.split(',')
            placeholder = name
            if i == randomint:
                color_name = placeholder
            i += 1
        response = MessagingResponse()
        response.message("You chose a random color.  The choice was " + color_name)

    message = controller.set_color(color_name)
    percent = colorPercent(file, color_name)
    date = firstEntryDate(file)
    response = MessagingResponse()
    response.message(message + " This entry has been chosen {:.1f}".format(percent) + "% of the time since " + date + "!")
    logging.info("Color " + color_name + " has been set by the phone number " + phone_number + ".")
    writeFile(file, str(phone_number), str(color_name), str(message))

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
