import os
import sys

BASE_DIR = os.getcwd()  # 当前文件夹地址
ALL_CONTENT = os.walk(BASE_DIR)  # 当前文件夹下所有文件
ALL_COUNT = 0  # 总行数


def path_with_file(filetype):
    """
    return
    _[0]    :   filepath
    i       :   filename
    """
    for _ in ALL_CONTENT:

        if "site-packages" in _[0]:
            continue

        for i in _[2]:
            if i.endswith(filetype):
                yield _[0], i


def main(sysfile='count.py', filetype='py', ignore_path=None):
    global ALL_COUNT

    _ = "." + filetype
    for filepath, filename in path_with_file(_):

        if isinstance(ignore_path, list):
            for ignore in ignore_path:
                if ignore in filepath:
                    break
            else:
                if filename == sysfile:
                    continue

                os.chdir(filepath)

                with open(filename, 'r', encoding='utf-8') as f:
                    _ = len(f.readlines())
                    ALL_COUNT += _

                    print(f"当前{filepath}目录下{filename}文件包含行数为：{_}")

                os.chdir(BASE_DIR)

                with open('log.txt', 'a', encoding='utf-8') as f:
                    f.write(f"当前{filepath}目录下{filename}文件包含行数为：{_}\n")

    with open('log.txt', 'a', encoding='utf-8') as f:
        f.write(f"总行数为:{ALL_COUNT}\n")

    print(f"总行数为:{ALL_COUNT}")


if __name__ == "__main__":
    try:
        sysfile = sys.argv[0]
        filetype = sys.argv[1]
    except Exception as e:
        main(ignore_path=['migrations'])
    else:
        main(sysfile, filetype, ['migrations'])
