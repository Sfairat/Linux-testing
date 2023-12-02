import datetime
import pytest
import yaml
from engine import find_text, get_hash
import os

with open('config.yaml', encoding='UTF-8') as f:
    data = yaml.safe_load(f)


@pytest.fixture(scope='class')
def make_folders():
    return find_text(f'mkdir -p {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ex")}', '')


@pytest.fixture(scope='class')
def delete_folders():
    yield
    return find_text(f'rm -rf {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ex")}', '')


@pytest.fixture(scope='class')
def make_files():
    return find_text(f'cd {data.get("folder_in")}; touch file_1.txt file_2.txt file_3.txt', '')


@pytest.fixture(autouse=True)
def add_stat():
    with open('stat.txt', 'a') as file:
        time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        file_size = os.path.getsize('config.yaml')
        with open('/proc/loadavg', 'r') as f:
            cpu_stat = f.read()
        stat = f'{time}, {file_size}, {cpu_stat}\n'
        file.write(stat)


@pytest.mark.usefixtures('make_folders', 'make_files', 'delete_folders')
class TestFolder:

    def test_step_1(self):
        assert find_text(f'cd {data.get("folder_in")}; 7z a -t{data.get("type")} '
                         f'{data.get("folder_out")}/archive_1', 'Everything is Ok')

    def test_step_2(self):
        assert find_text(f'cd {data.get("folder_out")}; 7z rn -t{data.get("type")} '
                         f'archive_1 file_1.txt file_100.txt', 'Everything is Ok')

    def test_step_3(self):
        assert find_text(f'cd {data.get("folder_out")}; 7z i -t{data.get("type")} '
                         f'archive_1', ' 0  ED  6F00181 AES256CBC')

    def test_step_4(self):
        output = str(get_hash(f'{data.get("folder_out")}/archive_1.7z')).upper()[2:]
        assert find_text(f'cd {data.get("folder_out")}; 7z h -t{data.get("type")} archive_1.7z', output)

    def test_step_5(self):
        assert find_text(f'cd {data.get("folder_out")}; 7z l -t{data.get("type")} archive_1.7z', '3 files')

    def test_step_6(self):
        assert find_text(f'cd {data.get("folder_out")}; 7z x -t{data.get("type")} archive_1.7z', 'Everything is Ok')


if __name__ == '__main__':
    pytest.main(['-vv'])
