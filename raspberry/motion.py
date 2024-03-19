import gpiozero
from time import sleep
from threading import Thread
import meshtastic
import meshtastic.serial_interface
import logging
from sys import stdout, exit
from os import path

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
stream_handler = logging.StreamHandler(stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
import meshtastic
import meshtastic.serial_interface
import logging
from sys import stdout

# Logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = False
stream_handler = logging.StreamHandler(stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

led = gpiozero.LED(1)
motion = gpiozero.MotionSensor(17)
meshtastic_device_path = '/dev/ttyACM0'

def blink_led():
    while True:
        led.on()
        sleep(0.5)
        led.off()
        sleep(0.5)

def motion_detection():
    logger.info("Starting motion detection")
    while True:
        motion.wait_for_motion()
        interface.sendText("Motion detected")
        logger.info("Motion detected")
        sleep(1)


if __name__ == "__main__":

    if path.exists(meshtastic_device_path):
        logger.debug("Creating Meshtastic device interface")
        interface = meshtastic.serial_interface.SerialInterface(devPath=meshtastic_device_path)
    else:
        logger.critical(f"Unable to connect to LoRA device on serial port")
        exit(1)

    th_blink = Thread(target=blink_led)
    th_blink.daemon = True
    #th_blink.start()

    th_motion = Thread(target=motion_detection)
    th_motion.daemon = True
    th_motion.start()

    while True:
        logger.debug("Running")
        sleep(1)
