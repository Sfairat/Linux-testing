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