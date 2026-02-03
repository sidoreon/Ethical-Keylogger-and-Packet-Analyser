from scapy.all import sniff, IP, TCP, conf
import time
import json
import os
import signal
import sys
import argparse
from datetime import datetime

def readtime(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

TIMEPDT = 10

os.makedirs("logs", exist_ok=True)

portcnt = {}
starttime = time.time()
active = True

def handlepacket(pkt):
    global portcnt
    if IP in pkt and TCP in pkt:
        flags = pkt[TCP].flags
        if flags & 0x02:
            dport = pkt[TCP].dport
            portcnt[dport] = portcnt.get(dport, 0) + 1

def flush():
    global portcnt, starttime
    if not portcnt:
        record = {
            "ts": int(starttime),
            "time" : readtime(int(starttime)),
            "syncnt": 0,
            "ports": {},
            "topport": None
        }
        with open("logs/network.log", "a") as f:
            f.write(json.dumps(record) + "\n")
        starttime = time.time()
        return
    
    syncnt = sum(portcnt.values())
    topport = max(portcnt, key = portcnt.get)
    record = {
        "ts" : int(starttime),
        "time" : readtime(int(starttime)),
        "syncnt" : syncnt,
        "ports" : portcnt,
        "topport" : int(topport)
    }
    with open("logs/network.log", "a") as f:
        f.write(json.dumps(record) + "\n")

    portcnt = {}
    starttime = time.time()

def shutdown(sig, frame):
    global active
    active = False
    flush()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

parser = argparse.ArgumentParser()
defaultiface = "lo0" if sys.platform == "darwin" else conf.iface
parser.add_argument("-i", "--iface", type=str, default=defaultiface)
args = parser.parse_args()

while active:
    sniff(
        iface = args.iface,
        filter="tcp",
        prn=handlepacket,
        store=False,
        timeout=1
    )
    if time.time() - starttime >= TIMEPDT:
        flush()
