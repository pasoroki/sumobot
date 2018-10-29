import zorg
import time
from threading import Thread, Event
from modules.controls import keyboard_reader, getch
from sys import stdin


stop = Event()
data = []
thread = None
# fd = stdin.fileno()
fd = stdin

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
    thread.start()
    print("LETSGO!")
    while not stop.is_set():
        print("WORK running")
        time.sleep(0.1)
        if data:
            action = data.pop(0)
            print("\r" + " ".join(data))
            if action == "q":
                print("STOP!!!!")
                stop.set()
            elif action == "w":
                my.left_servo.set_angle(1)
            elif action == "s":
                my.left_servo.set_angle(10)
            else:
                my.left_servo.set_angle(0)

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

thread = Thread(target=keyboard_reader, args=(data, stop, fd))
# thread.start()
print(" --> next")
robot.start()
