# Написать функцию на Python, которой передаются в качестве параметров команда и текст.
# Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False в противном случае.
# Передаваться должна только одна строка, разбиение вывода использовать не нужно.

import subprocess


def find_text(command: str, text: str):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
    out = result.stdout
    if result.returncode == 0:
        if text in out:
            return True
        else:
            return False


print(find_text('cat /etc/os-release', 'jammy'))
