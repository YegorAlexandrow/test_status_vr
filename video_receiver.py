import cv2
import redis
import numpy as np
import base64

REDIS_ADDRES = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = 'DTL@b2021'

redis_connection = redis.Redis(host=REDIS_ADDRES, port=REDIS_PORT, db=0, password=REDIS_PASSWORD)
pubsub = redis_connection.pubsub()

# Receiving commands in separate thread
pubsub.subscribe('video')

while True:
    img_str = pubsub.get_message()
    if img_str is not None:
        if img_str['data'] != 1:
            jpg_original = base64.b64decode(img_str['data'])
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            decoded_frame = cv2.imdecode(jpg_as_np, flags=1)

            cv2.imshow('frame', decoded_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()