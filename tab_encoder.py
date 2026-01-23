import flet as ft

def create_encoder_tab(page: ft.Page, service):
    tab_column = ft.Column(spacing=10, scroll="auto")

    # Поля для введення
    name_field = ft.TextField(label="Назва режиму", width=150)
    left_field = ft.TextField(label="Left", width=100)
    right_field = ft.TextField(label="Right", width=100)
    alt_left_field = ft.TextField(label="Alt Left", width=100)
    alt_right_field = ft.TextField(label="Alt Right", width=100)

    # Список режимів
    modes_list = ft.Column(spacing=5)

    def refresh_modes():
        modes_list.controls.clear()
        for em in service.get_encoder_modes():
            
            # Текст опису режиму
            info_text = ft.Text(
                f"{em.name} \n   L:{em.left_cmd} R:{em.right_cmd}\n   Alt: {em.alt_left_cmd}/{em.alt_right_cmd}", 
                size=12
            )

            # Кнопка видалення
            delete_btn = ft.IconButton(
                # ВИПРАВЛЕННЯ: ft.icons (маленька літера)
                icon=ft.icons.DELETE_OUTLINE,
                icon_color="red",
                tooltip="Видалити режим",
                on_click=lambda e, x=em: delete_mode(x)
            )

            # Рядок: Текст + Кнопка видалення
            row = ft.Container(
                content=ft.Row(
                    [info_text, delete_btn],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=10,
                border=ft.border.all(1, ft.colors.OUTLINE), # Також colors з маленької
                border_radius=5
            )
            
            modes_list.controls.append(row)
        page.update()

    # Функція видалення
    def delete_mode(mode_obj):
        service.remove_encoder_mode(mode_obj)
        refresh_modes()
        # Також оновлюємо випадаючі списки у вкладці кнопок
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    # Функція збереження
    def save_encoder_mode(e):
        name = name_field.value.strip()
        if not name:
            page.snack_bar = ft.SnackBar(ft.Text("❌ Введіть назву режиму!"))
            page.snack_bar.open = True
            page.update()
            return

        service.add_encoder_mode(
            name, 
            left_field.value.strip(), 
            right_field.value.strip(),
            alt_left_field.value.strip(),
            alt_right_field.value.strip()
        )
        
        # Очистка полів
        name_field.value = ""
        left_field.value = ""
        right_field.value = ""
        alt_left_field.value = ""
        alt_right_field.value = ""
        
        refresh_modes()
        
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    save_button = ft.ElevatedButton("Додати режим", on_click=save_encoder_mode)

    # Компонування форми
    form_row_1 = ft.Row([name_field, save_button])
    form_row_2 = ft.Row([left_field, right_field])
    form_row_3 = ft.Row([alt_left_field, alt_right_field])

    tab_column.controls.extend([
        ft.Text("Додати новий режим енкодера", weight="bold"),
        form_row_1,
        form_row_2,
        form_row_3,
        ft.Divider(),
        ft.Text("Список режимів:", weight="bold"),
        modes_list
    ])

    refresh_modes()
    return tab_column