import serial, serial.tools.list_ports, threading
from hotkeys import press_combo

class ArduinoHandler:
    def __init__(self, callback, active_encoder_ref, service):
        self.arduino = None
        self.callback = callback
        self.active_encoder_ref = active_encoder_ref
        self.service = service # Посилання на Service для перемикання профілів

    def find_port(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("❌ COM-порти не знайдено")
            return None
        return ports[0].device

    def connect(self):
        port = self.find_port()
        if port:
            try:
                self.arduino = serial.Serial(port, 9600, timeout=1)
                threading.Thread(target=self.read_loop, daemon=True).start()
                return port
            except Exception as e:
                print(f"⚠️ Помилка: {e}")
        return None
    
    def handle_encoder_turn(self, direction):
        mode = self.active_encoder_ref["mode"]
        if mode:
            cmd = mode.get_left_command() if direction == "LEFT" else mode.get_right_command()
            print(f"[Arduino] Енкодер {direction} → {cmd}")
            press_combo(cmd)

    def read_loop(self):
        while self.arduino:
            try:
                line = self.arduino.readline().decode(errors="ignore").strip()
                if line:
                    if line.startswith("BUTTON_"):
                        self.callback(line) # Натискання кнопки
                    elif line in ["RIGHT", "LEFT"]:
                        self.handle_encoder_turn(line)
                    elif line in ["MODE_V", "MODE_H"]:
                        # Зміна під-режиму енкодера
                        if self.active_encoder_ref["mode"]:
                            self.active_encoder_ref["mode"].alt_active = (line == "MODE_V")
                            print(f"ℹ️ Режим енкодера: {line}")
                    
                    # === НОВЕ: Обробка глобальних профілів ===
                    elif line.startswith("GLOBAL_MODE_"):
                        try:
                            # Отримуємо цифру (1, 2 або 3)
                            new_mode = int(line.split("_")[-1])
                            self.service.set_active_profile(new_mode)
                        except ValueError:
                            pass

            except Exception as e:
                print("⚠️ Помилка читання:", e)
                break