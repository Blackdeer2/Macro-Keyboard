# main.py
import flet as ft
from tab_buttons import create_buttons_tab
from tab_hotkeys import create_hotkeys_tab
from tab_encoder import create_encoder_tab
from main_data import arduino_buttons, hotkey_combos, encoder_modes
from service import Service

def main(page: ft.Page):
    page.title = "Arduino Hotkeys + Encoder Modes"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Створюємо об'єкт сервісу
    service = Service(
    arduino_buttons=arduino_buttons,
    hotkey_combos=hotkey_combos,
    encoder_modes=encoder_modes
)

    # Створюємо вкладки
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Кнопки",
                content=create_buttons_tab(page, service)  # <-- передаємо service
            ),
            ft.Tab(
                text="Гарячи клавіші",
                content=create_hotkeys_tab(page, service)  # <-- передаємо service
            ),
            ft.Tab(
                text="Режими енкодера",
                content=create_encoder_tab(page, service)  # <-- передаємо service
            ),
        ],
        expand=True
    )

    page.add(tabs)

if __name__ == "__main__":
    ft.app(target=main)
