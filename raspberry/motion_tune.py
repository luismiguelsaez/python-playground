from gpiozero import MotionSensor, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import logging
from sys import stdout

# GPIO configuration
buzzer_pin = 2
buzzer_frequency = 500
motion_pin = 14
motion_queue_length = 10
motion_sample_rate = 10
motion_threshold = 0.1
loop_sleep_time = 0.5

# Logging configuration
logger = logging.getLogger("main")
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - [%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Initialize in/out objects
logger.debug(f"Initializing objects: buzzer({buzzer_pin}), motionsensor({motion_pin})")
buzzer = TonalBuzzer(pin=buzzer_pin)
motion = MotionSensor(pin=motion_pin, queue_len=motion_queue_length, sample_rate=motion_sample_rate, threshold=motion_threshold)

tune = [('C#4', 0.2), ('D4', 0.2), (None, 0.2),
    ('Eb4', 0.2), ('E4', 0.2), (None, 0.6),
    ('F#4', 0.2), ('G4', 0.2), (None, 0.6),
    ('Eb4', 0.2), ('E4', 0.2), (None, 0.2),
    ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
    ('C4', 0.2), ('B4', 0.2), (None, 0.2),
    ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
    ('B4', 0.2), ('Bb4', 0.5), (None, 0.6),
    ('A4', 0.2), ('G4', 0.2), ('E4', 0.2),
    ('D4', 0.2), ('E4', 0.2)]

def play_tune(tune: list = [])->None:
    for note, duration in tune:
        buzzer.play(note)
        sleep(float(duration))
    buzzer.stop()

while True:
    if motion.motion_detected:
        logger.info(f"Motion detected")
        play_tune(tune)

    sleep(loop_sleep_time)