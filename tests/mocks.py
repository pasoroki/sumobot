from modules.arduino import SumoBot, BotWheel


class FakeServo:
    """
    Fake servo module to control servo settings done by Wheel
    """
    _angle = None

    def __init__(self, angle=None):
        if angle is not None:
            self.angle = angle

    def set_angle(self, value):
        self.angle = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value


def generate_robot(left_wheels: list, right_wheels: list):
    # with patch('pyfirmata') as pyfirmata:
    bot = SumoBot(left_wheels=left_wheels, right_wheels=right_wheels)
    return bot


def generate_wheel(angle: int or None=None, inverted: bool=False):
    wheel = BotWheel(inverted=inverted)
    wheel.servo = FakeServo(angle=angle)
    return wheel


def get_fake_robot(left_wheels: list=[], right_wheels: list=[]):
    """
    Generate robot using list of wheels
    each value in list correspond to initial servo angles
    """
    _left_wheels = []
    for wheel_angle in left_wheels:
        _left_wheels.append(generate_wheel(wheel_angle, inverted=True))

    _right_wheels = []
    for right_angle in right_wheels:
        _right_wheels.append(generate_wheel(right_angle, inverted=False))

    bot = generate_robot(
        left_wheels  = _left_wheels,
        right_wheels = _right_wheels
    )
    return bot
