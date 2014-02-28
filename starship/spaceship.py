import base


class Spaceship(base.BaseSpaceship):
    def input(self):
        print "input!"
        print "velocity", self.velocity
        print "position", self.x, self.y
        print "throttle", self.throttle,
        print "heading", self.heading
