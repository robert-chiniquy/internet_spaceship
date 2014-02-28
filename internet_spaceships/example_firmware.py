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
        # Turn 45 degrees every turn
        if self.heading + 45 > 359:
            self.heading -= 314
        else:
            self.heading += 45

    def fire_on_closest_ship(self):
        """ Look for the closest ship and shoot at them
        """
        for ship in self.scanners:
            if ship['type'] == 'ship' and \
                    ship['distance'] <= self.weapon_range:
                self.fire_on(ship['id'])

    def mine_asteroid_if_close(self):
        """ If we're within mining distance of an asteroid, mine it. Mine
        all the dogecoin. Returns True if we start mining, False if we aren't
        mining.
        """
        for asteroid in self.scanners:
            if asteroid['type'] == 'asteroid' and \
                    asteroid['position'] <= 2:
                self.throttle = 0
                self.mine(asteroid['id'])
                return True
        return False
