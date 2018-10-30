from modules.arduino import BotWheel
import pytest


class TestBotWheel:
    def setup_class(self):
        print("setup class")

    def test_one(self):
        print("ONE")
