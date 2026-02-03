import flet as ft

def create_hotkeys_tab(page: ft.Page, service):
    # Основний контейнер
    tab_content = ft.Column(spacing=20, scroll="auto")

    # ==========================================
    # 1. БЛОК СТВОРЕННЯ (Верхня частина)
    # ==========================================
    
    name_field = ft.TextField(
        hint_text="Назва (напр. Copy)", 
        width=200, 
        height=35,
        text_size=13,
        content_padding=10,
        filled=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_width=0,
        border_radius=5
    )
    
    combo_field = ft.TextField(
        hint_text="Комбінація (напр. ctrl+c)", 
        width=200,
        height=35,
        text_size=13,
        content_padding=10,
        filled=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        border_width=0,
        border_radius=5
    )

    def save_hotkey(e):
        name = name_field.value.strip()
        combo = combo_field.value.strip()
        if not name or not combo:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Введіть назву та комбінацію!"))
            page.snack_bar.open = True
            page.update()
            return

        service.add_hotkey(name, combo)
        update_hotkeys_list()
        
        name_field.value = ""
        combo_field.value = ""
        name_field.update()
        combo_field.update()
        
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()
            
        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Гарячу клавішу '{name}' додано!"))
        page.snack_bar.open = True
        page.update()

    add_button = ft.ElevatedButton(
        text="Додати",
        icon=ft.icons.ADD,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.padding.symmetric(horizontal=15)
        ),
        height=35,
        on_click=save_hotkey
    )

    create_row = ft.Container(
        content=ft.Row([
            ft.Text("Нова клавіша:", weight="bold", size=14, color="grey"),
            name_field,
            ft.Text("+", size=16, color="grey"),
            combo_field,
            add_button
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=10,
        bgcolor=ft.colors.with_opacity(0.05, "blue"),
        border_radius=10
    )

    # ==========================================
    # 2. ТАБЛИЦЯ СПИСКУ (Нижня частина)
    # ==========================================
    
    hotkeys_list = ft.Column(spacing=2)

    def update_hotkeys_list():
        hotkeys_list.controls.clear()
        
        # --- ЗАГОЛОВОК ТАБЛИЦІ ---
        header = ft.Container(
            content=ft.Row([
                ft.Text("Назва", weight="bold", color="grey"),       # Ліворуч
                ft.Text("Комбінація", weight="bold", color="grey"),  # Центр (умовно)
                ft.Container(width=40)                               # Праворуч (пустишка під смітник)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),        # <--- РОЗТЯГУЄМО
            padding=ft.padding.only(left=10, right=10, bottom=5)
        )
        hotkeys_list.controls.append(header)

        # --- РЯДКИ ---
        for hk in service.get_hotkeys():
            
            # Кнопка видалення (Червоний смітник)
            delete_btn = ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE, # <--- СМІТНИК
                    icon_size=20,
                    icon_color="red",             # <--- ЧЕРВОНИЙ
                    tooltip="Видалити",
                    on_click=lambda e, x=hk: remove_hotkey(x),
                    style=ft.ButtonStyle(padding=0)
                ),
                width=40,
                alignment=ft.alignment.center_right
            )

            # Вміст рядка
            row_content = ft.Row([
                # Колонка 1: Назва
                ft.Row([
                    ft.Icon(ft.icons.KEYBOARD, size=16, color="blue"),
                    ft.Text(hk.name, weight="bold", size=14)
                ]),

                # Колонка 2: Комбінація
                ft.Container(
                    content=ft.Text(hk.combo, font_family="monospace", size=12),
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    bgcolor=ft.colors.with_opacity(0.1, "grey"),
                    border_radius=4,
                ),

                # Колонка 3: Смітник
                delete_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, height=45) # <--- РОЗТЯГУЄМО

            # Контейнер рядка
            row_container = ft.Container(
                content=row_content,
                padding=ft.padding.symmetric(horizontal=10),
                border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.with_opacity(0.1, "grey"))),
            )
            
            hotkeys_list.controls.append(row_container)
        
        if page: page.update()

    def remove_hotkey(hk_to_remove):
        service.remove_hotkey(hk_to_remove)
        update_hotkeys_list()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()
        
        page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ '{hk_to_remove.name}' видалено"))
        page.snack_bar.open = True
        page.update()

    # Збираємо все до купи
    tab_content.controls.append(create_row)
    tab_content.controls.append(ft.Divider(height=20, color="transparent"))
    tab_content.controls.append(hotkeys_list)

    update_hotkeys_list()

    return ft.Container(
        content=tab_content,
        padding=20
    )