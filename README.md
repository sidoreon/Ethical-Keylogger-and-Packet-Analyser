# Ethical Keylogger and Packet Analyser

A Python-based security monitoring system that detects potential threats by correlating keyboard input patterns with network traffic anomalies.

## Overview

An ethical security tool that identifies suspicious activities by monitoring keyboard input patterns and network traffic, then correlating these signals to generate alerts.

## Features

- Real-time keyboard and network traffic monitoring
- Correlation engine for identifying simultaneous anomalies
- Tiered alert system (LOW, MEDIUM, HIGH severity)
- Rule-based detection for focused attacks
- JSON logging for all events and alerts

## Project Structure

```
ethical_keylogger_and_packet_analyser/
├── detection/
│   ├── __init__.py
│   ├── analyse.py      # Correlation engine and alert generation
│   └── rules.py        # Rule-based detection for focused attacks
├── input/
│   ├── __init__.py
│   └── inputmonitor.py # Keyboard monitoring module
├── network/
│   ├── __init__.py
│   └── packetmonitor.py # Network packet capture and analysis
├── logs/
|   |___.gitkeep          # Keeps logs/ directory in version control
│   ├── input.log       # Input activity records
│   ├── network.log     # Network traffic records
│   ├── output.log      # Correlated alerts
│   └── alerts.log      # Rule-based alerts
├── main.py             # Application entry point
|__ .gitignore          # Git ignore file
└── README.md            # Project documentation
```

## Requirements

- Python 3.6+
- `pynput` and `scapy` packages
- Root/Administrator privileges for packet capture

## Installation

```bash
pip install pynput scapy
```

## Usage

**Start monitoring:**
```bash
python main.py
```
Press `Ctrl+C` to stop and generate alerts.

**Individual components:**
```bash
python -m input.inputmonitor                    # Input monitor only
sudo python -m network.packetmonitor           # Network monitor only
python -m detection.analyse                     # Run analysis
sudo python -m network.packetmonitor -i eth0   # Specify interface
```

## Detection Logic

**Input Anomaly:** ≥40 keys with ≤0.05s median delay in 10s window (indicates automation/bots)

**Network Anomaly:** ≥20 SYN packets in 10s window (indicates SYN floods/port scans)

**Correlation:** HIGH severity alert when both occur within 10s

**Rule-based:** Flags when ≥60% of SYNs target a single port

## Alert Severity Levels

| Severity | Condition | Description |
|----------|-----------|-------------|
| **HIGH** | Input + Network correlation | Simultaneous input and network anomalies detected |
| **MEDIUM** | Network anomaly only | Unusual network activity or focused port attacks |
| **LOW** | Input anomaly only | Suspicious keyboard patterns without network activity |

## Log Files

### input.log
Records keyboard activity metrics:
```json
{
  "ts": 1738584123,
  "time": "2026-02-03 14:22:03",
  "keys": 45,
  "mediandelay": 0.0342,
  "maxburst": 12
}
```

### network.log
Records network traffic metrics:
```json
{
  "ts": 1738584125,
  "time": "2026-02-03 14:22:05",
  "syncnt": 24,
  "ports": {"80": 15, "443": 9},
  "topport": 80
}
```

### output.log
Correlated alerts:
```json
{
  "ts": 1738584123,
  "time": "2026-02-03 14:22:03",
  "type": "correlationalert",
  "severity": "high",
  "reason": "Flagged Simultaneous Input and Network Anomaly",
  "inputdata": {...},
  "networkdata": {...}
}
```

### alerts.log
Rule-based detections:
```json
{
  "ts": 1738584130,
  "time": "2026-02-03 14:22:10",
  "type": "networkanomaly",
  "severity": "medium",
  "reason": "Flagged high volume of SYNs focused on a single port",
  "topport": 22,
  "syncnt": 35,
  "focusratio": 0.89
}
```

## Configuration

**analyse.py:**
- `TIMETOL = 10` - Correlation time window (seconds)
- `keylimit = 40` - Minimum keys for input anomaly
- `delaylimit = 0.05` - Maximum median delay
- `synlimit = 20` - Minimum SYN count

**rules.py:**
- `syncntlim = 20` - Minimum SYNs for rule evaluation
- `portfocusratio = 0.6` - Threshold for focused attacks

**inputmonitor.py / packetmonitor.py:**
- `TIMEPDT = 10` - Data collection window (seconds)

## Ethical Considerations

**For authorized security monitoring only.**

**Appropriate Use:**
- Your own systems
- Authorized security testing
- Educational purposes with authorization

**Prohibited:**
- Unauthorized monitoring
- Privacy law violations

Ensure proper authorization and legal compliance before deployment.

## License

For educational and authorized security monitoring purposes only. Users must comply with all applicable laws.

## Disclaimer

Provided "as is" without warranty. Authors not responsible for misuse or damage.