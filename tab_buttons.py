import flet as ft

def create_buttons_tab(page: ft.Page, service):
    tab_column = ft.Column(spacing=10, scroll="auto")
    
    # Зберігаємо посилання на елементи
    ui_rows = []

    # ----------------- Функція оновлення -----------------
    def refresh_dropdowns():
        current_buttons_data = service.get_buttons()

        for i, (hk_dd, em_dd, btn_name) in enumerate(ui_rows):
            btn_data = current_buttons_data[i]

            # Оновлюємо варіанти
            hk_dd.options.clear()
            hk_dd.options.append(ft.dropdown.Option("---")) 
            for hk in service.get_hotkeys():
                hk_dd.options.append(ft.dropdown.Option(hk.name))

            em_dd.options.clear()
            em_dd.options.append(ft.dropdown.Option("---"))
            for em in service.get_encoder_modes():
                em_dd.options.append(ft.dropdown.Option(em.name))

            # Встановлюємо значення
            hk_dd.value = btn_data.hotkey.name if btn_data.hotkey else "---"
            em_dd.value = btn_data.encoder_mode.name if btn_data.encoder_mode else "---"

            hk_dd.update()
            em_dd.update()

        page.update()

    service.refresh_buttons_dropdowns = refresh_dropdowns

    # ----------------- Створення рядків -----------------
    initial_buttons = service.get_buttons()

    for btn in initial_buttons:
        # Створюємо змінні заздалегідь, щоб використати їх у функціях
        hk_dd = ft.Dropdown(label="Гаряча клавіша", width=200)
        em_dd = ft.Dropdown(label="Режим енкодера", width=200)

        # === ЛОГІКА ВЗАЄМНОГО ВИКЛЮЧЕННЯ ===
        # Якщо обрали гарячу клавішу -> скидаємо енкодер
        def on_hotkey_change(e, e_d=em_dd):
            if e.control.value != "---":
                e_d.value = "---"
                e_d.update()

        # Якщо обрали режим енкодера -> скидаємо гарячу клавішу
        def on_encoder_change(e, h_d=hk_dd):
            if e.control.value != "---":
                h_d.value = "---"
                h_d.update()

        # Прив'язуємо функції до події on_change
        hk_dd.on_change = on_hotkey_change
        em_dd.on_change = on_encoder_change

        # === Кнопка збереження ===
        def save_btn_click(e, b_name=btn.name, h_d=hk_dd, e_d=em_dd):
            hk_val = h_d.value if h_d.value != "---" else None
            em_val = e_d.value if e_d.value != "---" else None

            # Зберігаємо (сервіс сам подбає про очистку конфліктів)
            service.assign_hotkey_to_button(b_name, hk_val)
            service.assign_encoder_mode_to_button(b_name, em_val)

            page.snack_bar = ft.SnackBar(ft.Text(f"{b_name} збережено!"))
            page.snack_bar.open = True
            page.update()

        save_button = ft.ElevatedButton("Зберегти", on_click=save_btn_click)

        ui_rows.append((hk_dd, em_dd, btn.name))

        row = ft.Row([
            ft.Text(btn.name, width=80, weight="bold"), 
            hk_dd, 
            em_dd, 
            save_button
        ], spacing=10)
        
        tab_column.controls.append(row)

    # Первинне наповнення (те саме, що було раніше)
    current_buttons_data = service.get_buttons()
    for i, (hk_dd, em_dd, _) in enumerate(ui_rows):
        btn_data = current_buttons_data[i]
        hk_dd.options.append(ft.dropdown.Option("---"))
        for hk in service.get_hotkeys():
            hk_dd.options.append(ft.dropdown.Option(hk.name))
        em_dd.options.append(ft.dropdown.Option("---"))
        for em in service.get_encoder_modes():
            em_dd.options.append(ft.dropdown.Option(em.name))
        hk_dd.value = btn_data.hotkey.name if btn_data.hotkey else "---"
        em_dd.value = btn_data.encoder_mode.name if btn_data.encoder_mode else "---"

    return tab_column