import flet as ft

def create_encoder_tab(page: ft.Page, service):
    # Основний контейнер
    tab_content = ft.Column(spacing=20, scroll="auto")

    # ==========================================
    # 1. БЛОК СТВОРЕННЯ (Компактний)
    # ==========================================
    
    # Допоміжна функція для створення полів
    def create_input(label, hint, icon=None, color=None):
        return ft.TextField(
            label=label,
            hint_text=hint,
            width=180, 
            height=35,
            text_size=13,
            content_padding=10,
            prefix_icon=icon,
            label_style=ft.TextStyle(color=color) if color else None,
            filled=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border_width=0,
            border_radius=5
        )

    # --- Поля ---
    name_field = ft.TextField(
        hint_text="Назва пресету", 
        width=250, 
        height=35, text_size=13, content_padding=10,
        filled=True, bgcolor=ft.colors.SURFACE_VARIANT, border_width=0, border_radius=5
    )

    # Шар 1 (Звичайний)
    left_field = create_input("Вліво", "vol_down", ft.icons.ROTATE_LEFT)
    right_field = create_input("Вправо", "vol_up", ft.icons.ROTATE_RIGHT)

    # Шар 2 (Клік - Помаранчевий)
    click_left_field = create_input("Клік+Вліво", "prev", ft.icons.ROTATE_LEFT, "orange")
    click_right_field = create_input("Клік+Вправо", "next", ft.icons.ROTATE_RIGHT, "orange")

    # --- Логіка збереження ---
    def save_encoder_mode(e):
        name = name_field.value.strip()
        if not name:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Введіть назву!"))
            page.snack_bar.open = True
            page.update()
            return

        service.add_encoder_mode(
            name, 
            left_field.value.strip(), right_field.value.strip(),
            click_left_field.value.strip(), click_right_field.value.strip()
        )
        
        # Очистка
        name_field.value = ""
        left_field.value = ""
        right_field.value = ""
        click_left_field.value = ""
        click_right_field.value = ""
        
        refresh_modes()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

        page.snack_bar = ft.SnackBar(ft.Text(f"✅ Пресет '{name}' збережено!"))
        page.snack_bar.open = True
        page.update()

    # Кнопка додавання
    add_button = ft.ElevatedButton(
        text="Зберегти пресет",
        icon=ft.icons.SAVE,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=5),
            padding=ft.padding.symmetric(horizontal=15)
        ),
        height=35,
        on_click=save_encoder_mode
    )

    # Компонування форми
    create_form = ft.Container(
        content=ft.Column([
            ft.Row([ft.Text("Новий пресет:", weight="bold", color="grey"), name_field, add_button], alignment=ft.MainAxisAlignment.START),
            ft.Divider(color="transparent", height=5),
            ft.Row([
                ft.Text("Звичайний:", width=80, size=12, weight="bold", color="blue"),
                left_field, right_field
            ]),
            ft.Row([
                ft.Text("Після кліку:", width=80, size=12, weight="bold", color="orange"),
                click_left_field, click_right_field
            ])
        ], spacing=5),
        padding=15,
        bgcolor=ft.colors.with_opacity(0.03, "blue"),
        border_radius=10
    )

    # ==========================================
    # 2. ТАБЛИЦЯ СПИСКУ
    # ==========================================
    
    modes_list = ft.Column(spacing=2)

    def refresh_modes():
        modes_list.controls.clear()
        
        # --- ЗАГОЛОВОК ---
        header = ft.Container(
            content=ft.Row([
                ft.Text("Назва", width=150, weight="bold", color="grey"),
                ft.Text("Звичайний режим", width=180, weight="bold", color="grey", text_align="center"),
                ft.Text("Клік режим", width=180, weight="bold", color="grey", text_align="center"),
                ft.Container(width=40) # Під смітник
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(left=10, right=10, bottom=5)
        )
        modes_list.controls.append(header)

        # --- РЯДКИ ---
        for em in service.get_encoder_modes():
            
            # Смітник
            delete_btn = ft.Container(
                content=ft.IconButton(
                    icon=ft.icons.DELETE_OUTLINE, 
                    icon_size=20,
                    icon_color="red",
                    tooltip="Видалити",
                    on_click=lambda e, x=em: delete_mode(x),
                    style=ft.ButtonStyle(padding=0)
                ),
                width=40,
                alignment=ft.alignment.center_right
            )

            # === ФУНКЦІЯ ДЛЯ ВІДОБРАЖЕННЯ КОМАНД (КНОПКИ) ===
            def format_cmd(l, r, text_color):
                return ft.Container(
                    content=ft.Row([
                        # Команда Вліво
                        ft.Text(l if l else "-", size=12, color=text_color, font_family="monospace", weight="bold"),
                        # Розділювач
                        ft.Text("|", size=12, color="grey"),
                        # Команда Вправо
                        ft.Text(r if r else "-", size=12, color=text_color, font_family="monospace", weight="bold"),
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                    
                    # Стиль фону
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    bgcolor=ft.colors.with_opacity(0.1, "grey"), # Світло-сірий фон
                    border_radius=4,
                    alignment=ft.alignment.center
                )

            # Рядок
            row_content = ft.Row([
                # Колонка 1: Назва
                ft.Row([
                    ft.Icon(ft.icons.TUNE, size=16, color="blue"),
                    ft.Text(em.name, weight="bold", size=14, width=120, no_wrap=True)
                ], width=150),

                # Колонка 2: Звичайний (СИНІЙ ТЕКСТ)
                format_cmd(em.left_cmd, em.right_cmd, text_color="blue"),

                # Колонка 3: Клік (ОРАНЖЕВИЙ ТЕКСТ)
                format_cmd(em.alt_left_cmd, em.alt_right_cmd, text_color="orange"),

                # Колонка 4: Смітник
                delete_btn

            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, height=45)

            # Контейнер рядка
            row_container = ft.Container(
                content=row_content,
                padding=ft.padding.symmetric(horizontal=10),
                border=ft.border.only(bottom=ft.border.BorderSide(1, ft.colors.with_opacity(0.1, "grey"))),
            )
            modes_list.controls.append(row_container)
        
        if page: page.update()

    def delete_mode(mode_obj):
        service.remove_encoder_mode(mode_obj)
        refresh_modes()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()
        
        page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ Пресет '{mode_obj.name}' видалено"))
        page.snack_bar.open = True
        page.update()

    # Збираємо
    tab_content.controls.append(create_form)
    tab_content.controls.append(ft.Divider(height=20, color="transparent"))
    tab_content.controls.append(modes_list)

    refresh_modes()
    
    return ft.Container(
        content=tab_content,
        padding=20
    )