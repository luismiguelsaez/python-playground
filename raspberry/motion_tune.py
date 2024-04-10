from gpiozero import MotionSensor, TonalBuzzer, LED
from gpiozero.tones import Tone
from time import sleep
import logging
import threading
import subprocess
from datetime import datetime

# GPIO configuration
buzzer_pin = 2
buzzer_frequency = 500
motion_pin = 14
motion_queue_length = 10
motion_sample_rate = 10
motion_threshold = 0.1
led_pin = 4
led_time = 0.5
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
led = LED(pin=led_pin)

tune =  [
            ('C#4', 0.2), ('D4', 0.2), (None, 0.2),
            ('Eb4', 0.2), ('E4', 0.2), (None, 0.6),
            ('F#4', 0.2), ('G4', 0.2), (None, 0.6),
            ('Eb4', 0.2), ('E4', 0.2), (None, 0.2),
            ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
            ('C4', 0.2), ('B4', 0.2), (None, 0.2),
            ('F#4', 0.2), ('G4', 0.2), (None, 0.2),
            ('B4', 0.2), ('Bb4', 0.5), (None, 0.6),
            ('A4', 0.2), ('G4', 0.2), ('E4', 0.2),
            ('D4', 0.2), ('E4', 0.2)
        ]

def play_tune(tune: list = [])->None:
    for note, duration in tune:
        buzzer.play(note)
        sleep(float(duration))
    buzzer.stop()

def stream_video(port: int = 8888)->None:
    subprocess.run(["libcamera-vid", "--timeout=0", "--inline", "--listen", f"--output=tcp://0.0.0.0:{port}"])

def wait_video(filename: str)->None:
    subprocess.run(["libcamera-vid", "--mode=640:480", "--initial=pause", "--signal=1", "--inline", "--timeout=0", "--split", f"--output={filename}"])

def capture_video(timeout_ms: int = 5000)->str:
    ts = datetime.today().strftime("%Y%m%d-%H%M%S")
    file_name = f"/tmp/{ts}"
    file_ext = "h264"
    file_ext_conv = "mp4"

    logger.debug(f"Capturing video: {file_name}.{file_ext}")
    cmd_capture = subprocess.run(["libcamera-vid", f"--output={file_name}.{file_ext}", f"--timeout={timeout_ms}", "--mode=640:480"], capture_output=True)
    if cmd_capture.returncode == 0:
        logger.debug(f"Captured video: {file_name}.{file_ext}")
    else:
        logger.error(f"Error capturing video [{cmd_capture.returncode}]: {cmd_capture.stdout.decode()}")

    logger.debug(f"Converting video: {file_name}.{file_ext} > {file_name}.{file_ext_conv}")
    cmd_convert = subprocess.run(["MP4Box", "-add", f"{file_name}.{file_ext}", f"{file_name}.{file_ext_conv}"], capture_output=True)
    if cmd_convert.returncode == 0:
        logger.debug(f"Converted video: {file_name}.{file_ext} > {file_name}.{file_ext_conv}")
    else:
        logger.error(f"Error converting video [{cmd_convert.returncode}]: {cmd_convert.stdout.decode()}")
    
    return f"{file_name}.{file_ext_conv}"

def blink_led(t: float = 0.5):
    while True:
        led.on()
        sleep(t)
        led.off()
        sleep(t)

thread_wait_video = threading.Thread(target=wait_video, args=["/tmp/rolling-video.h264"])
thread_wait_video.daemon = True
#thread_wait_video.start()
thread_led = threading.Thread(target=blink_led, args=[led_time])
thread_led.daemon = True
thread_led.start()

while True:
    if motion.motion_detected:
        logger.info(f"Motion detected")
        video_file = capture_video(timeout_ms=20000)
        #play_tune(tune)

    sleep(loop_sleep_time)
