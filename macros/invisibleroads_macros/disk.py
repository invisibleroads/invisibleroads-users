import re
import shutil
from contextlib import contextmanager
from os import chdir, getcwd, makedirs, walk
from os.path import dirname, islink, join, normpath, realpath, relpath
from zipfile import ZipFile, ZIP_DEFLATED


def replace_folder(target_folder, source_folder):
    remove_folder(target_folder)
    make_folder(dirname(target_folder))
    shutil.copytree(source_folder, target_folder)
    return target_folder


def clean_folder(folder):
    remove_folder(folder)
    return make_folder(folder)


def remove_folder(folder):
    try:
        shutil.rmtree(folder)
    except OSError:
        pass
    return folder


def make_folder(folder):
    try:
        makedirs(folder)
    except OSError:
        pass
    return folder


def find_path(name, folder):
    for root_folder, folder_names, file_names in walk(folder):
        if name in file_names:
            return join(root_folder, name)


def compress(source_folder, target_path=None):
    source_folder = realpath(source_folder)
    if not target_path:
        target_path = normpath(source_folder) + '.zip'
    with ZipFile(target_path, 'w', ZIP_DEFLATED) as target_zip:
        for root_folder, folder_names, file_names in walk(source_folder):
            for file_name in file_names:
                source_path = join(root_folder, file_name)
                relative_path = relpath(source_path, source_folder)
                resolved_path = realpath(source_path)
                if not resolved_path.startswith(source_folder):
                    # Resolve links whose target is outside source_folder
                    source_path = resolved_path
                elif islink(source_path):
                    # Ignore links whose target is inside source_folder
                    continue
                target_zip.write(source_path, relative_path)
    return target_path


def uncompress(source_path, target_folder=None):
    if not target_folder:
        target_folder = re.sub(r'\.zip$', '', source_path)
    with ZipFile(source_path, 'r') as source_file:
        source_file.extractall(target_folder)
    return target_folder


@contextmanager
def cd(target_folder):
    source_folder = getcwd()
    try:
        chdir(target_folder)
        yield
    finally:
        chdir(source_folder)
