import serial, serial.tools.list_ports, threading

class ArduinoHandler:
    def __init__(self, callback):
        self.arduino = None
        self.callback = callback

    def find_port(self):
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("❌ COM-порти не знайдено")
            return None

        print("🔍 Знайдені COM-порти:")
        for port in ports:
            print(f"  {port.device}: {port.description}")

        # Автовибір першого порту (можна змінити логіку)
        return ports[0].device

    def connect(self):
        port = self.find_port()
        if port:
            try:
                self.arduino = serial.Serial(port, 9600, timeout=1)
                threading.Thread(target=self.read_loop, daemon=True).start()
                return port
            except Exception as e:
                print(f"⚠️ Помилка підключення до {port}: {e}")
                return None
        return None

    def read_loop(self):
        while self.arduino:
            try:
                line = self.arduino.readline().decode(errors="ignore").strip()
                if line:
                    self.callback(line)
            except Exception as e:
                print("⚠️ Помилка читання:", e)
                break

    def close(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None
