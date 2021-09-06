import base64
import redis
import time
import cv2


def _convert_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
    jpg_as_text = base64.b64encode(buffer)

    return jpg_as_text

_redis_conn = redis.Redis(
    host='localhost',
    port=6379,
    password='DTL@b2021',
    db=0
)


frame = cv2.imread('frame.png')
converted_frame = _convert_frame(frame)


while True:
    _redis_conn.publish('video', converted_frame)
    time.sleep(0.1)
