# import zorg
import time
from threading import Thread, Event
# from modules.controls import keyboard_reader, getch
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

# robot = zorg.robot({
#     "connections": {
#         "ArduinoLeonardo": {
#             "adaptor": "zorg_firmata.Firmata",
#             # "port": "/dev/ttyACM0",
#             "port": "/dev/tty.usbmodem14101",
#         },
#     },
#     "devices": {
#         "left_servo": {
#             "connection": "ArduinoLeonardo",
#             "driver":     "zorg_grove.Servo",
#             "port_id":       "/dev/tty.usbmodem14101",
#             "pin":        9,  # 9 is a pwm pin
#         },
#         # "right_servo": {
#         #     "connection": "ArduinoLeonardo",
#         #     "driver":     "zorg_grove.Servo",
#         #     "pin":        10,  # 10 is a pwm pin
#         # }
#     },
#     "name": "Servo Robot", # Give your robot a unique name
#     "work": work, # The method where the work will be done
# })

# thread = Thread(target=keyboard_reader, args=(data, stop, fd))
# thread.start()
print(" --> next")
# robot.start()

import pyfirmata
PORT = "/dev/tty.usbmodem14101"
board = pyfirmata.Arduino(PORT)

PIN = 9 # Pin 12 is used
DELAY = 2 # A 2 seconds delay

# print("pyFirmata version:\t%s" % pyfirmata.__version__)
# print("Hardware:\t\t%s" % board.__str__())
# #print "Firmata firmware name:  %s" % board.get_firmware()
# print("Firmata firmware:\t%i.%i" % \
#     (board.get_firmata_version()[0], board.get_firmata_version()[1]))

stop = Event()

# print("ON")
# board.digital[PIN].write(1) # Set the LED pin to 1 (HIGH)
# board.pass_time(DELAY)
# print("OFF")
# board.digital[PIN].write(0) # Set the LED pin to 0 (LOW)
# board.pass_time(DELAY)

print("WORK")


# Definition of the pin, one with PWM, marked as ~XX on the Arduino
digital_0 = board.get_pin('d:9:p')
print(" --> PIN: {}".format(digital_0))

board.servo_config(pin=9, min_pulse=544, max_pulse=2400, angle=0)

# # Time (approx. seconds) to get to the maximum/minimum
# DURATION = 5
# # Numbers of steps to get to the maximum/minimum
# STEPS = 10
#
# # Waiting time between the
# wait_time = DURATION/float(STEPS)
#
# # Note: Value range for PWM is 0.0 till 1.0
#
# # Up
# for i in range(1, STEPS + 1):
#     value = i/float(STEPS)
#     digital_0.write(value)
#     board.pass_time(wait_time)
#
# # Down
# increment = 1/float(STEPS)
# while STEPS > 0:
#     value = increment * STEPS
#     digital_0.write(value)
#     board.pass_time(wait_time)
#     STEPS = STEPS - 1
#
# board.exit()
# exit()

# global stop
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
                angle = 110

            elif action in ("down", 274, pygame.K_DOWN):
                print(" DOWN ")
                angle -= 1
                angle = 50
                # my.left_servo.set_angle(-150)

            elif action in ("left", 276, pygame.K_LEFT):
                print(" LEFT ")
                angle -= 1
                # my.left_servo.set_angle(-150)

            elif action in ("right", 275, pygame.K_RIGHT):
                print(" RIGHT ")
                angle += 1
                # my.left_servo.set_angle(-150)

            elif action in (32, pygame.K_SPACE):
                print(" SPACE ")
                angle = 93
                # my.left_servo.set_angle(0)

            else:
                print(" ELSE ")
                angle = 0
                # my.left_servo.set_angle(0)

        print(" -> {}".format(angle))
        digital_0.write(angle)
        # board.pass_time(DELAY)
    # print("ANGLE = {}".format(my.left_servo.get_angle()))

# my.left_servo.set_angle(0)
board.exit()
