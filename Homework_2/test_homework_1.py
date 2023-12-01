# Дополнить проект тестами, проверяющими команды вывода списка файлов (l)
# и разархивирования с путями (x).
# Доработать проект, добавив тест команды расчёта хеша (h).
# Проверить, что хеш совпадает с рассчитанным командой crc32.

import pytest
from Homework.Homework_1.task1 import find_text

folder_in = '/home/alex/folder_in'
folder_out = '/home/alex/folder_out'


def test_step_1():
    assert find_text(f'cd {folder_in}; 7z a {folder_out}/archive_1', 'Everything is Ok')


def test_step_2():
    assert find_text(f'cd {folder_out}; 7z l archive_1.7z', 'Physical Size = 150')


def test_step_3():
    assert find_text(f'cd {folder_out}; 7z x archive_1.7z', 'Everything is Ok')


def test_step_4():
    assert find_text(f'cd {folder_out}; 7z h archive_1.7z', '5B74D363')


def test_step_5():
    assert find_text(f'cd {folder_out}; 7z d archive_1.7z', 'Everything is Ok')


if __name__ == '__main__':
    pytest.main(['-vv'])
