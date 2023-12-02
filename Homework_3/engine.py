# Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее созданный файл stat.txt строку вида:
# время, кол-во файлов из конфига, размер файла из конфига, статистика загрузки процессора из файла /proc/loadavg
# (можно писать просто всё содержимое этого файла).
# Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг.

import subprocess
import zlib


def find_text(command: str, text: str):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
    out = result.stdout
    if result.returncode == 0:
        if text in out:
            return True
        else:
            return False


def get_hash(path):
    with open(path, 'rb') as f:
        data = f.read()
    return hex(zlib.crc32(data))
