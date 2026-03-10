"""Send LED commands (Serial fallback).

Protocol: send exactly 1 byte:
0=off, 1=red, 2=yellow, 3=green
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

from serial_device import open_serial_device


def send_light(state: int) -> None:
    if state not in (0, 1, 2, 3):
        raise ValueError("state must be 0..3")
    ser = open_serial_device(timeout=0.1)
    try:
        ser.write(bytes([state]))
        ser.flush()

        end = time.monotonic() + 0.4
        while time.monotonic() < end:
            if getattr(ser, "in_waiting", 0) <= 0:
                time.sleep(0.02)
                continue
            line = ser.readline()
            if line:
                print(line.decode(errors="ignore").rstrip())
    finally:
        ser.close()


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python traffic_light.py red|yellow|green|off")
        return 2

    mapping = {"off": 0, "red": 1, "yellow": 2, "green": 3}
    cmd = argv[1].lower()
    if cmd not in mapping:
        print("Usage: python traffic_light.py red|yellow|green|off")
        return 2

    send_light(mapping[cmd])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
