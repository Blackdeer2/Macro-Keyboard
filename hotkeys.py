from pynput.keyboard import Controller, Key

keyboard = Controller()

# Тут призначаємо гарячі клавіші для кнопок Arduino
button_mapping = {
    "BUTTON_1": "a",
    "BUTTON_2": "b",
    "BUTTON_3": "c",
    "BUTTON_4": "ctrl+alt+m",
}

def press_combo(combo: str):
    parts = combo.lower().split("+")
    keys = []
    for p in parts:
        if hasattr(Key, p):
            keys.append(getattr(Key, p))
        else:
            keys.append(p)
    # натискання
    for k in keys:
        keyboard.press(k)
    for k in reversed(keys):
        keyboard.release(k)
