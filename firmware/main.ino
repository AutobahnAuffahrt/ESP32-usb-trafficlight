// Firmware: LED Control + Serial/COM (1 Byte: 0..3)

static const int LED_RED_PIN = 23;
static const int LED_YELLOW_PIN = 19;
static const int LED_GREEN_PIN = 13;

void setLight(uint8_t state) {
  digitalWrite(LED_RED_PIN, state == 1 ? HIGH : LOW);
  digitalWrite(LED_YELLOW_PIN, state == 2 ? HIGH : LOW);
  digitalWrite(LED_GREEN_PIN, state == 3 ? HIGH : LOW);
}

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  pinMode(LED_RED_PIN, OUTPUT);
  pinMode(LED_YELLOW_PIN, OUTPUT);
  pinMode(LED_GREEN_PIN, OUTPUT);
  setLight(0);

  Serial.println("USB Traffic Light: ready (Serial fallback bytes 0..3)");
}

void loop() {
  while (Serial.available() > 0) {
    int value = Serial.read();
    if (value >= 0 && value <= 3) {
      setLight((uint8_t)value);
    }
  }
  delay(10);
}
