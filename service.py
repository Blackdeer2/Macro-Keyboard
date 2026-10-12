import json
import os
import shutil
import sys
from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode
from arduino_button import ArduinoButton

def _config_path():
    """Конфіг лежить у %APPDATA%/MacroKey (Windows) і не залежить від теки запуску."""
    base = os.environ.get("APPDATA") or os.path.join(os.path.expanduser("~"), ".config")
    folder = os.path.join(base, "MacroKey")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "config.json")
    if not os.path.exists(path):  # перенос старого конфігу поруч із програмою
        here = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
        old = os.path.join(here, "config.json")
        if os.path.exists(old):
            shutil.copy(old, path)
    return path

CONFIG_FILE = _config_path()

class Service:
    def __init__(self):
        # --- ДАНІ (раніше були в main_data.py) ---
        self.hotkey_combos = []
        self.encoder_modes = []
        self.active_profile_index = 1
        self.on_profile_change_callback = None
        
        # Ініціалізація пустих профілів
        self.profiles = {
            1: [ArduinoButton(name=f"BUTTON_{i}") for i in range(1, 10)],
            2: [ArduinoButton(name=f"BUTTON_{i}") for i in range(1, 10)],
            3: [ArduinoButton(name=f"BUTTON_{i}") for i in range(1, 10)]
        }
        
        # Для передачі стану енкодера в ArduinoHandler (раніше active_encoder_ref)
        self.current_encoder_mode_obj = None
        self.encoder_alt_active = False  # MODE_V / MODE_H від Arduino
        self.refresh_buttons_dropdowns = lambda: None  # підміняється вкладкою кнопок

    # === КОНФІГУРАЦІЯ (раніше config_manager.py) ===
    def load_config(self):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content: return
                data = json.loads(content)

            # 1. Завантажуємо довідники
            self.hotkey_combos.clear()
            for hk in data.get("hotkeys", []):
                self.hotkey_combos.append(HotkeyCombo(hk["name"], hk["combo"]))

            self.encoder_modes.clear()
            for em in data.get("encoder_modes", []):
                self.encoder_modes.append(EncoderMode(
                    em["name"], em.get("left_cmd", ""), em.get("right_cmd", ""), 
                    em.get("alt_left_cmd", ""), em.get("alt_right_cmd", "")
                ))

            # 2. Завантажуємо ПРОФІЛІ
            saved_profiles = data.get("profiles", {})
            for pid_str, buttons_data in saved_profiles.items():
                pid = int(pid_str)
                if pid in self.profiles:
                    target_list = self.profiles[pid]
                    # Синхронізуємо кнопки за іменами
                    for btn in target_list:
                        btn_data = next((b for b in buttons_data if b["name"] == btn.name), None)
                        if btn_data:
                            # Шукаємо об'єкти за іменами
                            btn.hotkey = next((hk for hk in self.hotkey_combos if hk.name == btn_data.get("hotkey")), None)
                            btn.encoder_mode = next((em for em in self.encoder_modes if em.name == btn_data.get("encoder_mode")), None)
            
            last = data.get("last_active_profile", 1)
            self.active_profile_index = last if last in self.profiles else 1
            print("✅ Конфігурація завантажена")
        except FileNotFoundError:
            print("ℹ️ Файл конфігурації не знайдено, створено новий.")
        except Exception as e:
            print(f"⚠️ Помилка завантаження: {e}")

    def save_config(self):
        # Формуємо JSON структуру
        profiles_data = {}
        for pid, buttons_list in self.profiles.items():
            profiles_data[str(pid)] = [
                {
                    "name": btn.name,
                    "hotkey": btn.hotkey.name if btn.hotkey else None,
                    "encoder_mode": btn.encoder_mode.name if btn.encoder_mode else None
                }
                for btn in buttons_list
            ]

        data = {
            "hotkeys": [{"name": hk.name, "combo": hk.combo} for hk in self.hotkey_combos],
            "encoder_modes": [
                {
                    "name": em.name,
                    "left_cmd": em.left_cmd,
                    "right_cmd": em.right_cmd,
                    "alt_left_cmd": em.alt_left_cmd,
                    "alt_right_cmd": em.alt_right_cmd
                } for em in self.encoder_modes
            ],
            "profiles": profiles_data,
            "last_active_profile": self.active_profile_index
        }
        
        try:
            tmp = CONFIG_FILE + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            os.replace(tmp, CONFIG_FILE)  # атомарно: не втратимо конфіг при збої
            print("💾 Конфігурація збережена")
        except Exception as e:
            print(f"❌ Помилка збереження: {e}")

    # === ЛОГІКА ===
    def get_buttons(self):
        return self.profiles[self.active_profile_index]

    def set_active_profile(self, profile_num):
        if profile_num in self.profiles:
            self.active_profile_index = profile_num
            print(f"🔄 [Service] Активний профіль: {profile_num}")
            if self.on_profile_change_callback:
                self.on_profile_change_callback()

    def get_current_profile_index(self):
        return self.active_profile_index

    def assign_hotkey_to_button(self, button_name, hotkey_name):
        btn = next((b for b in self.get_buttons() if b.name == button_name), None)
        hk = next((hk for hk in self.hotkey_combos if hk.name == hotkey_name), None)
        if btn:
            btn.hotkey = hk
            if hk: btn.encoder_mode = None # Очищаємо конфлікт

    def assign_encoder_mode_to_button(self, button_name, encoder_mode_name):
        btn = next((b for b in self.get_buttons() if b.name == button_name), None)
        em = next((em for em in self.encoder_modes if em.name == encoder_mode_name), None)
        if btn:
            btn.encoder_mode = em
            if em: btn.hotkey = None # Очищаємо конфлікт

    # === CRUD Методи для списків ===
    def get_hotkeys(self): return self.hotkey_combos
    def get_encoder_modes(self): return self.encoder_modes

    def add_hotkey(self, name, combo):
        # Якщо вже є - оновлюємо
        existing = next((hk for hk in self.hotkey_combos if hk.name == name), None)
        if existing: existing.combo = combo
        else: self.hotkey_combos.append(HotkeyCombo(name, combo))

    def remove_hotkey(self, hk_obj):
        if hk_obj in self.hotkey_combos:
            self.hotkey_combos.remove(hk_obj)
            # Очистити використання у кнопках
            for prof in self.profiles.values():
                for btn in prof:
                    if btn.hotkey == hk_obj: btn.hotkey = None

    def add_encoder_mode(self, name, l, r, al, ar):
        existing = next((em for em in self.encoder_modes if em.name == name), None)
        if existing:
            existing.left_cmd = l
            existing.right_cmd = r
            existing.alt_left_cmd = al
            existing.alt_right_cmd = ar
        else:
            self.encoder_modes.append(EncoderMode(name, l, r, al, ar))

    def remove_encoder_mode(self, mode_obj):
        if mode_obj in self.encoder_modes:
            self.encoder_modes.remove(mode_obj)
            if self.current_encoder_mode_obj is mode_obj:
                self.current_encoder_mode_obj = None
            for prof in self.profiles.values():
                for btn in prof:
                    if btn.encoder_mode == mode_obj: btn.encoder_mode = None