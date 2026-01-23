import flet as ft

def create_hotkeys_tab(page: ft.Page, service):
    # Основний список
    hotkeys_list = ft.Column(spacing=10)

    def update_hotkeys_list():
        hotkeys_list.controls.clear()
        for hk in service.get_hotkeys():
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE_OUTLINE,
                tooltip="Видалити",
                on_click=lambda e, hk=hk: remove_hotkey(hk)
            )
            # Картка для кожного хоткея
            card = ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"{hk.name}", weight="bold", width=150),
                        ft.Text(f"→   {hk.combo}", size=16, color="blue"),
                        delete_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=10,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=8,
                bgcolor=ft.colors.SURFACE_VARIANT
            )
            hotkeys_list.controls.append(card)
        page.update()

    def remove_hotkey(hk_to_remove):
        service.remove_hotkey(hk_to_remove)
        update_hotkeys_list()
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    # --- Форма додавання ---
    name_field = ft.TextField(label="Назва", width=200)
    combo_field = ft.TextField(label="Комбінація (напр. ctrl+c)", width=200)

    def save_hotkey(e):
        name = name_field.value.strip()
        combo = combo_field.value.strip()
        if not name or not combo: return

        service.add_hotkey(name, combo)
        update_hotkeys_list()
        
        name_field.value = ""
        combo_field.value = ""
        name_field.update()
        combo_field.update()
        
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    save_button = ft.ElevatedButton("Додати", on_click=save_hotkey, height=50)

    # Компонування форми
    form_row = ft.Row(
        [name_field, combo_field, save_button], 
        vertical_alignment=ft.CrossAxisAlignment.START,
        alignment=ft.MainAxisAlignment.START,
        spacing=20
    )

    content_col = ft.Column(
        controls=[
            ft.Text("Створити нову гарячу клавішу", size=20, weight="bold"),
            form_row,
            ft.Divider(height=30, thickness=2),
            ft.Text("Список доступних клавіш", size=20, weight="bold"),
            hotkeys_list
        ],
        scroll="auto"
    )

    update_hotkeys_list()

    # Повертаємо контейнер з відступами
    return ft.Container(
        content=content_col,
        padding=30
    )