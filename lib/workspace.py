from pathlib import Path
import os
import sublime

mTimes = {}
contents = {}
changes = {}


def is_file(base, filename=None):
    fullpath = base
    if filename:
        fullpath = os.path.join([base, filename])
    return os.path.isfile(fullpath)


def is_changed(folder_path, file_path=None):
    '''
    is the folder's files were changed
    :param file_path only check the file in the folder
    '''

    if file_path:
        if not file_path.startswith(folder_path):
            return False

        mTime = os.path.getmtime(file_path)
        return mTimes.get(file_path) != mTime

    if folder_path not in changes:
        return True
    with os.scandir(folder_path) as entries:
        files = [entry for entry in entries if entry.is_file() or entry.is_dir()]
    if changes[folder_path] != len(files):
        return True
    for entry in files:
        fullpath = entry.path
        mTime = os.path.getmtime(fullpath)
        if mTimes.get(fullpath) != mTime:
            return True

    return False


def set_unchanged(folder_path):
    '''
    set the folder's files is changed
    '''

    with os.scandir(folder_path) as entries:
        files = [entry.name for entry in entries if entry.is_file() or entry.is_dir()]
    changes[folder_path] = len(files)

    for file in files:
        fullpath = os.path.join(folder_path, file)
        mTime = os.path.getmtime(fullpath)
        mTimes[fullpath] = mTime


def get_file_content(base, file_path=None):
    fullpath = base
    if file_path:
        fullpath = get_path(base, file_path)
    if not fullpath:
        return
    if not os.path.isfile(fullpath):
        return

    mTime = os.path.getmtime(fullpath)
    # from cache
    if mTimes.get(fullpath) == mTime:
        return contents.get(fullpath)

    # from disk
    with open(fullpath, mode="r", encoding="utf-8") as f:
        content = f.read()
        mTimes[fullpath] = mTime
        contents[fullpath] = content
        return content


def get_recursion_files(folder, ext='.php'):
    '''
    get all files including sub-dirs with the extension
    '''
    files = []
    p = Path(folder)
    for file in p.rglob(f'*{ext}'):
        if file.is_file():
            files.append(str(file))
    return files


def get_folder_path(base, folder_name, recursion=True):
    '''
    get real path by folder name
    '''

    star = None
    folders = folder_name.split('/')
    if '*' == folders[-1]:
        star = folders.pop()
    folder_path = '/'.join(folders)

    full_folder_path = os.path.join(base, folder_path)
    if os.path.isdir(full_folder_path):
        if not star:
            return full_folder_path

        folders = []
        with os.scandir(full_folder_path) as entries:
            for entry in entries:
                if entry.is_dir():
                    folders.append(entry.path)

        return folders

    if not recursion:
        return

    with os.scandir(base) as entries:
        for entry in entries:
            if not entry.is_dir():
                continue

            folder = entry.path
            fullpath = get_folder_path(folder, folder_name, False)
            if fullpath:
                return fullpath


def get_path(base, file_path, recursion=True):
    '''
    get real path by a part of file path
    '''
    top_dir = None
    if '/' in file_path:
        top_dir = file_path.split('/')[0]

    with os.scandir(base) as entries:
        files = [entry.name for entry in entries]
    if not top_dir and file_path in files:
        fullpath = os.path.join(base, file_path)
        if os.path.isfile(fullpath):
            return fullpath
        return None

    for file in files:
        if os.path.isdir(base + '/' + file) is False:
            continue

        # if not the right dictionary, search the sub dictionaries
        if top_dir != file:
            if recursion:
                fullpath = get_path(base + '/' + file, file_path, False)
                if fullpath:
                    return fullpath
            continue

        fullpath = os.path.join(base, file_path)
        if os.path.isfile(fullpath):
            return fullpath


def get_folders():
    return sublime.active_window().folders()


def class_2_file(class_name):
    '''
    convert PHP class name to filename
    '''
    filename = class_name.replace(',', '').replace('::class', '')
    filename = filename.replace('\\', '/').strip() + '.php'
    if filename.startswith('/'):
        filename = filename[1:]

    if filename.startswith('App/'):
        filename = filename.replace('App/', 'app/', 1)

    return filename
