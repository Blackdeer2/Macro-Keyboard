import flet as ft

def create_buttons_tab(page: ft.Page, service):
    # Основний список (щільний)
    tab_column = ft.Column(spacing=2, scroll="auto")
    
    ui_rows = []

    # --- Оновлення даних ---
    def refresh_dropdowns():
        current_buttons_data = service.get_buttons()

        for i, (hk_dd, em_dd, btn_name) in enumerate(ui_rows):
            btn_data = current_buttons_data[i]

            # Оновлюємо списки
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

            if hk_dd.page: hk_dd.update()
            if em_dd.page: em_dd.update()

        if page: page.update()

    service.refresh_buttons_dropdowns = refresh_dropdowns

    # --- Створення рядків ---
    initial_buttons = service.get_buttons()

    # === ЗАГОЛОВОК ТАБЛИЦІ ===
    header = ft.Container(
        content=ft.Row([
            ft.Text("Кнопка", width=100, weight="bold", color="grey"),
            ft.Text("Гаряча клавіша", width=200, weight="bold", color="grey"),
            ft.Text("", width=30), # Місце під "або"
            ft.Text("Шар енкодера", width=200, weight="bold", color="grey"),
            ft.Text("", width=200, weight="bold", color="grey"),
        ], alignment=ft.MainAxisAlignment.START),
        padding=ft.padding.only(left=10, right=10, bottom=5)
    )
    tab_column.controls.append(header)

    for btn in initial_buttons:
        # === ДРОПДАУНИ ===
        # Прибрано параметр `icon=...`, тепер буде тільки одна стандартна стрілка
        
        hk_dd = ft.Dropdown(
            width=200, 
            height=35, 
            text_size=13,
            content_padding=10,
            # icon=ft.icons.KEYBOARD_ARROW_DOWN, <-- ПРИБРАНО
            filled=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=5,
            border_width=0,
            hint_text="---"
        )
        
        em_dd = ft.Dropdown(
            width=200, 
            height=35,
            text_size=13,
            content_padding=10,
            # icon=ft.icons.KEYBOARD_ARROW_DOWN, <-- ПРИБРАНО
            filled=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_radius=5,
            border_width=0,
            hint_text="---"
        )

        # Логіка
        def on_hotkey_change(e, e_d=em_dd):
            if e.control.value != "---":
                e_d.value = "---"
                if e_d.page: e_d.update()

        def on_encoder_change(e, h_d=hk_dd):
            if e.control.value != "---":
                h_d.value = "---"
                if h_d.page: h_d.update()

        hk_dd.on_change = on_hotkey_change
        em_dd.on_change = on_encoder_change

        # Збереження
        def save_btn_click(e, b_name=btn.name, h_d=hk_dd, e_d=em_dd):
            hk_val = h_d.value if h_d.value != "---" else None
            em_val = e_d.value if e_d.value != "---" else None
            service.assign_hotkey_to_button(b_name, hk_val)
            service.assign_encoder_mode_to_button(b_name, em_val)
            
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ {b_name} збережено"), duration=1000)
            page.snack_bar.open = True
            page.update()

        # Кнопка збереження в рядку
        save_button = ft.Container(
            content=ft.IconButton(
                icon=ft.icons.SAVE, # <-- ЗАМІНЕНО на іконку збереження
                icon_size=20,
                icon_color="grey", # Трохи нейтральніший колір, поки не натиснуто
                tooltip="Зберегти",
                on_click=save_btn_click,
                style=ft.ButtonStyle(padding=0)
            ),
            width=40,
            alignment=ft.alignment.center
        )

        ui_rows.append((hk_dd, em_dd, btn.name))

        # === РЯДОК ===
        row_content = ft.Row([
            # Назва кнопки
            ft.Row([
                ft.Icon(ft.icons.SMART_BUTTON, size=16, color="blue"),
                ft.Text(btn.name, weight="bold", size=14)
            ], width=100),
            
            hk_dd,
            
            ft.Text("або", size=12, color="grey", italic=True, width=30, text_align="center"),
            
            em_dd,
            
            save_button
        ], alignment=ft.MainAxisAlignment.START, height=45)

        row_container = ft.Container(
            content=row_content,
            padding=ft.padding.symmetric(horizontal=10),
            border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.with_opacity(0.1, "grey"))),
        )
        
        tab_column.controls.append(row_container)

    refresh_dropdowns()

    return ft.Container(
        content=tab_column,
        padding=20
    )