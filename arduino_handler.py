import threading
import time

import serial
import serial.tools.list_ports

from hotkeys import press_combo

BAUD = 9600
RECONNECT_DELAY = 2.0

# VID плат Arduino та поширених USB-UART клонів (CH340, CP210x, FTDI)
KNOWN_VIDS = {0x2341, 0x2A03, 0x1B4F, 0x1A86, 0x10C4, 0x0403}
KNOWN_WORDS = ("arduino", "ch340", "ch341", "usb-serial", "usb serial", "cp210", "ftdi")


def find_arduino_port():
    """Шукає порт Arduino за VID/описом; якщо не знайшов — єдиний наявний порт."""
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        text = f"{p.description} {p.manufacturer or ''}".lower()
        if p.vid in KNOWN_VIDS or any(w in text for w in KNOWN_WORDS):
            return p.device
    return ports[0].device if len(ports) == 1 else None


class ArduinoHandler:
    """Читає події з Arduino у фоновому потоці й сам перепідключається."""

    def __init__(self, service):
        self.service = service
        self.serial = None
        self.port = None
        self.on_status_change = None  # callback(connected: bool, port: str | None)
        self._stop = threading.Event()
        self._thread = None

    # --- керування ---
    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop.set()
        self._close()

    def _close(self):
        try:
            if self.serial:
                self.serial.close()
        except Exception:
            pass
        self.serial = None

    def _set_status(self, connected, port=None):
        self.port = port
        if self.on_status_change:
            try:
                self.on_status_change(connected, port)
            except Exception as e:
                print(f"⚠️ Помилка оновлення статусу: {e}")

    # --- основний цикл: підключення → читання → перепідключення ---
    def _run(self):
        while not self._stop.is_set():
            device = find_arduino_port()
            if not device:
                self._set_status(False)
                self._stop.wait(RECONNECT_DELAY)
                continue
            try:
                self.serial = serial.Serial(device, BAUD, timeout=1)
            except Exception as e:
                print(f"⚠️ Не вдалось відкрити {device}: {e}")
                self._set_status(False)
                self._stop.wait(RECONNECT_DELAY)
                continue

            print(f"🔌 Підключено: {device}")
            self._set_status(True, device)
            self._read_loop()
            self._close()
            if not self._stop.is_set():
                print("🔌 З'єднання втрачено, пробую знову...")
                self._set_status(False)
                self._stop.wait(RECONNECT_DELAY)

    def _read_loop(self):
        while not self._stop.is_set():
            try:
                line = self.serial.readline().decode(errors="ignore").strip()
            except Exception as e:
                print(f"⚠️ Помилка серійного порту: {e}")
                return
            if not line:
                continue
            try:
                self._handle_line(line)
            except Exception as e:  # одна погана команда не повинна вбивати читання
                print(f"⚠️ Помилка обробки '{line}': {e}")

    # --- обробка команд ---
    def _handle_line(self, line):
        svc = self.service
        if line.startswith("BUTTON_"):
            self.handle_button_action(line)
        elif line in ("RIGHT", "LEFT"):
            self.handle_encoder_turn(line)
        elif line in ("MODE_V", "MODE_H"):
            svc.encoder_alt_active = (line == "MODE_V")
            print(f"ℹ️ Alt режим: {line}")
        elif line.startswith("GLOBAL_MODE_"):
            try:
                svc.set_active_profile(int(line.split("_")[-1]))
            except ValueError:
                pass

    def handle_button_action(self, button_name):
        btn = next((b for b in self.service.get_buttons() if b.name == button_name), None)
        if not btn:
            return
        if btn.encoder_mode:
            self.service.current_encoder_mode_obj = btn.encoder_mode
            print(f"🔧 Режим енкодера: {btn.encoder_mode.name}")
        elif btn.hotkey:
            print(f"🎹 {btn.hotkey.combo}")
            press_combo(btn.hotkey.combo)
        else:
            print(f"⚪ {button_name} (пусто)")

    def handle_encoder_turn(self, direction):
        mode = self.service.current_encoder_mode_obj
        if not mode:
            return
        alt = self.service.encoder_alt_active
        cmd = mode.get_left_command(alt) if direction == "LEFT" else mode.get_right_command(alt)
        print(f"🔄 Енкодер {direction} → {cmd}")
        press_combo(cmd)
