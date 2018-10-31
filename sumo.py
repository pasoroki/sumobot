import time
from threading import Event
from modules.joystick import Joystick
from modules.arduino import SumoBot, BotWheel
import pygame
import logging


LOG = logging.getLogger(__name__)
stop = Event()

left_wheel_front = BotWheel(
    pin         = 5,
    speed_limit = 1,
    inverted    = False
)
left_wheel_back = BotWheel(
    pin         = 10,
    speed_limit = 1,
    inverted    = False
)

right_wheel_front = BotWheel(
    pin         = 6,
    speed_limit = 1,
    inverted    = True
)
right_wheel_back = BotWheel(
    pin         = 9,
    speed_limit = 1,
    inverted    = True
)


bot = SumoBot(
    left_wheels  = [left_wheel_front, left_wheel_back],
    right_wheels = [right_wheel_front, right_wheel_back],
    port = "/dev/tty.usbmodem14101",
)
bot.print_firmata_status()

joystick = Joystick(stop=stop, width=100, height=100)


# print("Prepare the robot!")
# bot.stop()
# bot.execute()

print("Ready to serve")
while not stop.is_set():
    # time.sleep(0.1)
    # data = joystick.get_buttons_state()
    data = joystick.get_buttons_state
    # data = joystick.state
    if data:
        for action in data.keys():
            if action == "q":
                print("STOP!!!!")
                stop.set()

            elif action in ("up", 273, pygame.K_UP):
                print(" UP ")
                bot.forward()

            elif action in ("down", 274, pygame.K_DOWN):
                print(" DOWN ")
                bot.backward()

            elif action in ("left", 276, pygame.K_LEFT):
                print(" LEFT ")
                bot.left()

            elif action in ("right", 275, pygame.K_RIGHT):
                print(" RIGHT ")
                bot.right()

            elif action in (32, pygame.K_SPACE):
                print(" SPACE ")
                bot.stop()

            else:
                print(f" {action} ")
    else:
        bot.stop()

    bot.execute()
    time.sleep(0.05)

bot.stop()
# board.exit()
