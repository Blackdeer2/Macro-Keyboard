import flet as ft

def create_encoder_tab(page: ft.Page, service):
    # Поля
    name_field = ft.TextField(label="Назва режиму", width=200)
    
    # Групуємо поля по парах
    left_field = ft.TextField(label="Вліво (Left)", width=150)
    right_field = ft.TextField(label="Вправо (Right)", width=150)
    
    alt_left_field = ft.TextField(label="Alt Вліво", width=150)
    alt_right_field = ft.TextField(label="Alt Вправо", width=150)

    modes_list = ft.Column(spacing=10)

    def refresh_modes():
        modes_list.controls.clear()
        for em in service.get_encoder_modes():
            info_text = ft.Column([
                ft.Text(em.name, weight="bold", size=16),
                ft.Text(f"L: {em.left_cmd} | R: {em.right_cmd}", size=12),
                ft.Text(f"Alt L: {em.alt_left_cmd} | Alt R: {em.alt_right_cmd}", size=12, color="grey"),
            ], spacing=2)

            delete_btn = ft.IconButton(
                icon=ft.icons.DELETE_OUTLINE,
                icon_color="red",
                on_click=lambda e, x=em: delete_mode(x)
            )

            row = ft.Container(
                content=ft.Row([info_text, delete_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=15,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=10,
                bgcolor=ft.colors.SURFACE_VARIANT
            )
            modes_list.controls.append(row)
        if page: page.update()

    def delete_mode(mode_obj):
        service.remove_encoder_mode(mode_obj)
        refresh_modes()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    def save_encoder_mode(e):
        name = name_field.value.strip()
        if not name: return

        service.add_encoder_mode(
            name, 
            left_field.value.strip(), right_field.value.strip(),
            alt_left_field.value.strip(), alt_right_field.value.strip()
        )
        
        name_field.value = ""
        left_field.value = ""
        right_field.value = ""
        alt_left_field.value = ""
        alt_right_field.value = ""
        
        refresh_modes()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    save_button = ft.ElevatedButton("Додати режим", on_click=save_encoder_mode, height=50)

    # Компонування
    content_col = ft.Column(
        controls=[
            ft.Text("Додати режим енкодера", size=20, weight="bold"),
            ft.Row([name_field, save_button], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Row([left_field, right_field]),
            ft.Row([alt_left_field, alt_right_field]),
            ft.Divider(height=30),
            ft.Text("Активні режими", size=20, weight="bold"),
            modes_list
        ],
        scroll="auto",
        spacing=15
    )

    refresh_modes()
    
    return ft.Container(
        content=content_col,
        padding=30
    )