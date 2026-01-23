from pynput.keyboard import Controller, Key
keyboard = Controller()

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
