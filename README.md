# MacroPad – Custom Programmable Keypad with LCD and Joystick

**MacroPad** is a compact, fully programmable macropad built around Arduino Uno. It features 16 tactile keys, an analog joystick with a button, and a 16x2 I2C LCD display. The firmware sends layer/key events over serial, and a Python companion script executes commands on the host PC: hotkeys, text snippets, application launchers, system controls, and more.

The project is ideal for beginners in embedded development, covering GPIO, I2C, ADC, finite state machines, and serial communication with a PC.

## Features
- **4 switchable layers** (Edit, Apps, Text, System) – 64 programmable actions
- **Layer switching** via joystick button press (with on-screen notification)
- **16 membrane keys** per layer
- **Analog joystick** (future menu navigation support)
- **Python host script** for executing:
  - Global hotkeys (Ctrl+C, Win+D, Alt+Tab, etc.)
  - Launching applications by path or name
  - Inserting pre-defined text (email, signature, code templates)
  - System commands (shutdown, reboot, volume control, custom scripts)
- **LCD 1602 I2C** display showing current layer and last action
- **Modular design** – easy to expand and customize

## Hardware Requirements
- Arduino Uno R3
- LCD 1602 with I2C module (address 0x27 or 0x3F)
- 4x4 membrane keypad
- Analog joystick (KY-023 or similar)
- Wires, breadboard or custom PCB
- (Optional) Enclosure

### Wiring
| Keypad | Arduino Pin |
|--------|-------------|
| R1     | 2           |
| R2     | 3           |
| R3     | 4           |
| R4     | 5           |
| C1     | 6           |
| C2     | 7           |
| C3     | 8           |
| C4     | 9           |

| Joystick | Arduino Pin |
|----------|-------------|
| GND      | GND         |
| +5V      | 5V          |
| VRx      | A0          |
| VRy      | A1          |
| SW       | 10          |

| LCD I2C | Arduino Pin |
|---------|-------------|
| GND     | GND         |
| VCC     | 5V          |
| SDA     | A4          |
| SCL     | A5          |

## Firmware (PlatformIO)
The firmware is written in C++ using Arduino framework. It scans the keyboard matrix, reads joystick button with debouncing, and sends layer:key messages over Serial (115200 baud). A simple state machine manages layer switching and display updates.

### Build & Upload
1. Clone this repository
2. Open `firmware/` in PlatformIO
3. Adjust `I2C_ADDR` if needed (0x27 or 0x3F)
4. Build and upload to Arduino Uno
5. The LCD will show "Macropad Ready" and current layer

## Host Script (Python)
The Python script (`software/macro_server.py`) listens on the specified COM port and interprets incoming commands. It uses `pyautogui`, `pyperclip`, and `subprocess` to execute actions.

### Requirements
- Python 3.7+
- Install dependencies: `pip install pyserial pyautogui pyperclip`

### Usage
1. Edit `SERIAL_PORT` to match your Arduino's port (e.g., `COM7` on Windows)
2. Run: `python macro_server.py`
3. Press keys on the macropad – commands will execute on the PC

### Customizing Commands
All mappings are defined in the `COMMANDS` dictionary. Each entry uses the format:
`(layer, key): [action_type, arg1, arg2, ...]`

Examples:
- `(0, '1'): ['hotkey', 'ctrl', 'c']`
- `(1, '1'): ['launch', 'C:\\path\\to\\Telegram.exe']`
- `(2, '1'): ['text', 'Best regards, Alex']`
- `(3, '1'): ['system', 'shutdown /s /t 0']`

## Future Improvements
- On-screen menu navigation using joystick axes
- EEPROM storage of last active layer
- Native USB HID support with ATmega32U4 board (Pro Micro)
- GUI configuration tool

## License
This project is licensed under the MIT License – feel free to use, modify, and share.

---

# MacroPad – Программируемый макропад с дисплеем и джойстиком

**MacroPad** – компактный программируемый макропад на базе Arduino Uno. Включает 16 кнопок мембранной клавиатуры, аналоговый джойстик с кнопкой и LCD-дисплей 16×2 с I2C интерфейсом. Прошивка передаёт события слоёв и клавиш через Serial, а Python-скрипт на ПК выполняет действия: горячие клавиши, текстовые вставки, запуск приложений, системные команды и многое другое.

Проект отлично подходит новичкам для изучения GPIO, I2C, АЦП, конечных автоматов и взаимодействия микроконтроллера с компьютером.

## Возможности
- **4 переключаемых слоя** (Горячие клавиши, Программы, Текст, Система) – 64 программируемых действия
- **Переключение слоёв** кнопкой джойстика с уведомлением на дисплее
- **16 мембранных кнопок** в каждом слое
- **Аналоговый джойстик** (в будущем — навигация по меню)
- **Python-скрипт** для выполнения команд:
  - Глобальные сочетания клавиш (Ctrl+C, Win+D, Alt+Tab и др.)
  - Запуск приложений по имени или полному пути
  - Вставка заготовленного текста (email, подпись, шаблоны кода)
  - Системные команды (выключение, перезагрузка, управление громкостью, скрипты)
- **LCD 1602 I2C** отображает текущий слой и последнее действие
- **Модульная архитектура** – легко расширяется под свои нужды

## Аппаратное обеспечение
- Arduino Uno R3
- LCD 1602 с модулем I2C (адрес 0x27 или 0x3F)
- Мембранная клавиатура 4×4
- Аналоговый джойстик (KY-023 или аналог)
- Соединительные провода, макетная плата или печатная плата
- (Опционально) Корпус

### Схема подключения
См. таблицы в английской версии.

## Прошивка (PlatformIO)
Прошивка написана на C++ с использованием Arduino framework. Она опрашивает клавиатурную матрицу, считывает кнопку джойстика с подавлением дребезга и отправляет сообщения вида `слой:клавиша` через Serial (115200 бод). Простой конечный автомат управляет слоями и обновлением дисплея.

### Сборка и загрузка
1. Клонируйте репозиторий
2. Откройте папку `firmware/` в PlatformIO
3. При необходимости измените `I2C_ADDR` в `main.cpp`
4. Скомпилируйте и загрузите в Arduino Uno
5. На дисплее появится приветствие "Macropad Ready"

## Хост-скрипт (Python)
Python-скрипт (`software/macro_server.py`) слушает указанный COM-порт и исполняет полученные команды. Для работы используются библиотеки `pyautogui`, `pyperclip`, `subprocess`.

### Требования
- Python 3.7+
- Установите зависимости: `pip install pyserial pyautogui pyperclip`

### Запуск
1. Укажите правильный последовательный порт в переменной `SERIAL_PORT` (например, `COM7`)
2. Запустите: `python macro_server.py`
3. Нажимайте кнопки на макропаде – команды будут выполняться на ПК

### Настройка команд
Все соответствия задаются в словаре `COMMANDS`. Формат записи:
`(слой, клавиша): [тип_команды, аргументы...]`

Примеры:
- `(0, '1'): ['hotkey', 'ctrl', 'c']`
- `(1, '1'): ['launch', 'C:\\путь\\к\\Telegram.exe']`
- `(2, '1'): ['text', 'С уважением, Александр']`
- `(3, '1'): ['system', 'shutdown /s /t 0']`

## Планы по развитию
- Экранное меню с навигацией джойстиком
- Сохранение активного слоя в EEPROM
- Поддержка нативного USB HID (плата на ATmega32U4, например Pro Micro)
- Графический конфигуратор

## Лицензия
Проект распространяется под лицензией MIT – используйте, модифицируйте, делитесь.
