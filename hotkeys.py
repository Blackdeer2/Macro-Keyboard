from pynput.keyboard import Controller, Key

keyboard = Controller()

# Зручні назви → клавіші pynput
ALIASES = {
    "control": Key.ctrl, "win": Key.cmd, "windows": Key.cmd, "super": Key.cmd,
    "return": Key.enter, "escape": Key.esc, "del": Key.delete,
    "pgup": Key.page_up, "pgdn": Key.page_down,
    "vol_up": Key.media_volume_up, "vol_down": Key.media_volume_down,
    "mute": Key.media_volume_mute, "next": Key.media_next,
    "prev": Key.media_previous, "play": Key.media_play_pause,
    "playpause": Key.media_play_pause,
}


def parse_combo(combo: str):
    """'Ctrl + C' -> [Key.ctrl, 'c']. Кидає ValueError для невідомої клавіші."""
    keys = []
    for part in combo.lower().split("+"):
        part = part.strip()
        if not part:
            raise ValueError(f"порожня клавіша в '{combo}'")
        if part in ALIASES:
            keys.append(ALIASES[part])
        elif part in Key.__members__:
            keys.append(Key[part])
        elif len(part) == 1:
            keys.append(part)
        else:
            raise ValueError(f"невідома клавіша '{part}'")
    return keys


def validate_combo(combo: str):
    """Повертає None якщо комбінація коректна, інакше текст помилки."""
    try:
        parse_combo(combo)
        return None
    except ValueError as e:
        return str(e)


def press_combo(combo: str):
    if not combo:
        return
    try:
        keys = parse_combo(combo)
    except ValueError as e:
        print(f"⚠️ Некоректна комбінація: {e}")
        return
    pressed = []
    try:
        for k in keys:
            keyboard.press(k)
            pressed.append(k)
    except Exception as e:
        print(f"⚠️ Помилка натискання '{combo}': {e}")
    finally:
        for k in reversed(pressed):
            try:
                keyboard.release(k)
            except Exception:
                pass
