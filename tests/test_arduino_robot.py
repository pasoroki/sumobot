from modules.arduino import SumoBot, BotWheel
import pytest
from tests.mocks import FakeServo, get_fake_robot
from unittest.mock            import MagicMock, patch


STOP     = 0
FORWARD  = 1
BACKWARD = 1


class TestSumoBot:
    """
    Make sure wheel correctly responses on movement requests
    """
    def setup_class(self):
        # print("setup class")
        pass

    def test_stop_bot__stopped__all_wheels_are_stopped(self):
        bot = get_fake_robot(
            left_wheels=[10],
            right_wheels=[-10]
        )
        bot.stop()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == 0, "Left wheel speeds should be 0 during stop"
        for speed in bot.right_wheels.values():
            assert speed == 0, "Right wheel speeds should be 0 during stop"

        # print("---- {}".format(bot))
        # for wheel in left_wheels:
        #     print(wheel.servo)
        #     assert wheel.servo.angle == STOP
        # for wheel in right_wheels:
        #     assert wheel.servo.angle == STOP

    def test_move_forward__stopped__all_wheels_are_full_speed(self):
        bot = get_fake_robot(
            left_wheels=[10],
            right_wheels=[-10]
        )
        bot.forward()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == 1, "Left wheel speeds should be at full speed"
        for speed in bot.right_wheels.values():
            assert speed == 1, "Right wheel speeds should be at full speed"