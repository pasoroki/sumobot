import pyfirmata
import logging
from math import ceil


LOG = logging.getLogger("arduino")


class BotWheel:
    """
    Class with SumoBot settings (Wheels)
    """
    _speed_limit = 0

    def __init__(self, pin: int=9, speed_limit: float=1.0, inverted: bool=False):
        self._pin        = pin
        self.speed_limit = speed_limit
        self._inverted   = inverted
        self._servo      = None    # Actual servo engine

        self._full_backward = 85
        self._full_stop     = 93    # No rotation
        self._full_forward  = 110

    @property
    def pin(self):
        return self._pin

    @property
    def speed_limit(self):
        return self._speed_limit

    @speed_limit.setter
    def speed_limit(self, speed_limit: float=1.0):
        if speed_limit < 0.0 or speed_limit > 1.0:
            raise ValueError(f"Speed must be between 0.0 and 1.0 ({speed_limit:.2f} provided)")
        self._speed_limit = speed_limit

    @property
    def servo(self):
        return self._servo

    @servo.setter
    def servo(self, new_servo):
        self._servo = new_servo

    @property
    def inverted(self):
        return self._inverted

    @property
    def stop(self):
        return self._full_stop

    @property
    def min_max_speed(self):
        # if self.inverted:
        #     return self._full_stop, self._full_backward
        # return self._full_stop, self._full_forward
        if self.inverted:
            data = range(self._full_stop, self._full_backward+2)     # one extra number because we round up too high
        else:
            data = range(self._full_stop, self._full_forward-2, -1)  # one extra number because we round up too high
        return list(data)

    def get_rotation_for_speed(self, speed: float=1.0):
        """
        Get rotation ID for desired speed
        The provided speed parameter also affected by global wheel speed limit
        (!) NOTE:
                 If you want full speed, make sure you run
        :param speed:
        :return:
        """
        resulting_speed = self.speed_limit * speed
        available_speed = self.min_max_speed

        total = len(available_speed) - 1

        if len(total) < 1:
            raise RuntimeError("For given speed settings (global:{} | requested:{}) no possible rotation is found".format(
                self.speed_limit,
                speed
            ))
        one_percent = total / 100

        return available_speed[ceil(resulting_speed * one_percent)]


# my.left_servo.set_angle(0)

class SumoBot:
    """
    Module to control the SumoBot
    """
    _board = None

    def __init__(self, left_wheels: BotWheel, right_wheels: BotWheel, port: str="/dev/tty.usbmodem14101"):
        self._board        = pyfirmata.Arduino(port)
        self._left_wheels  = {}
        self._right_wheels = {}

        # Wheels are stored in dictionary:
        #    wheel object : desired rotation angle / speed
        # TODO: decide which one to use

        for left_wheel in left_wheels:
            self._left_wheels[left_wheel] = 0
        for right_wheel in right_wheels:
            self.right_wheels[right_wheel] = 0

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Disconnect from arduino
        """
        print("---- EXIT BOT ----")
        self.board.exit()

    @property
    def board(self):
        return self._board

    @property
    def left_wheels(self):
        return self._left_wheels

    @property
    def right_wheels(self):
        return self._right_wheels

    def print_firmata_status(self):
        """
        Output Firmata board status
        """
        print(f"pyFirmata version:     {pyfirmata.__version__}")
        print(f"Hardware:              {self.board.__str__()}")
        print(f"Firmata firmware name: {self.board.get_firmware()}")
        print( "Firmata firmware:      {major}.{minor}".format(
            major = self.board.get_firmata_version()[0],
            minor = self.board.get_firmata_version()[1]
        ))

    def stop(self):
        pass

    def forward(self):
        for left_wheel, speed in self.left_wheels.items():
            self.left_wheels[left_wheel] = speed + 1.0
        for right_wheel, speed in self.right_wheels.items():
            self.right_wheels[right_wheel] = speed + 1.0

    def backward(self):
        for left_wheel, speed in self.left_wheels.items():
            self.left_wheels[left_wheel] = speed - 1.0
        for right_wheel, speed in self.right_wheels.items():
            self.right_wheels[right_wheel] = speed - 1.0

    def left(self):
        for left_wheel, speed in self.left_wheels.items():
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.left_wheels[left_wheel] = speed - extra
        for right_wheel, speed in self.right_wheels.items():
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.right_wheels[right_wheel] = speed + extra

    def right(self):
        for left_wheel, speed in self.left_wheels.items():
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.left_wheels[left_wheel] = speed + extra
        for right_wheel, speed in self.right_wheels.items():
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.right_wheels[right_wheel] = speed - extra

    def execute(self):
        for left_wheel, speed in self.left_wheels.items():
            left_wheel.servo.set_angle(speed)
        for right_wheel, speed in self.right_wheels.items():
            right_wheel.servo.set_angle(speed)
