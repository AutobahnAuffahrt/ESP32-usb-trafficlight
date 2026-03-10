# Protokoll (1 Byte)

Aktuell wird **Serial/COM** verwendet (ESP32 classic). Später ist eine **USB-HID** Erweiterung (ESP32-S3) geplant.

Report-/Payloadgröße: 1 Byte

| Wert | Bedeutung     |
| ---- | ------------- |
|    0 | alle LEDs aus |
|    1 | rot           |
|    2 | gelb          |
|    3 | grün          |

Hinweis: Serial und späteres HID nutzen dieselbe 1-Byte-Wertemappung (0–3).
