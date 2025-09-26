# tab_buttons.py
import flet as ft
from main_data import arduino_buttons, hotkey_combos, encoder_modes

def create_buttons_tab(page: ft.Page):
    """
    Повертає колонку з кнопками Arduino та полями для призначення гарячих клавіш
    або режимів енкодера.
    """

    tab_column = ft.Column(spacing=10, scroll="auto")

    for btn in arduino_buttons:
        # Поле для гарячої клавіші
        hotkey_field = ft.TextField(
            label=f"{btn.name} Hotkey",
            width=250,
            value=btn.hotkey.name if btn.hotkey else ""
        )

        # Випадний список для вибору режиму енкодера
        encoder_dropdown = ft.Dropdown(
            label="Виберіть режим енкодера",
            options=[ft.dropdown.Option(mode.name) for mode in encoder_modes],
            value=btn.encoder_mode.name if btn.encoder_mode else None,
            width=250
        )

        # Функція збереження налаштувань кнопки
        def save_btn(e, b=btn, hf=hotkey_field, ed=encoder_dropdown):
            # Зберігаємо гарячу клавішу (пошук за назвою)
            b.hotkey = next((hk for hk in hotkey_combos if hk.name == hf.value.strip()), None)

            # Зберігаємо режим енкодера (пошук за назвою)
            b.encoder_mode = next((em for em in encoder_modes if em.name == ed.value), None)

            page.snack_bar = ft.SnackBar(ft.Text(f"{b.name} збережено ✅"))
            page.snack_bar.open = True
            page.update()

        save_button = ft.ElevatedButton(text="Зберегти", on_click=save_btn)

        # Додаємо до вкладки: поле гарячої клавіші, дропдаун і кнопку
        tab_column.controls.append(ft.Column([hotkey_field, encoder_dropdown, save_button, ft.Divider()]))

    return tab_column
