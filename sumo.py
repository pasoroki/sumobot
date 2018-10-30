import time
from threading import Event
from modules.joystick import Joystick
from modules.arduino import SumoBot, BotWheel
import pygame
# from pygame.locals import QUIT, KEYDOWN, KEYUP
import logging


LOG = logging.getLogger(__name__)
stop = Event()

left_wheel_front = BotWheel(
    pin         = 6,
    speed_limit = 1,
    inverted    = False
)
left_wheel_back = BotWheel(
    pin         = 9,
    speed_limit = 1,
    inverted    = False
)

right_wheel_front = BotWheel(
    pin         = 5,
    speed_limit = 1,
    inverted    = True
)
right_wheel_back = BotWheel(
    pin         = 10,
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




#
#
# # while not stop.is_set():
# #     # print(f"\n - content: {data}")
# #     # print("a")
# #     time.sleep(0.5)
# #     if data:
# #         action = data.pop(0)
# #         print("\r" + " ".join(data))
#
#
#
# def mypprint(obj):
#     for i in dir(obj):
#         if i.startswith("_"): continue
#         print(" - {:20} : {}".format(i, getattr(obj, i)))
#
#
# def work(my):
#     print("WORK")
#     global stop
#     # global thread
#     # thread.start()
#     angle = 0
#     while not stop.is_set():
#         time.sleep(0.1)
#         data = get_state()
#         if data:
#             for action in data.keys():
#                 # action = data.pop(0)
#                 # print("\r" + " ".join(data))
#                 print(" --> {}".format(action))
#                 if action == "q":
#                     print("STOP!!!!")
#                     stop.set()
#
#                 elif action in ("up", 273, pygame.K_UP):
#                     print(" UP ")
#                     # my.left_servo.set_angle(150)
#                     angle += 1
#                     my.left_servo.set_angle(angle)
#
#                 elif action in ("down", 274, pygame.K_DOWN):
#                     print(" DOWN ")
#                     angle -= 1
#                     # my.left_servo.set_angle(-150)
#                     my.left_servo.set_angle(angle)
#
#                 elif action in ("left", 276, pygame.K_LEFT):
#                     print(" LEFT ")
#                     angle -= 10
#                     # my.left_servo.set_angle(-150)
#                     my.left_servo.set_angle(angle)
#
#                 elif action in ("right", 275, pygame.K_RIGHT):
#                     print(" RIGHT ")
#                     angle += 10
#                     # my.left_servo.set_angle(-150)
#                     my.left_servo.set_angle(angle)
#
#                 elif action in (32, pygame.K_SPACE):
#                     print(" SPACE ")
#                     angle = 0
#                     # my.left_servo.set_angle(0)
#                     my.left_servo.set_angle(angle)
#
#                 else:
#                     print(" ELSE ")
#                     angle = 0
#                     # my.left_servo.set_angle(0)
#                     my.left_servo.set_angle(angle)
#
#
#         print("ANGLE = {}".format(my.left_servo.get_angle()))
#
#     my.left_servo.set_angle(0)
#
#
#
#
#
#         # while True:
#     #
#     #     print("1")
#     #     # Move the servo to 20 degrees
#     #     print(my)
#     #     mypprint(my)
#     #
#     #     print("\n\n LEFT SERVO:")
#     #     # mypprint(my.left_servo)
#     #
#     #     print("\n\n\n-----------\n\n\n")
#     #
#     #
#     #     my.left_servo.set_angle(20)
#     #
#     #     print("2")
#     #     print("Servo angle set to", my.left_servo.get_angle())
#     #
#     #     # Wait 1 seconds before doing it again
#     #     time.sleep(1)
#     #
#     #     # Move the servo to 100 degrees
#     #     my.left_servo.set_angle(100)
#     #
#     #     print("Servo angle set to", my.left_servo.get_angle())
#     #
#     #     # Wait 1 seconds before doing it again
#     #     time.sleep(1)
#
# # robot = zorg.robot({
# #     "connections": {
# #         "ArduinoLeonardo": {
# #             "adaptor": "zorg_firmata.Firmata",
# #             # "port": "/dev/ttyACM0",
# #             "port": "/dev/tty.usbmodem14101",
# #         },
# #     },
# #     "devices": {
# #         "left_servo": {
# #             "connection": "ArduinoLeonardo",
# #             "driver":     "zorg_grove.Servo",
# #             "port_id":       "/dev/tty.usbmodem14101",
# #             "pin":        9,  # 9 is a pwm pin
# #         },
# #         # "right_servo": {
# #         #     "connection": "ArduinoLeonardo",
# #         #     "driver":     "zorg_grove.Servo",
# #         #     "pin":        10,  # 10 is a pwm pin
# #         # }
# #     },
# #     "name": "Servo Robot", # Give your robot a unique name
# #     "work": work, # The method where the work will be done
# # })
#



# # thread = Thread(target=keyboard_reader, args=(data, stop, fd))
# # thread.start()
# print(" --> next")
# # robot.start()
#
# import pyfirmata
# PORT = "/dev/tty.usbmodem14101"
# board = pyfirmata.Arduino(PORT)
#
# PIN = 9 # Pin 12 is used
# DELAY = 2 # A 2 seconds delay
#
# # print("pyFirmata version:\t%s" % pyfirmata.__version__)
# # print("Hardware:\t\t%s" % board.__str__())
# # #print "Firmata firmware name:  %s" % board.get_firmware()
# # print("Firmata firmware:\t%i.%i" % \
# #     (board.get_firmata_version()[0], board.get_firmata_version()[1]))
#
# stop = Event()
#
# # print("ON")
# # board.digital[PIN].write(1) # Set the LED pin to 1 (HIGH)
# # board.pass_time(DELAY)
# # print("OFF")
# # board.digital[PIN].write(0) # Set the LED pin to 0 (LOW)
# # board.pass_time(DELAY)
#
# print("WORK")
#
#
# # Definition of the pin, one with PWM, marked as ~XX on the Arduino
# digital_0 = board.get_pin('d:9:p')
# print(" --> PIN: {}".format(digital_0))
#
# board.servo_config(pin=9, min_pulse=544, max_pulse=2400, angle=0)
#
# # # Time (approx. seconds) to get to the maximum/minimum
# # DURATION = 5
# # # Numbers of steps to get to the maximum/minimum
# # STEPS = 10
# #
# # # Waiting time between the
# # wait_time = DURATION/float(STEPS)
# #
# # # Note: Value range for PWM is 0.0 till 1.0
# #
# # # Up
# # for i in range(1, STEPS + 1):
# #     value = i/float(STEPS)
# #     digital_0.write(value)
# #     board.pass_time(wait_time)
# #
# # # Down
# # increment = 1/float(STEPS)
# # while STEPS > 0:
# #     value = increment * STEPS
# #     digital_0.write(value)
# #     board.pass_time(wait_time)
# #     STEPS = STEPS - 1
# #
# # board.exit()
# # exit()
#
# # global stop
# # global thread
# # thread.start()

print("Prepare the robot!")
bot.stop()
bot.execute()


print("Ready to serve")
while not stop.is_set():
    time.sleep(0.1)
    # data = joystick.get_buttons_state()
    data = joystick.get_buttons_state
    if data:
        for action in data.keys():
            print(" --> {}".format(action))
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
                angle = 93
                bot.stop()
                # my.left_servo.set_angle(0)

            else:
                print(" ELSE ")
                angle = 0
                # my.left_servo.set_angle(0)
    else:
        print(".")
        bot.stop()
    print(" -> execute")
    bot.execute()
    # print("ANGLE = {}".format(my.left_servo.get_angle()))

bot.stop()
# board.exit()
