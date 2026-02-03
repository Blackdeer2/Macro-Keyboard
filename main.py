import flet as ft
import atexit
import threading
import pystray
from PIL import Image, ImageDraw

from service import Service
from arduino_handler import ArduinoHandler
from tab_buttons import create_buttons_tab
from tab_hotkeys import create_hotkeys_tab
from tab_encoder import create_encoder_tab

# --- ТРЕЙ ---
def create_icon_image():
    image = Image.new('RGB', (64, 64), color=(30, 30, 30))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(0, 255, 0))
    return image

def main(page: ft.Page):
    # 1. ІНІЦІАЛІЗАЦІЯ СЕРВІСУ
    service = Service()
    service.load_config()
    
    # 2. ПІДКЛЮЧЕННЯ ARDUINO
    arduino = ArduinoHandler(service)
    arduino.connect()

    # Збереження при виході
    atexit.register(lambda: service.save_config())

    # 3. НАЛАШТУВАННЯ ВІКНА
    page.title = "Arduino MacroKey"
    page.window.width = 800
    page.window.height = 800
    page.window.prevent_close = True

    def window_event(e):
        if e.data == "close":
            page.window.visible = False
            page.update()

    page.window.on_event = window_event

    # 4. ТРЕЙ (Запуск у потоці)
    def tray_thread():
        def on_open(icon, item):
            page.window.minimized = False
            page.window.visible = True
            page.window.always_on_top = True
            page.update()
            page.window.always_on_top = False
            page.update()

        def on_quit(icon, item):
            icon.stop()
            service.save_config()
            page.window.destroy()

        icon = pystray.Icon("MacroKey", create_icon_image(), "MacroKey", 
            menu=pystray.Menu(
                pystray.MenuItem("Відкрити", on_open, default=True),
                pystray.MenuItem("Вихід", on_quit)
            ))
        icon.run()

    threading.Thread(target=tray_thread, daemon=True).start()

    # 5. ІНТЕРФЕЙС
    profile_text = ft.Text(
        value=f"АКТИВНИЙ ПРОФІЛЬ: {service.get_current_profile_index()}", 
        size=20, weight="bold", color="green"
    )

    def update_profile_ui():
        idx = service.get_current_profile_index()
        profile_text.value = f"АКТИВНИЙ ПРОФІЛЬ: {idx}"
        profile_text.color = {1: "red", 2: "yellow", 3: "green"}.get(idx, "black")
        
        # Оновлюємо вміст вкладок, якщо вони мають метод refresh
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()
        page.update()

    service.on_profile_change_callback = update_profile_ui

    # Вкладки
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Налаштування кнопок", content=create_buttons_tab(page, service)),
            ft.Tab(text="Гарячі клавіші", content=create_hotkeys_tab(page, service)),
            ft.Tab(text="Енкодер", content=create_encoder_tab(page, service)),
        ],
        expand=True
    )

    page.add(
        ft.Row([profile_text], alignment=ft.MainAxisAlignment.CENTER),
        tabs
    )

if __name__ == "__main__":
    ft.app(target=main)