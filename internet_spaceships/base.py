import json
import logging
import sys
import math


class BaseFirmware(object):

    def __init__(self):
        """ initial_position is a tuple in the form (x,y)
        """
        # Set these with their matching properties. e.g. self.throttle = 100
        # throttle can be 0 to 100
        self._throttle = 0
        # heading can be 0 ('north') through 359, going clockwise
        self._heading = 0

        # You shouldn't change these. It won't affect anything. They get
        # updated each time you get an input.

        # Actions
        self.fire_on = None
        self.mine_target = None
        self.upgrade_system = None

        # Attributes
        self.doge = 0
        self.position = [0, 0]
        self.speed = 0
        self.shields = 100

        # Don't blow your engine! This is unbounded, so it can go over 9000.
        self.engineTemperature = 0

        # Unused power
        self.power = 0

        self.shields_level = 1
        self.shield_recharge = 1

        self.weapons_level = 1
        self.weapon_power = 10
        self.weapon_range = 50

        self.armor_level = 1
        self.armor = 100

        self.thrusters_level = 1
        self.thrusters = 10

        # Represents what happens in the game, e.g. getting hit or shooting
        # another ship.
        self.log = []

        # Represents every ship/body/asteroid detected
        self.scanners = []

        # Erase old log file and set up a logger so we can debug
        open('debug.log', 'w')
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

    def input(self):
        """ This function will be called every time data is sent to the
        spaceship by the game. You must implement this in firmware.py if you
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
        # See if the target is a ship. Can't fire on bodies/asteroids
        for ship in self.scanners:
            if ship['type'] == 'ship' and ship['id'] == target_id:
                if ship['type'] == 'ship':
                    self.fire_on = target_id
                else:
                    raise ValueError("Fire target id {} is not a ship, "
                                     "is {}.".format(target_id, ship['type']))
        raise ValueError("Could not find target_id {}".format(target_id))

    def mine(self, asteroid_id):
        """ Attempt to mine an asteroid. You must be within 1 unit of the
        asteroid.
        """
        # See if the asteroid is nearby
        for asteroid in self.get_asteroids():
            print asteroid
            if asteroid['id'] == asteroid_id:
                if asteroid['distance'] <= 2:
                    self.mine_target = asteroid_id
                    return
                else:
                    raise ValueError("Asteroid {} is too far away, "
                                     "is {} units away.".format(
                                     asteroid_id,
                                     asteroid['distance']))
        raise ValueError("Could not find target_id {}".format(asteroid_id))

    def get_asteroids(self):
        asteroids = []
        for asteroid in self.scanners:
            if asteroid['type'] == 'asteroid':
                asteroids.append(asteroid)
        return asteroids

    def get_ships(self):
        ships = []
        for ship in self.scanners:
            if ship['type'] == 'ship':
                ships.append(ship)
        return ships

    def get_planets(self):
        planets = []
        for planet in self.scanners:
            if planet['type'] == 'planet':
                planets.append(planet)
        return planets

    # Utility functions you probably don't want to modify

    def output(self):
        """ Return the current output state
        """
        return {
            'position': self.position,
            'throttle': self.throttle,
            'heading': self._heading,
            'fire_on': self.fire_on,
            'mine_target': self.mine_target,
            'upgrade_system': self.upgrade_system
        }

    def write_output(self, output_data):
        """ Send data back to the server via stdout
        """
        # Send data to the stdout
        print json.dumps(output_data)

    def update_sensors(self, json_lines):
        """ Take the sensor data and update our sensors, then call your
        firmware input.
        """
        # Reset
        self.fire_on = None
        self.mine_target = None
        self.upgrade_system = None

        # Save all the data
        for key, val in json_lines.items():
            setattr(self, key, val)

    def start(self):
        """
        This is the reading function
        """
        if not 1 < len(sys.argv) <= 3:
            raise ValueError("firmware takes exactly 1 argument, the input "
                             "JSON.")
        try:
            input_data = json.loads(sys.argv[1])
        except ValueError:
            raise ValueError("Input JSON couldn't be decoded. Weird.")
        output_data = []
        for tick in input_data:
            self.update_sensors(tick)
            self.input()
            # Save the output data to a list we print out at the end.
            output_data.append(self.output())
        self.write_output(output_data)

    def _distance(self, position):
        """ Cartesian distance to position
        """
        return math.sqrt((position[0] - self.position[0])**2 +
                         (position[1] - self.position[1])**2)
