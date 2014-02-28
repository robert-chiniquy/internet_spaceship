from internet_spaceships import base


class Firmware(base.BaseFirmware):
    def input(self):
        """ Implement your code here. This will be called on every tick after
        the class data has been set up from the JSON.
        """
        print "Woo!"


if __name__ == "__main__":
    """ This sets up your firmware when you run "firmware.py" with some JSON
    input.
    """
    firmware = Firmware()
    firmware.start()