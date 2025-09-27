import flet as ft

def create_buttons_tab(page: ft.Page, service):
    """
    Вкладка для 9 кнопок Arduino.
    Для кожної кнопки можна вибрати гарячу клавішу і режим енкодера.
    """

    tab_column = ft.Column(spacing=10, scroll="auto")
    dropdowns = []  # зберігатимемо посилання на dropdown-и для оновлення

    def refresh_dropdowns():
        """Оновлює всі dropdown-и, коли змінився service"""
        hotkey_options = [ft.dropdown.Option(hk.name) for hk in service.get_hotkeys()]
        encoder_options = [ft.dropdown.Option(mode.name) for mode in service.get_encoder_modes()]

        for hk_dd, em_dd, btn in dropdowns:
            hk_dd.options = hotkey_options
            hk_dd.value = btn.hotkey.name if btn.hotkey else None

            em_dd.options = encoder_options
            em_dd.value = btn.encoder_mode.name if btn.encoder_mode else None

        page.update()

    # Підписуємо вкладку на зміни в service
    service.subscribe(refresh_dropdowns)

    for btn in service.get_buttons():
        hotkey_dropdown = ft.Dropdown(label="Гаряча клавіша", width=200)
        encoder_dropdown = ft.Dropdown(label="Режим енкодера", width=200)

        # кнопка "Зберегти" для конкретної кнопки
        def save_btn(e, b=btn, hk_dd=hotkey_dropdown, em_dd=encoder_dropdown):
            service.assign_hotkey_to_button(b.name, hk_dd.value)
            service.assign_encoder_mode_to_button(b.name, em_dd.value)
            page.snack_bar = ft.SnackBar(ft.Text(f"{b.name} збережено ✅"))
            page.snack_bar.open = True
            page.update()

        save_button = ft.ElevatedButton("Зберегти", on_click=save_btn)

        # Додаємо dropdown-и та кнопку до списку для оновлення
        dropdowns.append((hotkey_dropdown, encoder_dropdown, btn))

        # Створюємо рядок для кнопки
        row = ft.Row(
            controls=[ft.Text(btn.name, width=100), hotkey_dropdown, encoder_dropdown, save_button],
            spacing=10
        )
        tab_column.controls.append(row)

    # Підвантажуємо початкові дані
    refresh_dropdowns()

    return tab_column
