import flet as ft
from tab_buttons import create_buttons_tab
from tab_hotkeys import create_hotkeys_tab
from tab_encoder import create_encoder_tab
from service import Service
from arduino_handler import ArduinoHandler
from hotkeys import press_combo
from config_manager import load_config, save_config
import atexit
import threading
import pystray
from PIL import Image, ImageDraw
import time

# Реєстрація збереження при виході
atexit.register(lambda: save_config())

# --- ІКОНКА ---
def create_icon_image():
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(30, 30, 30))
    dc = ImageDraw.Draw(image)
    dc.rectangle((16, 16, 48, 48), fill=(0, 255, 0)) # Зелений квадрат
    return image

def main(page: ft.Page):
    # 1. БАЗОВІ НАЛАШТУВАННЯ (НОВИЙ СИНТАКСИС)
    page.title = "Arduino MacroKey"
    
    # Використовуємо page.window.xxx замість page.window_xxx
    page.window.width = 800
    page.window.height = 700
    
    # === ВАЖЛИВО: Блокуємо закриття (новий синтаксис) ===
    page.window.prevent_close = True
    page.update() 
    print("🔒 БЛОКУВАННЯ ЗАКРИТТЯ УВІМКНЕНО")

    # 2. ФУНКЦІЯ ОБРОБКИ ПОДІЙ ВІКНА
    def window_event(e):
        # Якщо натиснули Хрестик ("close")
        if e.data == "close":
            print("🔽 Команда 'Закрити' перехоплена. Ховаємо вікно...")
            page.window.visible = False
            page.update()
            print("ℹ️ Програма працює у фоні! Шукайте зелений квадрат біля годинника.")

    # Прив'язуємо подію (новий синтаксис)
    page.window.on_event = window_event

    # 3. ЛОГІКА ТРЕЯ
    def on_tray_open(icon, item):
        print("🔼 Відновлюємо вікно...")
        # Використовуємо page.window.xxx
        page.window.minimized = False
        page.window.visible = True
        page.update()
        
        # Хак для фокусу
        page.window.always_on_top = True
        page.update()
        page.window.always_on_top = False
        page.update()

    def on_tray_quit(icon, item):
        print("👋 Повний вихід...")
        icon.stop()
        page.window.destroy()

    def start_tray():
        try:
            icon = pystray.Icon("MacroKey", create_icon_image(), "Arduino MacroKey", 
                menu=pystray.Menu(
                    pystray.MenuItem("Відкрити", on_tray_open, default=True),
                    pystray.MenuItem("Вихід", on_tray_quit)
                )
            )
            icon.run()
        except Exception as e:
            print(f"❌ Помилка трея: {e}")

    threading.Thread(target=start_tray, daemon=True).start()

    # --- ЗАВАНТАЖЕННЯ ДАНИХ ---
    print("⏳ Завантаження конфігурації...")
    load_config()
    service = Service()
    active_encoder_ref = {"mode": None}

    # Інтерфейс
    profile_text = ft.Text(
        value=f"АКТИВНИЙ ПРОФІЛЬ: {service.get_current_profile_index()}", 
        size=20, weight="bold", color="green"
    )

    def on_profile_changed():
        new_idx = service.get_current_profile_index()
        profile_text.value = f"АКТИВНИЙ ПРОФІЛЬ: {new_idx}"
        colors = {1: "red", 2: "yellow", 3: "green"}
        profile_text.color = colors.get(new_idx, "black")
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()
        page.update()

    service.on_profile_change_callback = on_profile_changed

    # Обробка кнопок
    def handle_button_press(button_name):
        try:
            current_buttons = service.get_buttons()
            btn = next((b for b in current_buttons if b.name == button_name), None)
            
            if btn:
                if btn.encoder_mode:
                    active_encoder_ref["mode"] = btn.encoder_mode
                    print(f"🔧 Енкодер: {btn.encoder_mode.name}")
                elif btn.hotkey:
                    print(f"🎹 Клік: {btn.hotkey.combo}")
                    press_combo(btn.hotkey.combo)
                else:
                    print(f"⚪ {button_name} (без дії)")
        except Exception as e:
            print(f"⚠️ Помилка обробки кнопки: {e}")

    arduino = ArduinoHandler(handle_button_press, active_encoder_ref, service)
    arduino.connect()

    # Вкладки (залишаємо text, бо версія дозволяє)
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Налаштування кнопок", 
                content=create_buttons_tab(page, service)
            ),
            ft.Tab(
                text="Гарячі клавіші", 
                content=create_hotkeys_tab(page, service)
            ),
            ft.Tab(
                text="Енкодер", 
                content=create_encoder_tab(page, service)
            ),
        ],
        expand=True
    )

    page.add(
        ft.Row([profile_text], alignment=ft.MainAxisAlignment.CENTER),
        tabs
    )
    
    page.update()

if __name__ == "__main__":
    ft.app(target=main)

    