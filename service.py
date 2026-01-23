import main_data
from main_data import hotkey_combos, encoder_modes, profiles
from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode

class Service:
    def __init__(self):
        self.hotkey_combos = hotkey_combos
        self.encoder_modes = encoder_modes
        self.on_profile_change_callback = None

    # === УПРАВЛІННЯ ПРОФІЛЯМИ ===
    def set_active_profile(self, profile_num):
        if profile_num in profiles:
            main_data.active_profile_index = profile_num
            print(f"🔄 [Service] Активний профіль змінено на: {profile_num}")
            if self.on_profile_change_callback:
                self.on_profile_change_callback()

    def get_current_profile_index(self):
        return main_data.active_profile_index

    # === РОБОТА З КНОПКАМИ ===
    def get_buttons(self):
        return profiles[main_data.active_profile_index]

    def assign_hotkey_to_button(self, button_name, hotkey_name):
        current_buttons = self.get_buttons()
        btn = next((b for b in current_buttons if b.name == button_name), None)
        hk = next((hk for hk in self.hotkey_combos if hk.name == hotkey_name), None)
        
        if btn:
            btn.hotkey = hk # Призначаємо гарячу клавішу (або None)
            
            # === ВАЖЛИВО: Якщо призначили клавішу, стираємо режим енкодера ===
            if hk is not None:
                btn.encoder_mode = None

    def assign_encoder_mode_to_button(self, button_name, encoder_mode_name):
        current_buttons = self.get_buttons()
        btn = next((b for b in current_buttons if b.name == button_name), None)
        em = next((em for em in self.encoder_modes if em.name == encoder_mode_name), None)
        
        if btn:
            btn.encoder_mode = em # Призначаємо режим (або None)
            
            # === ВАЖЛИВО: Якщо призначили режим, стираємо гарячу клавішу ===
            if em is not None:
                btn.hotkey = None

    # === ГАРЯЧІ КЛАВІШІ ===
    def add_hotkey(self, name, combo):
        existing = next((hk for hk in self.hotkey_combos if hk.name == name), None)
        if existing:
            existing.combo = combo
        else:
            self.hotkey_combos.append(HotkeyCombo(name, combo))
            
    def remove_hotkey(self, hk_obj):
        if hk_obj in self.hotkey_combos:
            self.hotkey_combos.remove(hk_obj)

    def get_hotkeys(self):
        return self.hotkey_combos

    # === РЕЖИМИ ЕНКОДЕРА (ОНОВЛЕНО) ===
    def add_encoder_mode(self, name, left_cmd, right_cmd, alt_left_cmd="", alt_right_cmd=""):
        existing = next((em for em in self.encoder_modes if em.name == name), None)
        if existing:
            existing.left_cmd = left_cmd
            existing.right_cmd = right_cmd
            existing.alt_left_cmd = alt_left_cmd
            existing.alt_right_cmd = alt_right_cmd
        else:
            self.encoder_modes.append(EncoderMode(name, left_cmd, right_cmd, alt_left_cmd, alt_right_cmd))

    # НОВИЙ МЕТОД ВИДАЛЕННЯ
    def remove_encoder_mode(self, mode_obj):
        if mode_obj in self.encoder_modes:
            # 1. Видаляємо сам режим
            self.encoder_modes.remove(mode_obj)
            
            # 2. Очищаємо кнопки у ВСІХ профілях, які використовували цей режим
            for profile_buttons in profiles.values():
                for btn in profile_buttons:
                    if btn.encoder_mode == mode_obj:
                        btn.encoder_mode = None
            
            print(f"🗑️ Режим енкодера '{mode_obj.name}' видалено та відв'язано від кнопок")

    def get_encoder_modes(self):
        return self.encoder_modes