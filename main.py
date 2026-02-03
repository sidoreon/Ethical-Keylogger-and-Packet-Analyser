import os
import sys
import subprocess
import time

BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASEDIR)

def main():
    print("Ethical Keylogger and Packet Analyzer\n")

    processes = []

    try:
        print("Starting input monitor")
        p_input = subprocess.Popen(
            [sys.executable, "-m", "input.inputmonitor"]
        )
        processes.append(p_input)

        print("Starting network monitor")
        p_net = subprocess.Popen(
            ["sudo", sys.executable, "-m", "network.packetmonitor"]
        )
        processes.append(p_net)

        print("\nMonitoring active. Press Ctrl+C to stop.")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDeactivating monitors")

    finally:
        for p in processes:
            if p.poll() is None:
                p.terminate()

        print("Monitors deactivated.")

        print("\nRunning analysis.")
        subprocess.run(
            [sys.executable, "-m", "detection.analyse"]
        )

        print("Analysis complete. Exiting.")

if __name__ == "__main__":
    main()
