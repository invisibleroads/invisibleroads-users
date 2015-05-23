import fnmatch
import re
import shutil
import subprocess
from contextlib import contextmanager
from glob import glob
from os import chdir, getcwd, makedirs, walk
from os.path import abspath, dirname, islink, join, normpath, realpath, relpath
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
    raise IOError('cannot find "%s" in "%s"' % (name, folder))


def find_paths(name_expression, folder):
    return [
        join(root_folder, file_name)
        for root_folder, folder_names, file_names in walk(folder)
        for file_name in fnmatch.filter(file_names, name_expression)]


def resolve_relative_path(relative_path, folder):
    relative_path = relpath(join(folder, relative_path), folder)
    if relative_path.startswith('..'):
        raise IOError('relative_path must refer to a file inside folder')
    return join(folder, relative_path)


def compress(source_folder, target_path=None):
    if not target_path or target_path.endswith('.tar.gz'):
        return compress_tar(source_folder, target_path)
    return compress_zip(source_folder, target_path)


def compress_tar(source_folder, target_path=None):
    if not target_path:
        target_path = normpath(source_folder) + '.tar.gz'
    target_path = abspath(target_path)
    command_terms = ['tar', 'czhf']
    with cd(source_folder):
        source_paths = glob('*')
        if not source_paths:
            raise IOError('cannot compress empty folder "%s"' % source_folder)
        subprocess.check_output(command_terms + [target_path] + source_paths)
    return target_path


def compress_zip(source_folder, target_path=None):
    if not target_path:
        target_path = normpath(source_folder) + '.zip'
    source_folder = realpath(source_folder)
    with ZipFile(
        target_path, 'w', ZIP_DEFLATED, allowZip64=True,
    ) as target_zip:
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
    if source_path.endswith('.tar.gz'):
        return _uncompress_tar(source_path, target_folder)
    if source_path.endswith('.zip'):
        return _uncompress_zip(source_path, target_folder)


def _uncompress_tar(source_path, target_folder=None):
    if not target_folder:
        target_folder = re.sub(r'\.tar.gz$', '', source_path)
    command_terms = ['tar', 'xf', source_path, '-C']
    subprocess.check_output(command_terms + [make_folder(target_folder)])
    return target_folder


def _uncompress_zip(source_path, target_folder=None):
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
