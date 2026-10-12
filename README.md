# Arduino MacroKey

Програма для Windows, яка перетворює Arduino (9 кнопок + енкодер) на макро-клавіатуру.
Налаштування кнопок, гарячих клавіш і режимів енкодера — у вікні, програма живе в треї.

## Запуск
```
pip install -r requirements.txt
python main.py
```

## Збірка .exe (на Windows)
```
pyinstaller MacroKey.spec
```
Готовий файл — `dist/MacroKey.exe`. Розповсюджуйте його через GitHub Releases.

Конфіг зберігається в `%APPDATA%\MacroKey\config.json`.
Порт Arduino шукається автоматично, при відключенні програма сама перепідключається.

## Протокол Arduino → ПК (Serial, 9600 бод, рядки з `\n`)
| Рядок | Значення |
|---|---|
| `BUTTON_1`…`BUTTON_9` | натиснуто кнопку |
| `LEFT` / `RIGHT` | поворот енкодера |
| `MODE_V` / `MODE_H` | енкодер у альтернативному / звичайному режимі |
| `GLOBAL_MODE_1`…`3` | активний профіль |

Прошивку заливайте через **Arduino IDE**; вона має слати саме ці рядки.

## Назви клавіш
`ctrl, alt, shift, win, esc, enter, tab, space, del, pgup, pgdn, up/down/left/right, f1…f12`,
медіа: `vol_up, vol_down, mute, next, prev, play`. Комбінації через `+`: `ctrl+shift+esc`.
