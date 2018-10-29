import zorg
import time
from threading import Thread, Event
from modules.controls import keyboard_reader, getch
from sys import stdin
import pygame, sys
# from pygame.locals import *
from pygame.locals import QUIT, KEYDOWN, KEYUP

# pygame.init()
# BLACK  = (0, 0, 0)
# WIDTH  = 100
# HEIGHT = 100
# windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
# windowSurface.fill(BLACK)
# x = 0

stop = Event()
# data = []
thread = None
# fd = stdin.fileno()
fd = stdin



# while True:
#       print("EVENT: {}".format(event))

def init():
    pygame.init()
    BLACK = (0, 0, 0)
    WIDTH = 100
    HEIGHT = 100
    windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    windowSurface.fill(BLACK)
    x = 0


def get_state():
    global stop
    init()
    state = {}
    # state = {
    #     "left":  0,
    #     "right": 0,
    #     "up":    0,
    #     "down":  0
    # }
    # print(event.key)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            stop.set()

        if event.type == KEYDOWN:
             key = event.key
             # print(key)
             # if key == pygame.K_UP:
             #     state["up"] = 1
             #
             # if key == pygame.K_DOWN:
             #     state["down"] = 1
             #
             # if key == pygame.K_LEFT:
             #     state["left"] = 1
             #
             # if key == pygame.K_RIGHT:
             #     state["right"] = 1

             state[key] = 1

    return state



# while not stop.is_set():
#     # print(f"\n - content: {data}")
#     # print("a")
#     time.sleep(0.5)
#     if data:
#         action = data.pop(0)
#         print("\r" + " ".join(data))



def mypprint(obj):
    for i in dir(obj):
        if i.startswith("_"): continue
        print(" - {:20} : {}".format(i, getattr(obj, i)))


def work(my):
    print("WORK")
    global stop
    # global thread
    # thread.start()
    angle = 0
    while not stop.is_set():
        time.sleep(0.1)
        data = get_state()
        if data:
            for action in data.keys():
                # action = data.pop(0)
                # print("\r" + " ".join(data))
                print(" --> {}".format(action))
                if action == "q":
                    print("STOP!!!!")
                    stop.set()

                elif action in ("up", 273, pygame.K_UP):
                    print(" UP ")
                    # my.left_servo.set_angle(150)
                    angle += 1
                    my.left_servo.set_angle(angle)

                elif action in ("down", 274, pygame.K_DOWN):
                    print(" DOWN ")
                    angle -= 1
                    # my.left_servo.set_angle(-150)
                    my.left_servo.set_angle(angle)

                elif action in ("left", 276, pygame.K_LEFT):
                    print(" LEFT ")
                    angle -= 10
                    # my.left_servo.set_angle(-150)
                    my.left_servo.set_angle(angle)

                elif action in ("right", 275, pygame.K_RIGHT):
                    print(" RIGHT ")
                    angle += 10
                    # my.left_servo.set_angle(-150)
                    my.left_servo.set_angle(angle)

                elif action in (32, pygame.K_SPACE):
                    print(" SPACE ")
                    angle = 0
                    # my.left_servo.set_angle(0)
                    my.left_servo.set_angle(angle)

                else:
                    print(" ELSE ")
                    angle = 0
                    # my.left_servo.set_angle(0)
                    my.left_servo.set_angle(angle)


        print("ANGLE = {}".format(my.left_servo.get_angle()))

    my.left_servo.set_angle(0)





        # while True:
    #
    #     print("1")
    #     # Move the servo to 20 degrees
    #     print(my)
    #     mypprint(my)
    #
    #     print("\n\n LEFT SERVO:")
    #     # mypprint(my.left_servo)
    #
    #     print("\n\n\n-----------\n\n\n")
    #
    #
    #     my.left_servo.set_angle(20)
    #
    #     print("2")
    #     print("Servo angle set to", my.left_servo.get_angle())
    #
    #     # Wait 1 seconds before doing it again
    #     time.sleep(1)
    #
    #     # Move the servo to 100 degrees
    #     my.left_servo.set_angle(100)
    #
    #     print("Servo angle set to", my.left_servo.get_angle())
    #
    #     # Wait 1 seconds before doing it again
    #     time.sleep(1)

robot = zorg.robot({
    "connections": {
        "ArduinoLeonardo": {
            "adaptor": "zorg_firmata.Firmata",
            # "port": "/dev/ttyACM0",
            "port": "/dev/tty.usbmodem14101",
        },
    },
    "devices": {
        "left_servo": {
            "connection": "ArduinoLeonardo",
            "driver":     "zorg_grove.Servo",
            "port_id":       "/dev/tty.usbmodem14101",
            "pin":        9,  # 9 is a pwm pin
        },
        # "right_servo": {
        #     "connection": "ArduinoLeonardo",
        #     "driver":     "zorg_grove.Servo",
        #     "pin":        10,  # 10 is a pwm pin
        # }
    },
    "name": "Servo Robot", # Give your robot a unique name
    "work": work, # The method where the work will be done
})

# thread = Thread(target=keyboard_reader, args=(data, stop, fd))
# thread.start()
print(" --> next")
robot.start()
