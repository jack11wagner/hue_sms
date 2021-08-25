class mockphone:

    def __init__(self):
        self.phoneNumber = None
        self.message = ""

    def getNumber(self):
        return self.phoneNumber

    def setNumber(self, numberInput):
        self.phoneNumber = numberInput

    # Allows value for message variable to be set, in order to test that message sent from from self.phoneNumber
    def setMessage(self, messageBody):
        self.message = messageBody

    def getMessage(self):
        return self.message
