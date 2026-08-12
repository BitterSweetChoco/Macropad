#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>

// ==================== ПРОТОТИПЫ ====================
void switchLayer();
void handleKeyPress(char key);
void updateDisplay();

// ==================== НАСТРОЙКИ ====================
#define I2C_ADDR 0x27
#define LCD_COLS 16
#define LCD_ROWS 2

// Пины клавиатуры (строки, столбцы)
const byte ROWS = 4, COLS = 4;
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {2, 3, 4, 5};
byte colPins[COLS] = {6, 7, 8, 9};

// Джойстик
#define JOY_SW_PIN 10   // кнопка джойстика (слои)
#define JOY_X_PIN A0    // ось X (влево/вправо – треки)
#define JOY_Y_PIN A1    // ось Y (вверх/вниз – громкость)

// Параметры джойстика (мультимедиа)
#define JOY_DEADZONE 200        // мёртвая зона (512 ± 200)
#define JOY_REPEAT_DELAY 150    // задержка повтора при удержании (мс)

// ==================== ОБЪЕКТЫ ====================
LiquidCrystal_I2C lcd(I2C_ADDR, LCD_COLS, LCD_ROWS);
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// ==================== СЛОИ ====================
const char* layerNames[] = {
  "1.Edit", "2.Apps", "3.Text", "4.System"
};
const int NUM_LAYERS = 4;

int currentLayer = 0; // активный слой (0..3)

// ==================== ПЕРЕМЕННЫЕ ДЛЯ КНОПКИ ДЖОЙСТИКА ====================
bool lastJoySW = HIGH;
unsigned long lastJoyDebounce = 0;
#define DEBOUNCE_DELAY 250

// ==================== ПЕРЕМЕННЫЕ ДЛЯ МУЛЬТИМЕДИА (оси) ====================
unsigned long lastJoyMediaEvent = 0;
String lastJoyDirection = "";

// ==================== ИНИЦИАЛИЗАЦИЯ ====================
void setup() {
  lcd.init();
  lcd.backlight();
  pinMode(JOY_SW_PIN, INPUT_PULLUP);

  Serial.begin(115200);
  Serial.println("Ready");   // тестовое сообщение

  lcd.setCursor(0,0);
  lcd.print("Macropad Ready");
  lcd.setCursor(0,1);
  lcd.print("Layer: ");
  lcd.print(layerNames[currentLayer]);
  delay(1000);
  updateDisplay();
}

// ==================== ОСНОВНОЙ ЦИКЛ ====================
void loop() {
  // 1. Проверка кнопки джойстика (с антидребезгом, смена слоя)
  bool joySW = digitalRead(JOY_SW_PIN);
  if (joySW == LOW && lastJoySW == HIGH) {
    unsigned long now = millis();
    if (now - lastJoyDebounce > DEBOUNCE_DELAY) {
      lastJoyDebounce = now;
      switchLayer();
    }
  }
  lastJoySW = joySW;

  // 2. Опрос клавиатуры
  char key = keypad.getKey();
  if (key) {
    handleKeyPress(key);
  }

  // 3. Оси джойстика – мультимедиа
  int x = analogRead(JOY_X_PIN);
  int y = analogRead(JOY_Y_PIN);

  String direction = "";

  if (x < 512 - JOY_DEADZONE) {
    direction = "LEFT";       // предыдущий трек
  } else if (x > 512 + JOY_DEADZONE) {
    direction = "RIGHT";      // следующий трек
  } else if (y < 512 - JOY_DEADZONE) {
    direction = "UP";         // громкость вверх
  } else if (y > 512 + JOY_DEADZONE) {
    direction = "DOWN";       // громкость вниз
  }

  if (direction != "") {
    if (direction != lastJoyDirection || millis() - lastJoyMediaEvent > JOY_REPEAT_DELAY) {
      Serial.print("J:");
      Serial.println(direction);
      lastJoyMediaEvent = millis();
    }
  } else {
    // Джойстик в нейтрали – сбрасываем направление
    lastJoyDirection = "";
  }
  lastJoyDirection = direction;
}

// ==================== ПЕРЕКЛЮЧЕНИЕ СЛОЯ ====================
void switchLayer() {
  currentLayer = (currentLayer + 1) % NUM_LAYERS;
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Switch to:");
  lcd.setCursor(0,1);
  lcd.print(layerNames[currentLayer]);
  delay(600);
  updateDisplay();
}

// ==================== ОБРАБОТКА НАЖАТИЯ КЛАВИШИ ====================
void handleKeyPress(char key) {
  Serial.print(currentLayer);
  Serial.print(':');
  Serial.println(key);

  lcd.setCursor(0,1);
  lcd.print("Last: L");
  lcd.print(currentLayer+1);
  lcd.print(" K");
  lcd.print(key);
}

// ==================== ОБНОВЛЕНИЕ ГЛАВНОГО ЭКРАНА ====================
void updateDisplay() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Layer: ");
  lcd.print(layerNames[currentLayer]);
  lcd.setCursor(0,1);
  lcd.print("Press a key...");
}
