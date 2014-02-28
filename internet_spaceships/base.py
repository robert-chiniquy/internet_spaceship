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
        # Set these with their matching properties. e.g. self.throttle = 100
        # throttle can be 0 to 100
        self._throttle = 0
        # heading can be 0 ('north') through 359, going clockwise
        self._heading = 0

        # You shouldn't change these. It won't affect anything. They get
        # updated each time you get an input.

        # Attributes
        self.doge = 0
        self.x, self.y = initial_position
        self.velocity = 0
        self.shields = 100

        self.shields_level = 1
        self.shield_recharge = 1

        self.weapons_level = 1
        self.weapon_power = 10

        self.armor_level = 1
        self.armor = 100

        self.thrusters_level = 1
        self.thrusters = 10

        # Actions
        self.fire_on = None
        self.mine_target = None
        self.upgrade_system = None

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

    def fire(self, target_id):
        """ Attempt to fire at the target.
        """
        self.fire_on = target_id

    # def upgrade(self, system):
    #     """ Upgrade one of your systems to the next level (if possible).
    #     system can be 'shields', 'weapons', 'armor' or 'thrusters'.
    #     """
    #     if system not in ['shields', 'weapons', 'armor', 'thrusters']:
    #         raise ValueError("System must be one of 'shields', 'weapons', "
    #                          "'armor' or 'thrusters'.")
    #
    #     self.upgrade_system = system

    def mine(self, asteroid_id):
        """ Attempt to mine an asteroid. You must be within 1 unit of the
        asteroid.
        """
        self.mine = asteroid_id

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
        # Reset
        self.fire_on = None
        self.mine_target = None
        self.upgrade_system = None

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
