"""Вставляет актуальные исходники игры в конец PROMPT.md.

Запускать из папки игры после ЛЮБОГО изменения index.html, style.css или script.js:

    python tools/build_prompt.py

Скрипт заменяет всё между метками SOURCES:START и SOURCES:END,
поэтому исходники в PROMPT.md всегда совпадают с файлами игры.
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')  # русский текст в консоли Windows

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ROOT / 'PROMPT.md'
START = '<!-- SOURCES:START -->'
END = '<!-- SOURCES:END -->'

# Файл и язык для подсветки в markdown
FILES = [
    ('index.html', 'html'),
    ('style.css', 'css'),
    ('script.js', 'javascript'),
]


def build_sources():
    parts = [START, '', '<!-- Этот раздел создаётся скриптом tools/build_prompt.py — не редактируйте вручную -->', '']
    for name, lang in FILES:
        code = (ROOT / name).read_text(encoding='utf-8').replace('\r\n', '\n').rstrip('\n')
        if '````' in code:
            raise SystemExit(f'{name}: в коде есть ````, блок markdown сломается')
        parts += [f'### `{name}`', '', f'````{lang}', code, '````', '']
    parts.append(END)
    return '\n'.join(parts)


def main():
    text = PROMPT.read_text(encoding='utf-8').replace('\r\n', '\n')
    if START not in text or END not in text:
        raise SystemExit('В PROMPT.md нет меток SOURCES:START / SOURCES:END')
    before = text.split(START)[0]
    after = text.split(END, 1)[1]
    PROMPT.write_text(before + build_sources() + after, encoding='utf-8', newline='\n')
    print('PROMPT.md обновлён: исходники вставлены')


if __name__ == '__main__':
    main()
