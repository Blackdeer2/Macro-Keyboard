from hotkey_combo import HotkeyCombo
from encoder_mode import EncoderMode

class ArduinoButton:
    def __init__(self, name: str, hotkey: HotkeyCombo = None, encoder_mode: EncoderMode = None):
        self.name = name
        self.hotkey = hotkey          # об’єкт HotkeyCombo або None
        self.encoder_mode = encoder_mode  # об’єкт EncoderMode або None

    def __repr__(self):
        return f"ArduinoButton(name='{self.name}', hotkey={self.hotkey}, encoder_mode={self.encoder_mode})"
