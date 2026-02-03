import json
import os
from datetime import datetime

def readtime(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

netlog = "logs/network.log"
alertlog = "logs/alerts.log"

syncntlim = 20
portfocusratio = 0.6 

def detect():
    if not os.path.exists(netlog):
        return

    with open(netlog) as f:
        for line in f:
            record = json.loads(line)
            syncnt = record["syncnt"]
            if syncnt < syncntlim:
                continue
            ports = record["ports"]
            topport = record["topport"]
            if not ports or topport is None:
                continue
            topcount = ports[str(topport)] if str(topport) in ports else ports[topport]
            focusratio = topcount/syncnt
            if focusratio >= portfocusratio:
                alert = {
                    "ts": record["ts"],
                    "time": readtime(record["ts"]),
                    "type": "networkanomaly",
                    "severity": "medium",
                    "reason": "Flagged high volume of SYNs focused on a single port",
                    "topport": topport,
                    "syncnt": syncnt,
                    "focusratio": round(focusratio, 2)
                }
                with open(alertlog, "a") as out:
                    out.write(json.dumps(alert) + "\n")


if __name__ == "__main__":
    detect()
