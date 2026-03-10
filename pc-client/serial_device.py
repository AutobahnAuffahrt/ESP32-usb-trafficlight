"""Find Serial Device (ESP32 classic fallback)."""

from __future__ import annotations

from serial import Serial
from serial.tools import list_ports


def open_serial_device(baudrate: int = 115200, timeout: float = 1.0) -> Serial:
    ports = list(list_ports.comports())
    known_vids = {0x10C4, 0x1A86, 0x0403, 0x067B}
    keywords = ("cp210", "silicon labs", "ch340", "ch341", "ftdi", "usb to uart")

    for p in ports:
        desc = (p.description or "").lower()
        hwid = (p.hwid or "").lower()
        vid = getattr(p, "vid", None)
        pid = getattr(p, "pid", None)
        if (vid in known_vids) or any(k in desc or k in hwid for k in keywords):
            ser = Serial()
            ser.port = p.device
            ser.baudrate = baudrate
            ser.timeout = timeout
            # Avoid auto-reset impulses: keep DTR/RTS low BEFORE opening.
            ser.dtr = False
            ser.rts = False
            try:
                ser.dsrdtr = False
                ser.rtscts = False
            except Exception:
                pass
            ser.open()
            return ser

    raise RuntimeError("No suitable serial device found (CP210x/CH340/FTDI).")
