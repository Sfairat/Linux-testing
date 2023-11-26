# Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы,
# в котором вывод разбивается на слова с удалением всех знаков пунктуации
# (их можно взять из списка string.punctuation модуля string). В этом режиме должно проверяться наличие слова в выводе.
import string
import subprocess


def find_text(command: str, text: str):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='UTF-8')
    out = result.stdout.replace('\n', '')
    out_result = ''
    for i in out:
        if i not in string.punctuation:
            out_result += i

    if result.returncode == 0:
        if text in out_result:
            return True
        else:
            return False


print(find_text('cat /etc/os-release', 'UBUNTU_CODENAME=jammy'))
print(find_text('cat /etc/os-release', 'UBUNTUCODENAMEjammy'))
