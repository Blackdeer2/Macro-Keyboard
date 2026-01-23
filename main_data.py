from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode
from arduino_button import ArduinoButton

hotkey_combos = []
encoder_modes = []

# Зберігаємо активний режим енкодера
active_encoder_mode = {"mode": None}

# === НОВЕ: СТРУКТУРА ПРОФІЛІВ ===
# Створюємо 3 окремі списки кнопок (для кожного режиму світлодіода)
profiles = {
    1: [ArduinoButton(name=f"BUTTON_{i}", hotkey=None, encoder_mode=None) for i in range(1, 10)],
    2: [ArduinoButton(name=f"BUTTON_{i}", hotkey=None, encoder_mode=None) for i in range(1, 10)],
    3: [ArduinoButton(name=f"BUTTON_{i}", hotkey=None, encoder_mode=None) for i in range(1, 10)]
}

# Змінна, яка пам'ятає, який профіль зараз активний (1, 2 або 3)
active_profile_index = 1