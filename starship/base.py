import json
import sys


class BaseSpaceship(object):
    sensors = {
        'position': 'update_position',
        'velocity': 'update_velocity',
    }

    def __init__(self, initial_position):
        """ initial_position is a tuple in the form (x,y)
        """
        # throttle can be 0 to 100
        self._throttle = 0
        # heading can be 0 ('north') through 359, going clockwise
        self._heading = 0

        # You shouldn't change these.
        self.x, self.y = initial_position
        self.velocity = 0

    def input(self):
        """ This function will be called every time data is sent to the
        starship by the game. You must implement this in spaceship.py if you
        want your ship to do anything.
        """
        raise NotImplementedError("You must implement the read_input function"
                                  ".")

    @property
    def heading(self):
        """ Heading can be anything between 0 ('north') to 359,
        going clockwise.
        """
        return self._heading

    @heading.setter
    def heading(self, value):
        if not 0 <= value <= 359:
            raise ValueError("Heading must be between 0 and 359")
        self._heading = value

    @property
    def throttle(self):
        """ Throttle is any integer between 0 and 100.
        """
        return self._throttle

    @throttle.setter
    def throttle(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Heading must be between 0 and 359")
        self._throttle = value

    def write_output(self):
        """ Send data back to the server.
        """
        data = {
            'position': (self.x, self.y),
            'throttle': self.throttle
        }
        print json.dumps(data)

    def update_sensors(self, json_lines):
        """ Take the sensor data and update our sensors, then call input.
        """
        for sensor, sensor_func in self.sensors.items():
            if sensor in json_lines:
                # Send the sensor data to the sensor func
                getattr(self, sensor_func)(json_lines[sensor])
        self.input()

    def update_position(self, current_position):
        """ Takes a position dict from the input and updates the ships
        position.
        """
        self.x, self.y = current_position

    def update_velocity(self, current_velocity):
        self.velocity = current_velocity

    def start(self):
        read_lines = ""
        while 1:
            input = sys.stdin.readline()
            if input == "":
                # Nothing to read in, send the data to the starship
                json_lines = json.dumps(read_lines)
                self.update_sensors(json_lines)
            else:
                # Still stuff to read, so add it to the lines
                read_lines += input
