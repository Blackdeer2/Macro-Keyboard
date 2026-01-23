import serial, serial.tools.list_ports, threading
from hotkeys import press_combo

class ArduinoHandler:
    def __init__(self, service):
        self.arduino = None
        self.service = service 

    def connect(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("❌ COM-порти не знайдено")
            return None
        
        try:
            self.arduino = serial.Serial(ports[0].device, 9600, timeout=1)
            threading.Thread(target=self.read_loop, daemon=True).start()
            return ports[0].device
        except Exception as e:
            print(f"⚠️ Помилка підключення: {e}")
            return None

    def handle_button_action(self, button_name):
        # Знаходимо кнопку в поточному профілі сервісу
        buttons = self.service.get_buttons()
        btn = next((b for b in buttons if b.name == button_name), None)
        
        if not btn: return

        if btn.encoder_mode:
            # Активуємо режим енкодера в сервісі
            self.service.current_encoder_mode_obj = btn.encoder_mode
            print(f"🔧 Активовано режим енкодера: {btn.encoder_mode.name}")
        elif btn.hotkey:
            print(f"🎹 Натискання: {btn.hotkey.combo}")
            press_combo(btn.hotkey.combo)
        else:
            print(f"⚪ {button_name} (пусто)")

    def handle_encoder_turn(self, direction):
        mode = self.service.current_encoder_mode_obj
        if mode:
            cmd = mode.get_left_command() if direction == "LEFT" else mode.get_right_command()
            print(f"🔄 Енкодер {direction} → {cmd}")
            press_combo(cmd)

    def read_loop(self):
        while self.arduino:
            try:
                if not self.arduino.is_open: break
                line = self.arduino.readline().decode(errors="ignore").strip()
                if not line: continue

                if line.startswith("BUTTON_"):
                    self.handle_button_action(line)
                
                elif line in ["RIGHT", "LEFT"]:
                    self.handle_encoder_turn(line)
                
                elif line in ["MODE_V", "MODE_H"]:
                    # Зміна під-режиму (Alt) у поточному об'єкті
                    curr_mode = self.service.current_encoder_mode_obj
                    if curr_mode:
                        curr_mode.alt_active = (line == "MODE_V")
                        print(f"ℹ️ Alt режим: {line}")
                
                elif line.startswith("GLOBAL_MODE_"):
                    try:
                        self.service.set_active_profile(int(line.split("_")[-1]))
                    except ValueError: pass

            except Exception as e:
                print(f"⚠️ Помилка серійного порту: {e}")
                break