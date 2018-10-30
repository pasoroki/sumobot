from modules.arduino import BotWheel
import pytest
from tests.mocks import FakeServo


STOP = 93


class TestBotWheel:
    """
    Make sure wheel correctly responses on movement requests
    """
    def setup_class(self):
        print("setup class")

    def test_one(self):
        print("ONE")

    def test_stop__stopped__correct_response(self):
        wheel = BotWheel(inverted=False)
        # wheel.servo = FakeServo(0)

        # wheel.stop()
        assert wheel.stop == STOP, "In stopped state servo must have value 93"
