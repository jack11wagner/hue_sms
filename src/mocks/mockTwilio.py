from hue_controller import HueController
from name_converter import clean_name
from mockPhone import mockphone

controller = HueController()
phone = mockphone()

class mocktwilio:

    def __init__(self):
        self.message = None
        self.number = phone.getNumber()


    def setMessage(self, message_inputted):
        self.message = message_inputted

    def getMessage(self):
        return self.message

    def setNumber(self, number_inputted):
        if isinstance(number_inputted, int) & len(str(number_inputted)) == 10:
            self.number = number_inputted
        else:
            return "Invalid number"

    def getNumber(self):
        return self.number

    # Takes length 2 array as response
    # responseNum is a 10 digit int
    # responseMessage is a string
    def testResponse(self, response_num, response_message):
        if isinstance(response_num, int) & len(str(response_num)) == 10 & isinstance(response_message, str):
            return True
        else:
            return False

    def sendMessage(self):
        controller.set_color(clean_name(self.message))
