from pynput import keyboard
import time
import json
import signal
import sys
from datetime import datetime

def readtime(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

TIMEPDT = 10
presstimes = []
starttime = time.time()

def press(key):
    global presstimes
    presstimes.append(time.time())


def flush():
    global presstimes, starttime
    if not presstimes:
        return
    intervals = []
    for i in range(1, len(presstimes)):
        span = presstimes[i] - presstimes[i - 1]
        intervals.append(span)
    mediantime = 0
    if intervals:
        sortedi = sorted(intervals)
        n = len(sortedi)
        mid = n // 2
        if n % 2 == 1:
            mediantime = sortedi[mid]
        else:
            mediantime = (sortedi[mid - 1] + sortedi[mid])/2
    maxburst = sum(1 for d in intervals if d < 0.1)
    record = {
        "ts" : int(starttime),
        "time" : readtime(int(starttime)),
        "keys" : len(presstimes),
        "mediandelay" : round(mediantime, 4),
        "maxburst" : maxburst
    }
    with open("logs/input.log", "a") as f:
        f.write(json.dumps(record) + "\n")
    presstimes = []
    starttime = time.time()

def shutdown(sig, frame):
    flush()
    sys.exit(0)

def main():
    global starttime
    starttime = time.time()
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    with keyboard.Listener(on_press=press) as listener:
        while(True):
            time.sleep(1)
            if time.time() - starttime >= TIMEPDT:
                flush()

if __name__ == "__main__":
    main()



