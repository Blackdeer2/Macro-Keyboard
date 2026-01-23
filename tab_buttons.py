import flet as ft

def create_buttons_tab(page: ft.Page, service):
    # Використовуємо Column для списку, але без скролу тут (скрол буде у зовнішньому контейнері, якщо треба, або тут)
    # Краще залишити скрол тут, але додати відступи через Container
    tab_column = ft.Column(spacing=15, scroll="auto") 
    
    ui_rows = []

    # --- Функція оновлення ---
    def refresh_dropdowns():
        current_buttons_data = service.get_buttons()

        for i, (hk_dd, em_dd, btn_name) in enumerate(ui_rows):
            btn_data = current_buttons_data[i]

            # 1. Оновлення списків (безпечно в пам'яті)
            hk_dd.options.clear()
            hk_dd.options.append(ft.dropdown.Option("---")) 
            for hk in service.get_hotkeys():
                hk_dd.options.append(ft.dropdown.Option(hk.name))

            em_dd.options.clear()
            em_dd.options.append(ft.dropdown.Option("---"))
            for em in service.get_encoder_modes():
                em_dd.options.append(ft.dropdown.Option(em.name))

            # 2. Встановлення значень
            hk_dd.value = btn_data.hotkey.name if btn_data.hotkey else "---"
            em_dd.value = btn_data.encoder_mode.name if btn_data.encoder_mode else "---"

            # 3. Візуальне оновлення (ТІЛЬКИ якщо елемент на сторінці)
            if hk_dd.page: hk_dd.update()
            if em_dd.page: em_dd.update()

        # Оновлення сторінки, якщо вона існує
        if page: page.update()

    service.refresh_buttons_dropdowns = refresh_dropdowns

    # --- Створення рядків ---
    initial_buttons = service.get_buttons()

    for btn in initial_buttons:
        hk_dd = ft.Dropdown(label="Гаряча клавіша", width=180, text_size=14)
        em_dd = ft.Dropdown(label="Режим енкодера", width=180, text_size=14)

        # Логіка перемикання
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

        # Кнопка збереження
        def save_btn_click(e, b_name=btn.name, h_d=hk_dd, e_d=em_dd):
            hk_val = h_d.value if h_d.value != "---" else None
            em_val = e_d.value if e_d.value != "---" else None
            service.assign_hotkey_to_button(b_name, hk_val)
            service.assign_encoder_mode_to_button(b_name, em_val)
            
            page.snack_bar = ft.SnackBar(ft.Text(f"✅ {b_name} збережено!"))
            page.snack_bar.open = True
            page.update()

        save_button = ft.ElevatedButton("Зберегти", on_click=save_btn_click)

        ui_rows.append((hk_dd, em_dd, btn.name))

        # === ГОЛОВНЕ ПОКРАЩЕННЯ ВИГЛЯДУ ===
        row = ft.Row(
            controls=[
                # Фіксована ширина для назви кнопки, вирівнювання тексту праворуч
                ft.Container(
                    content=ft.Text(btn.name, weight="bold", size=16),
                    width=100,
                    alignment=ft.alignment.center_left
                ),
                hk_dd, 
                em_dd, 
                save_button
            ],
            spacing=15,
            vertical_alignment=ft.CrossAxisAlignment.CENTER # Центруємо елементи по вертикалі
        )
        
        tab_column.controls.append(row)

    # Заповнюємо значення (без update(), бо елементи ще не на сторінці)
    refresh_dropdowns()

    # Повертаємо Контейнер з відступами
    return ft.Container(
        content=tab_column,
        padding=ft.padding.all(30), # Великий гарний відступ з усіх боків
        alignment=ft.alignment.top_left
    )