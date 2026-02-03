import json
import os
from datetime import datetime

inputlog = "logs/input.log"
netlog = "logs/network.log"
outputlog = "logs/output.log"

TIMETOL = 10

keylimit = 40
delaylimit = 0.05
synlimit = 20

def readtime(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def loadval(path):
    records = []
    if not os.path.exists(path):
        return records
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    return records

def flaginput(val):
    return val["keys"] >= keylimit and val["mediandelay"] <= delaylimit

def flagnetwork(val):
    return val["syncnt"] >= synlimit

def analyse():
    inputvals = loadval(inputlog)
    netvals = loadval(netlog)

    flaggedinputs = [i for i in inputvals if flaginput(i)]
    flaggednets = [n for n in netvals if flagnetwork(n)]

    visinput = set()
    visnet = set()
    alerts = []

    for i in range(len(flaggedinputs)):
        vali = flaggedinputs[i]
        for j in range(len(flaggednets)):
            valn = flaggednets[j]
            
            if abs(vali["ts"] - valn["ts"]) <= TIMETOL:
                alert = {
                    "ts": min(vali["ts"], valn["ts"]),
                    "time": readtime(min(vali["ts"], valn["ts"])),
                    "type": "correlationalert",
                    "severity": "high",
                    "reason": "Flagged Simultaneous Input and Network Anomaly",
                    "inputdata": vali,
                    "networkdata": valn
                }
                alerts.append(alert)
                visinput.add(i)
                visnet.add(j)
                break

    for i in range(len(flaggedinputs)):
        if i not in visinput:
            vali = flaggedinputs[i]
            alert = {
                "ts": vali["ts"],
                "time": readtime(vali["ts"]),
                "type": "inputanomaly",
                "severity": "low",
                "reason": "Flagged Input Anomaly",
                "inputdata": vali
            }
            alerts.append(alert)

    for j in range(len(flaggednets)):
        if j not in visnet:
            valn = flaggednets[j]
            alert = {
                "ts": valn["ts"],
                "time": readtime(valn["ts"]),
                "type": "networkanomaly",
                "severity": "medium",
                "reason": "Flagged Network Anomaly",
                "networkdata": valn
            }
            alerts.append(alert)

    alerts.sort(key=lambda x: x["ts"])

    if alerts:
        with open(outputlog, "a") as out:
            for alert in alerts:
                out.write(json.dumps(alert) + "\n")
        print(f"Analysis complete. {len(alerts)} alerts generated in {outputlog}")
    else:
        print("Analysis complete. No anomalies detected.")

if __name__ == "__main__":
    analyse()
