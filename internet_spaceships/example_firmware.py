import logging
from internet_spaceships import base


class Firmware(base.BaseFirmware):
    def input(self):
        """ Go in circles, look for asteroids. Obtain doge.
        """

        # Offense!
        self.fire_on_closest_ship()

        # Try and find an asteroid, mine and quit if we can. Otherwise,
        # fly in circles
        mining = self.mine_asteroid_if_close()
        if mining:
            # Don't fly away from the asteroid
            return

        # No asteroid? Go fast in circles!
        self.throttle = 100
        logging.debug("Current throttle: {}".format(self.throttle))
        # Turn 1 degree every tick
        if self.heading + 1 > 359:
            self.heading = 0
        else:
            self.heading += 1
        logging.debug("Current heading: {}".format(self.heading))

    def fire_on_closest_ship(self):
        """ Look for the closest ship and shoot at them
        """
        for ship in self.get_ships():
            if ship['distance'] <= self.weapon_range:
                self.fire_on(ship['id'])
                logging.debug("Shot at {}".format(ship['id']))

    def mine_asteroid_if_close(self):
        """ If we're within mining distance of an asteroid, mine it. Mine
        all the dogecoin. Returns True if we start mining, False if we aren't
        mining.
        """
        for asteroid in self.get_asteroids():
            if asteroid['distance'] <= 2:
                self.throttle = 0
                self.mine(asteroid['id'])
                logging.debug("Mining {}".format(asteroid['id']))
                return True
        logging.debug("Nothing close enough to mine")
        return False


if __name__ == "__main__":
    """ This sets up your firmware when you run "firmware.py" with some JSON
    input.
    """
    firmware = Firmware()
    firmware.start()
