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

    def test_move_forward_right__stopped__right_wheels_should_slow_down(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.forward()
        bot.right()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == 2, "Left wheel speeds should be at full speed"
        for speed in bot.right_wheels.values():
            assert speed == 0.5, "Right wheel speeds should be at half speed"

    def test_move_forward_left__stopped__left_wheels_should_slow_down(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.forward()
        bot.left()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == 0.5, "Left wheel speeds should be at half speed"
        for speed in bot.right_wheels.values():
            assert speed == 2, "Right wheel speeds should be at full speed"


    def test_move_backward_right__stopped__right_wheels_should_slow_down(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.backward()
        bot.right()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == -2, "Left wheel speeds should be at full speed"
        for speed in bot.right_wheels.values():
            assert speed == -0.5, "Right wheel speeds should be at half speed"

    def test_move_backward_left__stopped__left_wheels_should_slow_down(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.backward()
        bot.left()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == -0.5, "Left wheel speeds should be at half speed"
        for speed in bot.right_wheels.values():
            assert speed == -2, "Right wheel speeds should be at full speed"

    def test_rotate_left__stopped__wheels_must_go_sideways(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.left()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == -1, "Left wheel speeds should go back"
        for speed in bot.right_wheels.values():
            assert speed == 1, "Right wheel speeds should go forward"

    def test_rotate_right__stopped__wheels_must_go_sideways(self):
        bot = get_fake_robot(
            left_wheels=[120],
            right_wheels=[30]
        )
        bot.right()
        bot.execute()

        for speed in bot.left_wheels.values():
            assert speed == 1, "Left wheel speeds should go forward"
        for speed in bot.right_wheels.values():
            assert speed == -1, "Right wheel speeds should go back"



