# tab_hotkeys.py
import flet as ft

def create_hotkeys_tab(page: ft.Page, service):
    """
    Вкладка для створення гарячих клавіш.
    """

    tab_column = ft.Column(spacing=10, scroll="auto")

    # Поля для введення нової гарячої клавіші
    name_field = ft.TextField(label="Назва гарячої клавіші", width=250)
    combo_field = ft.TextField(label="Комбінація (наприклад: ctrl+alt+k)", width=250)

    # Список гарячих клавіш
    hotkey_list = ft.Column(spacing=5)

    def update_list():
        hotkey_list.controls.clear()
        for hk in service.get_hotkeys():
            hotkey_list.controls.append(ft.Text(f"{hk.name} → {hk.combo}"))
        page.update()

    def save_hotkey(e):
        if not name_field.value.strip() or not combo_field.value.strip():
            page.snack_bar = ft.SnackBar(ft.Text("❌ Заповни всі поля!"))
            page.snack_bar.open = True
            page.update()
            return

        service.add_hotkey(name_field.value.strip(), combo_field.value.strip())
        page.snack_bar = ft.SnackBar(ft.Text(f"Гаряча клавіша '{name_field.value}' додана ✅"))
        page.snack_bar.open = True
        page.update()

        name_field.value = ""
        combo_field.value = ""
        update_list()

    save_button = ft.ElevatedButton("Зберегти", on_click=save_hotkey)

    # Початкове наповнення
    update_list()

    tab_column.controls.extend([
        ft.Row([name_field, combo_field, save_button], spacing=10),
        ft.Divider(),
        ft.Text("Список гарячих клавіш:"),
        hotkey_list
    ])

    return tab_column
