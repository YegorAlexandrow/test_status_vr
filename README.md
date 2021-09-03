# Setup guide

1. Install [redis](https://redis.io/download).

1. Setup python ([guide for windows](https://www.python.org/downloads/windows/))

2. Setup pip ([guide for windows](https://www.liquidweb.com/kb/install-pip-windows/))

3. Install requirements:
```
pip install -r requirements.txt
```

4. Set redis-server host, port, password in `test_status_vr.py`:
```
_redis_conn = redis.Redis(
    host='your ip',
    port=6379, # your port
    password='your pass',
    db=0
)
```

5. Run the script:
```
python test_status_vr.py
```

6. Check redis:
```
$ redis-cli -h <host> -p <port>
redis> CONFIG SET requirepass <your pass>
OK
redis> SUBSCRIBE status

1) "message"
2) "status"
3) "{\"robot_state\": \"ARM_OPERATING_ST\", ...
```