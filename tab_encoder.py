# tab_encoder.py
import flet as ft

def create_encoder_tab(page: ft.Page, service):
    """
    Вкладка для створення режимів енкодера.
    """

    tab_column = ft.Column(spacing=10, scroll="auto")

    # Поля для введення нового режиму
    name_field = ft.TextField(label="Назва режиму", width=250)
    left_field = ft.TextField(label="Left Command", width=250)
    right_field = ft.TextField(label="Right Command", width=250)
    alt_left_field = ft.TextField(label="Alt Left", width=250)
    alt_right_field = ft.TextField(label="Alt Right", width=250)

    def save_encoder_mode(e):
        service.add_encoder_mode(
            name=name_field.value.strip(),
            left_cmd=left_field.value.strip(),
            right_cmd=right_field.value.strip(),
            alt_left_cmd=alt_left_field.value.strip(),
            alt_right_cmd=alt_right_field.value.strip()
        )
        page.snack_bar = ft.SnackBar(ft.Text(f"Режим '{name_field.value}' додано ✅"))
        page.snack_bar.open = True
        page.update()

        # Очищаємо поля
        name_field.value = ""
        left_field.value = ""
        right_field.value = ""
        alt_left_field.value = ""
        alt_right_field.value = ""
        page.update()

    save_button = ft.ElevatedButton("Зберегти", on_click=save_encoder_mode)

    tab_column.controls.extend([name_field, left_field, right_field, alt_left_field, alt_right_field, save_button, ft.Divider()])

    # Список існуючих режимів
    for em in service.get_encoder_modes():
        tab_column.controls.append(ft.Text(f"{em.name} → L:{em.left_cmd} R:{em.right_cmd} AltL:{em.alt_left_cmd} AltR:{em.alt_right_cmd}"))

    return tab_column
