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

    def configure_servo(self, board):
        """
        Configure servo engine for provided board
        """
        self.servo = board.get_pin(f"d:{self.pin}:p")
        board.servo_config(
            pin       = self.pin,
            min_pulse = 544,
            max_pulse = 2400,
            angle     = 0
        )

    def set_angle(self, angle):
        # print(" >>>>> {}    : {}".format(angle, self.servo))
        self.servo.write(angle)

    # @property
    def min_max_speed(self, invert: bool):
        # if self.inverted:
        #     return self._full_stop, self._full_backward
        # return self._full_stop, self._full_forward

        # TODO: This is stupid
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

        # print(f" resulting speed: {resulting_speed}")
        # print(f" available speed: {available_speed}")

        total = len(available_speed) - 1

        # print(f" total: {total}")

        if total < 1:
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

    def __init__(self, left_wheels: list, right_wheels: list, port: str="/dev/tty.usbmodem14101"):
        # self._board        = None
        self._board        = pyfirmata.Arduino(port)
        self._left_wheels  = {}
        self._right_wheels = {}
        self._current_angle = {}   # Keeping current wheel settings

        # Wheels are stored in dictionary:
        #    wheel object : desired rotation angle / speed
        # TODO: decide which one to use

        # self._board.servo_config(
        #     pin=9,
        #     min_pulse=544,
        #     max_pulse=2400,
        #     angle=0
        # )
        # self.a = self._board.get_pin("d:9:p")

        for left_wheel in left_wheels:
            self._left_wheels[left_wheel] = 0
            left_wheel.configure_servo(board=self._board)

        for right_wheel in right_wheels:
            self.right_wheels[right_wheel] = 0
            right_wheel.configure_servo(board=self._board)

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

    @property
    def current_angle(self):
        return self._current_angle

    def print_firmata_status(self):
        """
        Output Firmata board status
        """
        print(f"pyFirmata version:     {pyfirmata.__version__}")
        print(f"Hardware:              {self.board.__str__()}")
        # print(f"Firmata firmware name: {self.board.get_firmware()}")
        print( "Firmata firmware:      {major}.{minor}".format(
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
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.left_wheels[left_wheel] = speed - extra
        for right_wheel, speed in self.right_wheels.items():
            extra = 1.0
            # if speed > 0:
            #     extra = 0.5
            self.right_wheels[right_wheel] = speed + extra

    def right(self):
        for left_wheel, speed in self.left_wheels.items():
            extra = 1.0
            # if speed > 0:
            #     extra = 0.5
            self.left_wheels[left_wheel] = speed + extra
        for right_wheel, speed in self.right_wheels.items():
            extra = 1.0
            if speed > 0:
                extra = 0.5
            self.right_wheels[right_wheel] = speed - extra

    @staticmethod
    def _normalize_speed(speed):
        if speed > 0:
            # print(" {} = {} / {}".format(speed, abs(speed), ceil(speed)))
            speed = abs(speed) / ceil(speed)
            # print("           = {}".format(speed))
        elif speed < 0:
            # print(" {} = {} / {}".format(speed, abs(speed), floor(speed)))
            speed = abs(speed) / floor(speed)
            # print("           = {}".format(speed))
        return speed

    def need_changes(self, wheel, angle):
        """
        Check if wheel need to change its angle position
        """
        # if wheel not in self.current_angle:
        #     self.current_angle[wheel] = angle
        #     return True
        #
        # if self.current_angle[wheel] != angle:
        #     self.current_angle[wheel] = angle
        #     return True

        if self.current_angle.get(wheel) == angle:
            return False

        self.current_angle[wheel] = angle
        return True

    def execute(self):
        for left_wheel, speed in self.left_wheels.items():
            speed = self._normalize_speed(speed)
            angle = left_wheel.get_rotation_for_speed(speed)
            # if angle != 93:
            #     print(f" l --- SPEED: {speed} | {angle} ({self.left_wheels[left_wheel]})")
            if self.need_changes(left_wheel, angle):
                # print(" --- L: need changes")
                print(f" --- L: need changes: {speed} | {angle} ({self.left_wheels[left_wheel]})")
                left_wheel.set_angle(angle)

            # drop speed
            self.left_wheels[left_wheel] = 0

        for right_wheel, speed in self.right_wheels.items():
            speed = self._normalize_speed(speed)
            angle = right_wheel.get_rotation_for_speed(speed)
            # if angle != 93:
            #     print(f" r --- SPEED: {speed} | {angle} ({self.left_wheels[left_wheel]})")
            if self.need_changes(right_wheel, angle):
                print(f" --- R: need changes: {speed} | {angle} ({self.left_wheels[left_wheel]})")
                right_wheel.set_angle(angle)

            # drop speed
            self.right_wheels[right_wheel] = 0

        sleep(0.1)