import serial
import serial.tools.list_ports
import pyautogui
import subprocess
import time
import pyperclip

# ===== Автоматический поиск порта с чипом CH340 =====
def find_macropad_port():
    """Ищет последовательный порт, на котором висит устройство с CH340."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        description = port.description.lower()
        if "ch340" in description:
            return port.device
    for port in ports:
        description = port.description.lower()
        if any(key in description for key in ["usb serial", "arduino", "cp210x"]):
            return port.device
    return None

SERIAL_PORT = find_macropad_port()

if SERIAL_PORT is None:
    print("❌ Автоматически порт не найден.")
    manual = input("Введите имя порта вручную (например, COM8) или нажмите Enter для выхода: ").strip()
    if manual:
        SERIAL_PORT = manual
    else:
        print("Выход.")
        exit(1)
else:
    print(f"✅ Найден порт: {SERIAL_PORT}")

BAUD_RATE = 115200

# ===== Словарь команд =====
COMMANDS = {
    # ----- СЛОЙ 0: ГОРЯЧИЕ КЛАВИШИ -----
    (0, '1'): ['hotkey', 'ctrl', 'c'],
    (0, '2'): ['hotkey', 'ctrl', 'v'],
    (0, '3'): ['hotkey', 'ctrl', 'x'],
    (0, '4'): ['hotkey', 'ctrl', 'z'],
    (0, '5'): ['hotkey', 'ctrl', 'y'],
    (0, '6'): ['hotkey', 'ctrl', 'a'],
    (0, '7'): ['hotkey', 'ctrl', 's'],
    (0, '8'): ['hotkey', 'ctrl', 'f'],
    (0, '9'): ['hotkey', 'ctrl', 'p'],
    (0, '0'): ['hotkey', 'alt', 'tab'],
    (0, 'A'): ['hotkey', 'winleft', 'd'],
    (0, 'B'): ['hotkey', 'ctrl', 'shift', 'esc'],
    (0, 'C'): ['hotkey', 'winleft', 'e'],
    (0, 'D'): ['hotkey', 'winleft', 'r'],
    (0, '*'): ['hotkey', 'winleft', 'l'],
    (0, '#'): ['hotkey', 'alt', 'f4'],

    # ----- СЛОЙ 1: ПРОГРАММЫ -----
    (1, '1'): ['launch', r'C:\Users\Admin\Downloads\tportable-x64.6.0.2\Telegram\Telegram.exe'], 
    (1, '2'): ['launch', r'C:\Users\Admin\AppData\Local\Discord\Update.exe', '--processStart', 'Discord.exe'], 
    (1, '3'): ['launch', r'C:\Program Files\Yandex\YandexBrowser\Application\browser.exe', '--profile-directory=Default'], 
    (1, '4'): ['launch', 'calc'], 
    (1, '5'): ['launch', 'cmd'], 
    (1, '6'): ['launch', 'cmd'],
    (1, '7'): ['launch', r'C:\Users\Admin\AppData\Local\Programs\Obsidian\Obsidian.exe'], 
    (1, '8'): ['launch', 'notepad'], 
    (1, '9'): ['launch', 'code'],
    (1, '0'): ['launch', 'taskmgr'],
    (1, 'A'): ['launch', 'control'],
    (1, 'B'): ['launch', 'ms-settings:'],
    (1, 'C'): ['launch', r'C:\Users\Admin\AppData\Local\Programs\YandexMusic\Яндекс Музыка.exe'], 
    (1, 'D'): ['launch', 'vlc'],
    (1, '*'): ['launch', r'C:\Program Files (x86)\Steam\Steam.exe'], #
    (1, '#'): ['launch', 'powershell'], 

    # ----- СЛОЙ 2: ТЕКСТ -----
    (2, '1'): ['text', 'С уважением, Александр'],
    (2, '2'): ['text', 'Celestia@neko2.net'],
    (2, '3'): ['text', 'S****@gmail.com'],
    (2, '4'): ['text', 'My card: https://bittersweetchoco.github.io/businessCard/'],
    (2, '5'): ['text', 'My GitHub: https://github.com/BitterSweetChoco'],
    (2, '6'): ['text', '+7 996 ****'],
    (2, '7'): ['text', '+7 991 ****'],
    (2, '8'): ['text', 'https://github.com'],
    (2, '9'): ['text', 'Скинь ссылку'],
    (2, '0'): ['text', 'Я пока занят, отвечу позже'],
    (2, 'A'): ['text', 'T.me/Psychopoplovok'],
    (2, 'B'): ['text', 'T.me/TeaAndSarcasm'],
    (2, 'C'): ['text', 'Благодарю'],
    (2, 'D'): ['text', 'Нет, не срочно'],
    (2, '*'): ['text', 'Срочно!'],
    (2, '#'): ['text', 'if __name__ == "__main__":'],

    # ----- СЛОЙ 3: СИСТЕМА / СКРИПТЫ -----
    (3, '1'): ['system', 'shutdown /s /t 60'],
    (3, '2'): ['system', 'shutdown /r /t 0'],
    (3, '3'): ['hotkey', 'alt', 'shift'], # Переключение языка
    (3, '4'): ['system', 'explorer shell:Downloads'], # Открыть папку «Загрузки»
    (3, '5'): ['system', 'explorer shell:Personal'], # Открыть «Документы»
    (3, '6'): ['hotkey', 'winleft', 'l'], # Блокировка экрана
    (3, '7'): ['hotkey', 'winleft', 'printscreen'],
    (3, '8'): ['script', 'powershell Start-Process powershell -Verb RunAs'], # Открыть PowerShell от имени администратора
    (3, '9'): ['system', 'ms-settings:network-wifi'], # Открыть настройки Wi-Fi
    (3, '0'): ['system', 'ms-settings:bluetooth'], # Открыть настройки Bluetooth
    (3, 'A'): ['system', 'PowerShell Clear-RecycleBin -Force'], # Очистить корзину
    (3, 'B'): ['system', 'mspaint'],
    (3, 'C'): ['system', 'write'],
    (3, 'D'): ['volume', 'mute'],
    (3, '*'): ['system', 'cleanmgr'],
    (3, '#'): ['system', 'dxdiag'],

    # ----- ДЖОЙСТИК (МУЛЬТИМЕДИА) -----
    ('J', 'UP'):     ['media', 'volumeup'],
    ('J', 'DOWN'):   ['media', 'volumedown'],
    ('J', 'LEFT'):   ['media', 'prevtrack'],
    ('J', 'RIGHT'):  ['media', 'nexttrack'],
}

def execute_command(command_type, args):
    """Выполняет команду. Для Win-комбинаций используется ручная эмуляция с паузой."""
    if command_type == 'hotkey':
        if args[0].startswith('win'):
            pyautogui.keyDown(args[0])
            time.sleep(0.05)
            for key in args[1:]:
                pyautogui.press(key)
                time.sleep(0.05)
            pyautogui.keyUp(args[0])
        else:
            pyautogui.hotkey(*args)
    elif command_type == 'launch':
        try:
            subprocess.Popen(args, shell=True)
        except Exception as e:
            print(f"Ошибка запуска: {e}")
    elif command_type == 'text':
        # Копируем текст в буфер обмена
        pyperclip.copy(args[0])
        time.sleep(0.2)  # Даём буферу обмена время обновиться

        # Пытаемся вставить через Ctrl+V
        try:
            pyautogui.hotkey('ctrl', 'v')
        except Exception as e:
            print(f"Ошибка вставки через Ctrl+V: {e}, пробуем typewrite...")
            # Если не работает, используем медленный набор текста
            pyautogui.typewrite(args[0], interval=0.02)

    elif command_type == 'system':
        subprocess.Popen(args[0], shell=True)
    elif command_type == 'script':
        subprocess.Popen(args[0], shell=True)
    elif command_type == 'volume':
        action = args[0]
        if action == 'up':
            pyautogui.press('volumeup')
        elif action == 'down':
            pyautogui.press('volumedown')
        elif action == 'mute':
            pyautogui.press('volumemute')
    elif command_type == 'media':
        action = args[0]
        if action == 'prevtrack':
            pyautogui.press('prevtrack')
        elif action == 'nexttrack':
            pyautogui.press('nexttrack')
        elif action == 'volumeup':
            pyautogui.press('volumeup')
        elif action == 'volumedown':
            pyautogui.press('volumedown')
        elif action == 'playpause':
            pyautogui.press('playpause')

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Слушаю порт {SERIAL_PORT}...")
        time.sleep(2)
        ser.reset_input_buffer()

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if not line:
                continue
            print(f"Получено: {line}")

            # Игнорируем служебные сообщения (без двоеточия, типа "Ready")
            if ':' not in line:
                print(f"Игнорируем служебное сообщение: {line}")
                continue

            try:
                layer_str, key = line.split(':', 1)
                layer = int(layer_str) if layer_str != 'J' else layer_str
                if (layer, key) in COMMANDS:
                    cmd = COMMANDS[(layer, key)]
                    execute_command(cmd[0], cmd[1:])
                    print(f"Выполнено: {cmd}")
                else:
                    print(f"Нет действия для L{layer} K{key}")
            except Exception as e:
                print(f"Ошибка разбора: {e}")

    except serial.SerialException as e:
        print(f"Ошибка последовательного порта: {e}")
    except KeyboardInterrupt:
        print("Выход по запросу пользователя")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print("Порт закрыт.")

if __name__ == '__main__':
    main()
