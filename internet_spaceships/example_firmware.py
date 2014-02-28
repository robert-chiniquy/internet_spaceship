from internet_spaceships import base


class Firmware(base.BaseFirmware):
    def input(self):
        """ Go in circles, look for asteroids. Obtain doge.
        """
        # Try and find an asteroid
        for asteroid in self.objects.get('asteroids'):
            if self._distance(asteroid['position'] <= 2):
                self.throttle = 0
                self.mine(asteroid['id'])
                return
        # No asteroid? Go fast!
        self.throttle = 100
        # Turn 45 degrees every turn
        if self.heading + 45 > 359:
            self.heading -= 314
        else:
            self.heading += 45
