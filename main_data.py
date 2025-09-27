# main_data.py
from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode
from arduino_button import ArduinoButton

hotkey_combos = [
    # HotkeyCombo(name="Copy", combo="ctrl+c"),
    # HotkeyCombo(name="Paste", combo="ctrl+v"),
    # HotkeyCombo(name="Undo", combo="ctrl+z"),
    # HotkeyCombo(name="Redo", combo="ctrl+y"),
]

encoder_modes = [
    # EncoderMode(name="ScrollMode", left_cmd="up", right_cmd="down"),
    # EncoderMode(name="VolumeMode", left_cmd="volume_down", right_cmd="volume_up"),
    # EncoderMode(name="ShiftMode", left_cmd="shift+left", right_cmd="shift+right"),
]

arduino_buttons = []
for i in range(1, 10):
    btn_name = f"BUTTON_{i}"
    # На старті кнопки не мають призначеної гарячої клавіші чи режиму
    btn = ArduinoButton(name=btn_name, hotkey=None, encoder_mode=None)
    arduino_buttons.append(btn)