import time
import math
import board
import busio
import requests
import adafruit_adxl34x

BOT_TOKEN = 'your_bot_token'
CHAT_ID = 'guardian_chat_id'

FREEFALL_THRESHOLD = 3.0
FREEFALL_COUNT_LIMIT = 5

i2c = busio.I2C(board.SCL, board.SDA)
accelerometer = adafruit_adxl34x.ADXL345(i2c)


def send_notification(message):
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    try:
        requests.post(url, data=data, timeout=10)
    except requests.exceptions.RequestException as e:
        print("Notification failed:", e)


freefall_count = 0
freefall_flag = False

while True:
    x, y, z = accelerometer.acceleration
    total_acc = math.sqrt(x * x + y * y + z * z)
    print("x: %.2f, y: %.2f, z: %.2f, total: %.2f" % (x, y, z, total_acc))

    if total_acc < FREEFALL_THRESHOLD:
        freefall_count += 1
    else:
        freefall_count = 0
        freefall_flag = False

    if freefall_count > FREEFALL_COUNT_LIMIT and not freefall_flag:
        freefall_flag = True
        print("Fall Detected")
        send_notification("Fall Detected")

    time.sleep(0.05)
