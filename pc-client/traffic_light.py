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


def _write_state(ser, state: int) -> None:
    if state not in (0, 1, 2, 3):
        raise ValueError("state must be 0..3")
    ser.write(bytes([state]))
    ser.flush()


def send_light(state: int) -> None:
    ser = open_serial_device(timeout=0.1)
    try:
        _write_state(ser, state)

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


def run_cycle(total_seconds: float) -> None:
    if total_seconds <= 0:
        return

    phases: list[tuple[int, float]] = [
        (3, 10.0),  # green
        (2, 2.0),  # yellow
        (1, 10.0),  # red
        (2, 2.0),  # yellow
    ]

    ser = open_serial_device(timeout=0.1)
    try:
        end_total = time.monotonic() + float(total_seconds)
        while time.monotonic() < end_total:
            for state, phase_seconds in phases:
                now = time.monotonic()
                if now >= end_total:
                    break

                _write_state(ser, state)
                end_phase = min(end_total, now + phase_seconds)
                while True:
                    remaining = end_phase - time.monotonic()
                    if remaining <= 0:
                        break
                    time.sleep(min(0.1, remaining))
    finally:
        try:
            _write_state(ser, 0)
        finally:
            ser.close()


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python traffic_light.py red|yellow|green|off")
        print("       python traffic_light.py cycle <seconds>")
        return 2

    mapping = {"off": 0, "red": 1, "yellow": 2, "green": 3}
    cmd = argv[1].lower()
    try:
        total_seconds_shorthand = float(cmd)
    except ValueError:
        total_seconds_shorthand = None
    if total_seconds_shorthand is not None:
        if len(argv) != 2:
            print("Usage: python traffic_light.py <seconds>")
            return 2
        run_cycle(total_seconds_shorthand)
        return 0
    if cmd == "cycle":
        if len(argv) != 3:
            print("Usage: python traffic_light.py cycle <seconds>")
            return 2
        try:
            total_seconds = float(argv[2])
        except ValueError:
            print("seconds must be a number")
            return 2
        run_cycle(total_seconds)
    else:
        if len(argv) != 2 or cmd not in mapping:
            print("Usage: python traffic_light.py red|yellow|green|off")
            print("       python traffic_light.py cycle <seconds>")
            return 2
        send_light(mapping[cmd])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
