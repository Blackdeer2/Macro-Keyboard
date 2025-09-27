from pynput.keyboard import Controller, Key

keyboard = Controller()

class Service:
    def __init__(self, arduino_buttons, hotkey_combos, encoder_modes):
        self.arduino_buttons = arduino_buttons
        self.hotkey_combos = hotkey_combos
        self.encoder_modes = encoder_modes
        self.subscribers = []  # UI-підписники на оновлення

    # ----------------- Підписка UI -----------------
    def subscribe(self, callback):
        """Додає функцію, яку потрібно викликати при зміні даних"""
        self.subscribers.append(callback)

    def notify(self):
        """Оповіщає підписників про зміни"""
        for callback in self.subscribers:
            callback()

    # ----------------- Гарячі клавіші -----------------
    def add_hotkey(self, name, combo):
        existing = next((hk for hk in self.hotkey_combos if hk.name == name), None)
        if existing:
            existing.combo = combo
        else:
            from main_data import HotkeyCombo
            self.hotkey_combos.append(HotkeyCombo(name, combo))
        self.notify()  # повідомляємо UI

    # ----------------- Режими енкодера -----------------
    def add_encoder_mode(self, name, left_cmd, right_cmd, alt_left_cmd="", alt_right_cmd=""):
        existing = next((em for em in self.encoder_modes if em.name == name), None)
        if existing:
            existing.left_cmd = left_cmd
            existing.right_cmd = right_cmd
            existing.alt_left_cmd = alt_left_cmd
            existing.alt_right_cmd = alt_right_cmd
        else:
            from main_data import EncoderMode
            self.encoder_modes.append(EncoderMode(name, left_cmd, right_cmd, alt_left_cmd, alt_right_cmd))
        self.notify()

    # ----------------- Призначення для кнопки -----------------
    def assign_hotkey_to_button(self, button_name, hotkey_name):
        btn = next((b for b in self.arduino_buttons if b.name == button_name), None)
        hk = next((hk for hk in self.hotkey_combos if hk.name == hotkey_name), None)
        if btn:
            btn.hotkey = hk
        self.notify()

    def assign_encoder_mode_to_button(self, button_name, encoder_mode_name):
        btn = next((b for b in self.arduino_buttons if b.name == button_name), None)
        em = next((em for em in self.encoder_modes if em.name == encoder_mode_name), None)
        if btn:
            btn.encoder_mode = em
        self.notify()

    # ----------------- Виконання команди -----------------
    def execute_button(self, button_name, encoder_direction=None, alt_mode=False):
        btn = next((b for b in self.arduino_buttons if b.name == button_name), None)
        if not btn:
            return

        if btn.hotkey:
            self.press_combo(btn.hotkey.combo)
            return

        if btn.encoder_mode and encoder_direction:
            em = btn.encoder_mode
            cmd = None
            if alt_mode:
                cmd = em.alt_left_cmd if encoder_direction == "left" else em.alt_right_cmd
            else:
                cmd = em.left_cmd if encoder_direction == "left" else em.right_cmd
            if cmd:
                self.press_combo(cmd)

    # ----------------- Допоміжна функція натискання -----------------
    def press_combo(self, combo: str):
        parts = combo.lower().split("+")
        keys = []
        for p in parts:
            if hasattr(Key, p):
                keys.append(getattr(Key, p))
            else:
                keys.append(p)
        for k in keys:
            keyboard.press(k)
        for k in reversed(keys):
            keyboard.release(k)
