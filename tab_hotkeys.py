import flet as ft
from main_data import hotkey_combos
from hotkey_combo import HotkeyCombo

def create_hotkeys_tab(page: ft.Page, service):
    tab_column = ft.Column(spacing=10, scroll="auto")

    # Поля для введення
    name_field = ft.TextField(label="Назва гарячої клавіші", width=250)
    combo_field = ft.TextField(label="Комбінація (наприклад: ctrl+alt+k)", width=250)

    # Список гарячих клавіш
    hotkeys_list = ft.Column(spacing=5)

    def update_hotkeys_list():
        hotkeys_list.controls.clear()
        for hk in hotkey_combos:
            # Кнопка видалення поруч з гарячою клавішею
            delete_button = ft.IconButton(
                # ВИПРАВЛЕННЯ: ft.icons (маленька літера)
                icon=ft.icons.DELETE_OUTLINE,
                tooltip="Видалити",
                on_click=lambda e, hk=hk: remove_hotkey(hk)
            )
            hotkeys_list.controls.append(
                ft.Row([ft.Text(f"{hk.name} → {hk.combo}"), delete_button], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        page.update()

    def remove_hotkey(hk_to_remove):
        hotkey_combos.remove(hk_to_remove)
        print(f"❌ Видалено гарячу клавішу: {hk_to_remove.name}")
        update_hotkeys_list()
        # Оновлення dropdown у вкладці кнопок
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    # Кнопка збереження
    def save_hotkey(e):
        name = name_field.value.strip()
        combo = combo_field.value.strip()

        if not name or not combo:
            print("❌ Заповни всі поля!")
            return

        # Додаємо нову гарячу клавішу
        hotkey_combos.append(HotkeyCombo(name, combo))

        # Вивід у консоль
        print("=== Гарячі клавіші ===")
        for hk in hotkey_combos:
            print(f"{hk.name} → {hk.combo}")

        # Оновлення списку
        update_hotkeys_list()

        # Очищаємо поля
        name_field.value = ""
        combo_field.value = ""
        name_field.update()
        combo_field.update()

        # Оновлення dropdown у вкладці кнопок
        if hasattr(service, "refresh_buttons_dropdowns"):
            service.refresh_buttons_dropdowns()

    save_button = ft.ElevatedButton("Зберегти", on_click=save_hotkey)

    # Додаємо форму та список на вкладку
    tab_column.controls.append(
        ft.Row([name_field, combo_field, save_button], spacing=10)
    )
    tab_column.controls.append(ft.Text("Список гарячих клавіш:", weight="bold"))
    tab_column.controls.append(hotkeys_list)

    # Початкове оновлення списку
    update_hotkeys_list()

    return tab_column