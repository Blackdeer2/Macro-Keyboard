class HotkeyCombo:
    def __init__(self, name: str, combo: str):
        self.name = name
        self.combo = combo

    def __repr__(self):
        return f"HotkeyCombo(name='{self.name}', combo='{self.combo}')"
