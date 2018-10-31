import pyfirmata
import logging
from math import ceil, floor
from time import sleep


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

        # Check those values with current servo motor
        self._full_backward = 85
        self._full_stop     = 93    # No rotation
        self._full_forward  = 100

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

    def configure_servo(self, board):
        """
        Configure servo engine for provided board
        """
        self.servo = board.get_pin(f"d:{self.pin}:p")
        board.servo_config(
            pin       = self.pin,
            min_pulse = 544,
            max_pulse = 2400,
            angle     = 93
        )

    def set_angle(self, angle):
        self.servo.write(angle)

    def min_max_speed(self, invert: bool=False) -> list:
        """
        Get list of available rotation angles from stop to maximum speed
        This code makes sure to return max speed depending on internal `inverted` flag
        NOTE:
            the `invert` flag will invert the internal `inverted` flag
            this is necessary when we are moving backwards
        """

        # TODO: This looks weird, better find a nicer way to get backwards moving speed
        invert = self.inverted if not invert else not self.inverted

        if invert:
            data = range(self._full_stop, self._full_backward-2, -1)     # one extra number because we round up too high
        else:
            data = range(self._full_stop, self._full_forward+2)  # one extra number because we round up too high

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
        resulting_speed = abs(self.speed_limit * speed * 100)
        available_speed = self.min_max_speed(invert=speed < 0)
        total = len(available_speed) - 1

        if total < 1:
            raise RuntimeError("For given speed settings (global:{} | requested:{}) no possible rotation is found".format(
                self.speed_limit,
                speed
            ))
        one_percent = total / 100

        return available_speed[ceil(resulting_speed * one_percent)]


class SumoBot:
    """
    Module to control the SumoBot
    """
    _board = None

    def __init__(self, left_wheels: list, right_wheels: list, port: str="/dev/tty.usbmodem14101"):
        self._board        = pyfirmata.Arduino(port)

        # Wheels are stored in dictionary:
        #    wheel object : desired rotation speed
        self._left_wheels  = {}
        self._right_wheels = {}

        # The actual speed is stored in `current_angle` dictionary
        # This is to avoid duplicated servo config changes
        self._current_angle = {}

        # TODO: decide which one to use

        for left_wheel in left_wheels:
            self._left_wheels[left_wheel] = 0
            left_wheel.configure_servo(board=self._board)

        for right_wheel in right_wheels:
            self.right_wheels[right_wheel] = 0
            right_wheel.configure_servo(board=self._board)

    def __del__(self):
        if self.board:
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

    @property
    def current_angle(self):
        return self._current_angle

    def print_firmata_status(self):
        """
        Output Firmata board status
        """
        print(f"pyFirmata version: {pyfirmata.__version__}")
        print(f"Hardware:          {self.board.__str__()}")
        print( "Firmata firmware:  {major}.{minor}".format(
            major = self.board.get_firmata_version()[0],
            minor = self.board.get_firmata_version()[1]
        ))

    def stop(self):
        for left_wheel, speed in self.left_wheels.items():
            self.left_wheels[left_wheel] = 0
        for right_wheel, speed in self.right_wheels.items():
            self.right_wheels[right_wheel] = 0

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
            extra = -1.0

            if speed > 0:
                extra = -0.7

            elif speed < 0:
                extra = 0.7
            self.left_wheels[left_wheel] = speed + extra

        for right_wheel, speed in self.right_wheels.items():
            extra = 1.0

            if speed > 0:
                extra = 1.0

            elif speed < 0:
                extra = -1
            self.right_wheels[right_wheel] = speed + extra

    def right(self):
        for left_wheel, speed in self.left_wheels.items():
            extra = 1.0

            if speed > 0:
                extra = 1.0

            elif speed < 0:
                extra = -1.0
            self.left_wheels[left_wheel] = speed + extra

        for right_wheel, speed in self.right_wheels.items():
            extra = -1.0

            if speed > 0:
                extra = -0.7

            elif speed < 0:
                extra = 0.7
            self.right_wheels[right_wheel] = speed + extra

    @staticmethod
    def _normalize_speed(speed):
        if speed > 0:
            speed = abs(speed) / ceil(speed)
        elif speed < 0:
            speed = abs(speed) / floor(speed)
        return speed

    def need_changes(self, wheel, angle):
        """
        Check if wheel need to change its angle position
        """
        if self.current_angle.get(wheel) == angle:
            return False

        self.current_angle[wheel] = angle
        return True

    def execute(self):
        result = ""

        i = 0
        for left_wheel, speed in self.left_wheels.items():
            i += 1
            speed = self._normalize_speed(speed)
            angle = left_wheel.get_rotation_for_speed(speed)
            if angle != 93:
                result += f"{i}: {speed:.2f} | {angle}    | "
            if self.need_changes(left_wheel, angle):
                left_wheel.set_angle(angle)

            # drop speed
            self.left_wheels[left_wheel] = 0

        for right_wheel, speed in self.right_wheels.items():
            i += 1
            speed = self._normalize_speed(speed)
            angle = right_wheel.get_rotation_for_speed(speed)
            if angle != 93:
                result += f"{i}: {speed:.2f} | {angle}    | "
            if self.need_changes(right_wheel, angle):
                right_wheel.set_angle(angle)

            # drop speed
            self.right_wheels[right_wheel] = 0

        if result:
            print(result)
        sleep(0.1)