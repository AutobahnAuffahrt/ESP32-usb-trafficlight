# ESP32 USB Traffic Light (Serial/COM)

Dieses Repo baut ein kleines **Ampelgerät** (Rot/Gelb/Grün), das aktuell über **Serial/COM** vom PC gesteuert wird:

- ESP32 (classic) am USB‑UART (z. B. CP210x) → **COM‑Port**
- Steuerung per **Python CLI**
- Protokoll: **1 Byte**, Werte **0..3**

## Geplant: USB HID (ESP32-S3)

Ein **ESP32-S3** (natives USB-Device) ist bestellt. Sobald er da ist, möchte ich das Projekt um eine **USB-HID Variante ohne COM-Port** erweitern.

Wichtig: In diesem Stand ist **kein HID-Code** eingecheckt – nur die funktionierende Serial/COM-Variante.

## Hardware

- ESP32‑S3 Dev Board (native USB erforderlich)
- 3× LED (rot, gelb, grün)
- 3× Widerstand 220–330Ω

Beispiel-Pinbelegung (anpassbar):

| LED  | GPIO   |
| ---- | ------ |
| Rot  | GPIO23 |
| Gelb | GPIO19 |
| Grün | GPIO13 |

Schaltung je LED:

`GPIO → Widerstand → LED → GND`

## 3D‑Modell (Gehäuse)

Ich habe ein passendes Ampel-/Gehäusemodell von **Thingiverse** verwendet und ausgedruckt.

- Quelle/Attribution und Druckhinweise stehen in `docs/3d-model.md`
- Die `.stl` Dateien liegen unter `docs/3d/`

## Protokoll (1 Byte)

Das Gerät erwartet genau **1 Byte**:

| Wert | Bedeutung     |
| ---- | ------------- |
| 0    | alle LEDs aus |
| 1    | rot           |
| 2    | gelb          |
| 3    | grün          |

## Repository-Struktur

Die Zielstruktur ist:

```text
usb-traffic-light/
├─ firmware/
│  ├─ main.ino
│  └─ config.h
├─ pc-client/
│  ├─ traffic_light.py
│  ├─ serial_device.py
│  └─ requirements.txt
├─ docs/
│  ├─ 3d-model.md
│  ├─ 3d/
│  │  └─ (STL/3MF/STEP Dateien + README.md)
│  ├─ protocol.md
│  └─ hardware.md
└─ README.md
```

## Aktueller Stand

- Firmware liest in `firmware/main.ino` Serial-Bytes **0..3** und schaltet die LEDs.
- PC-Client in `pc-client/` findet den COM‑Port automatisch und sendet **1 Byte**.
- CLI: `python pc-client/traffic_light.py red|yellow|green|off`

## PC-Client (Python)

Abhängigkeit:

- `pyserial` (Serial/COM, inkl. Auto-Find)

Installation (virtuelle Umgebung empfohlen):

```bash
pip install -r pc-client/requirements.txt
```

## Build (PlatformIO)

Dieses Repo ist als PlatformIO-Projekt konfiguriert. Die Quellen liegen bewusst in `firmware/` (siehe `platformio.ini` mit `src_dir = firmware`).

Build:

```bash
pio run
```

Upload (Port ggf. anpassen):

```bash
pio run -t upload
```

Hinweis: Aktuell ist das Projekt auf **ESP32 classic + Serial/COM** ausgelegt. Eine spätere ESP32-S3/HID-Erweiterung ist geplant.

## Projektziel

- Jetzt: zuverlässig per **Serial/COM** steuerbar (Auto-Port-Find, 1 Byte).
- Später: optionaler **USB-HID** Modus auf ESP32-S3 (ohne COM-Port).
