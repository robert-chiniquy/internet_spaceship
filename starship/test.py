import random
import spaceship


def random_position():
    x = random.randrange(-100, 100, 1)
    y = random.randrange(-100, 100, 1)
    return x, y


def random_fake_input():
    pass


def test(ship):
    ship.update_sensors({
        'position': [0, 0],
        'velocity': 1
    })
    ship.update_sensors({
        'position': [1, 1],
        'velocity': 1
    })


if __name__ == '__main__':
    ship = spaceship.Spaceship(random_position())
    test(ship)
