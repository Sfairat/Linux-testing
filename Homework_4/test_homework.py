import pytest
import yaml
import os
import datetime
from sshcheckers import upload_files, ssh_checkout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(scope='class')
def make_folders():
    return ssh_checkout(f"{data['host']}",
                        f"{data['user']}",
                        f"{data['pswd']}",
                        f"mkdir -p {data['folder_in']} {data['folder_out']}",
                        " ")


@pytest.fixture(scope='class')
def make_files():
    return ssh_checkout(f"{data['host']}",
                        f"{data['user']}",
                        f"{data['pswd']}",
                        f"cd {data.get('folder_in')}; touch file_1.txt file_2.txt file_3.txt",
                        " ")


@pytest.fixture(scope='class')
def delete_folders():
    yield
    return ssh_checkout(f"{data['host']}",
                        f"{data['user']}",
                        f"{data['pswd']}",
                        f"rm -rf {data.get('folder_in')} {data.get('folder_out')}",
                        " ")


@pytest.fixture(scope='class')
def delete_package():
    yield
    return ssh_checkout(f'{data.get("host")}',
                        f'{data.get("user")}',
                        f'{data.get("pswd")}',
                        f'echo {data.get("pswd")} | sudo -S dpkg -r {data.get("folder_out")}{data.get("file")}',
                        "")


@pytest.fixture(autouse=True)
def add_stat():
    with open('stat.txt', 'a') as file:
        time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        file_size = os.path.getsize('config.yaml')
        with open('/proc/loadavg', 'r') as f:
            cpu_stat = f.read()
        stat = f'{time}, {file_size}, {cpu_stat}'
        file.write(stat)


@pytest.mark.usefixtures('make_folders', 'make_files', 'delete_folders', 'delete_package')
class TestHomework:

    def test_step_1(self):
        result_1 = ssh_checkout(f"{data.get('host')}",
                                f"{data.get('user')}",
                                f"{data.get('pswd')}",
                                f"cd {data.get('folder_in')}; 7z a {data.get('folder_out')}/archive_1",
                                f"Everything is Ok")
        assert result_1 == True

    def test_step_2(self):
        result_1 = ssh_checkout(f"{data.get('host')}",
                                f"{data.get('user')}",
                                f"{data.get('pswd')}",
                                f"cd {data.get('folder_out')}; 7z l archive_1.7z",
                                f"3 files")
        assert result_1 == True

    def test_step_3(self):
        upload_files(f'{data.get("host")}',
                     f'{data.get("user")}',
                     f'{data.get("pswd")}',
                     f'{data.get("folder_downloads")}{data.get("file")}.deb',
                     f'{data.get("folder_out")}{data.get("file")}.deb')
        result_1 = ssh_checkout(f'{data.get("host")}',
                                f'{data.get("user")}',
                                f'{data.get("pswd")}',
                                f'echo {data.get("pswd")} | sudo -S dpkg -i {data.get("folder_out")}{data.get("file")}.deb',
                                "Setting up")
        result_2 = ssh_checkout(f'{data.get("host")}',
                                f'{data.get("user")}',
                                f'{data.get("pswd")}',
                                f'echo {data.get("pswd")} | sudo -S dpkg -s {data.get("file")}',
                                f"Status: install ok installed")
        assert result_1, result_2 == True

    def test_step_4(self):
        result_1 = ssh_checkout(f"{data.get('host')}",
                                f"{data.get('user')}",
                                f"{data.get('pswd')}",
                                f"cd {data.get('folder_out')}; 7z x archive_1.7z",
                                f"Everything is Ok")
        assert result_1 == True


if __name__ == '__main__':
    pytest.main(['-vv'])
