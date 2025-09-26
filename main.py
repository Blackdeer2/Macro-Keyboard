import flet as ft
from hotkeys import press_combo
from encoder_mode import EncoderMode
from arduino_button import ArduinoButton

# Створюємо кнопки і режими
buttons = []
for i in range(1, 10):
    mode = EncoderMode(name=f"Mode_{i}", left_cmd="left", right_cmd="right")
    btn = ArduinoButton(name=f"BUTTON_{i}", hotkey="", encoder_mode=mode)
    buttons.append(btn)

def main(page: ft.Page):
    page.title = "Arduino Hotkeys + Encoder Modes"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Колонка з прокруткою
    scroll_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10, expand=True)

    for btn in buttons:
        # Поле для гарячої клавіші
        hotkey_field = ft.TextField(label=f"{btn.name} Hotkey", width=250, value=btn.hotkey)

        # Поля для енкодера
        left_field = ft.TextField(label="Left Command", width=250, value=btn.encoder_mode.left_cmd)
        right_field = ft.TextField(label="Right Command", width=250, value=btn.encoder_mode.right_cmd)
        alt_left_field = ft.TextField(label="Alt Left", width=250, value=btn.encoder_mode.alt_left_cmd)
        alt_right_field = ft.TextField(label="Alt Right", width=250, value=btn.encoder_mode.alt_right_cmd)

        def save_btn(e, b=btn, hf=hotkey_field, lf=left_field, rf=right_field, alf=alt_left_field, arf=alt_right_field):
            b.hotkey = hf.value.strip()
            b.encoder_mode.left_cmd = lf.value.strip()
            b.encoder_mode.right_cmd = rf.value.strip()
            b.encoder_mode.alt_left_cmd = alf.value.strip()
            b.encoder_mode.alt_right_cmd = arf.value.strip()
            page.snack_bar = ft.SnackBar(ft.Text(f"{b.name} збережено ✅"))
            page.snack_bar.open = True
            page.update()

        save_button = ft.ElevatedButton(text="Зберегти", on_click=save_btn)

        scroll_column.controls.extend([
            hotkey_field,
            left_field,
            right_field,
            alt_left_field,
            alt_right_field,
            save_button,
            ft.Divider()
        ])

    # Додаємо колонку на сторінку
    page.add(scroll_column)

if __name__ == "__main__":
    ft.app(target=main)
