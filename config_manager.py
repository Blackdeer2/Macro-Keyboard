import json
import main_data
from main_data import hotkey_combos, encoder_modes, profiles
from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode

CONFIG_FILE = "config.json"

def save_config():
    # 1. Формуємо дані профілів
    profiles_data = {}
    for pid, buttons_list in profiles.items():
        profiles_data[str(pid)] = [
            {
                "name": btn.name,
                "hotkey": btn.hotkey.name if btn.hotkey else None,
                "encoder_mode": btn.encoder_mode.name if btn.encoder_mode else None
            }
            for btn in buttons_list
        ]

    # 2. Збираємо все разом
    data = {
        "hotkeys": [{"name": hk.name, "combo": hk.combo} for hk in hotkey_combos],
        "encoder_modes": [
            {
                "name": em.name,
                "left_cmd": em.left_cmd,
                "right_cmd": em.right_cmd,
                "alt_left_cmd": em.alt_left_cmd,
                "alt_right_cmd": em.alt_right_cmd
            }
            for em in encoder_modes
        ],
        "profiles": profiles_data,
        "last_active_profile": main_data.active_profile_index
    }
    
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)
    print("💾 Конфігурація збережена")

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            content = f.read().strip()
            if not content: return
            data = json.loads(content)

        # 1. Завантажуємо довідники
        hotkey_combos.clear()
        for hk in data.get("hotkeys", []):
            hotkey_combos.append(HotkeyCombo(hk["name"], hk["combo"]))

        encoder_modes.clear()
        for em in data.get("encoder_modes", []):
            encoder_modes.append(
                EncoderMode(em["name"], em.get("left_cmd", ""), em.get("right_cmd", ""), 
                            em.get("alt_left_cmd", ""), em.get("alt_right_cmd", ""))
            )

        # 2. Завантажуємо ПРОФІЛІ
        saved_profiles = data.get("profiles", {})
        for pid_str, buttons_data in saved_profiles.items():
            pid = int(pid_str)
            if pid in profiles:
                target_list = profiles[pid]
                for btn in target_list:
                    btn_data = next((b for b in buttons_data if b["name"] == btn.name), None)
                    if btn_data:
                        btn.hotkey = next((hk for hk in hotkey_combos if hk.name == btn_data["hotkey"]), None)
                        btn.encoder_mode = next((em for em in encoder_modes if em.name == btn_data["encoder_mode"]), None)
        
        # 3. Відновлюємо останній активний профіль
        main_data.active_profile_index = data.get("last_active_profile", 1)

        print("✅ Конфігурація завантажена")
    except Exception as e:
        print(f"⚠️ Помилка завантаження: {e}")