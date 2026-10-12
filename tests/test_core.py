import json
import os
import sys
import tempfile

os.environ["APPDATA"] = tempfile.mkdtemp()  # ізольований конфіг для тестів
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest  # noqa: E402

from arduino_handler import ArduinoHandler  # noqa: E402
from hotkeys import parse_combo, validate_combo  # noqa: E402
from service import CONFIG_FILE, Service  # noqa: E402


def test_parse_combo():
    assert len(parse_combo("Ctrl + Shift+esc")) == 3
    assert parse_combo("c") == ["c"]


@pytest.mark.parametrize("bad", ["ctrl+foo", "ctrl+", ""])
def test_invalid_combo(bad):
    assert validate_combo(bad)


def test_config_roundtrip():
    s = Service()
    s.add_hotkey("copy", "ctrl+c")
    s.add_encoder_mode("move", "left", "right", "up", "down")
    s.assign_hotkey_to_button("BUTTON_1", "copy")
    s.assign_encoder_mode_to_button("BUTTON_2", "move")
    s.save_config()
    assert json.load(open(CONFIG_FILE, encoding="utf-8"))["hotkeys"][0]["combo"] == "ctrl+c"

    s2 = Service()
    s2.load_config()
    assert s2.get_buttons()[0].hotkey.combo == "ctrl+c"
    assert s2.get_buttons()[1].encoder_mode.name == "move"


def test_serial_protocol():
    s = Service()
    h = ArduinoHandler(s)
    h._handle_line("GLOBAL_MODE_3")
    assert s.active_profile_index == 3
    h._handle_line("MODE_V")
    assert s.encoder_alt_active is True
    h._handle_line("MODE_H")
    assert s.encoder_alt_active is False
    h._handle_line("GLOBAL_MODE_x")  # сміття не ламає обробку
