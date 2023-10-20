import os
import sublime

mTimes = {}
contents = {}


def get_file_content(folder, filepath=None):
    fullpath = folder
    if filepath:
        fullpath = get_path(folder, filepath, True)
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
    files = []
    for folder, subfolders, filenames in os.walk(folder):
        for filename in filenames:
            if filename.endswith(ext):
                files.append(os.path.join(folder, filename))
    return files


def get_path(folder, filepath, recursion=False):
    top_dir = None
    if '/' in filepath:
        top_dir = filepath.split('/')[0]

    files = os.listdir(folder)
    if not top_dir and filepath in files:
        fullpath = os.path.join(folder, filepath)
        if os.path.isfile(fullpath):
            return fullpath
        return None

    for file in files:
        if os.path.isdir(folder + '/' + file) is False:
            continue

        # if not the right dictionary, search the sub dictionaries
        if top_dir != file:
            if recursion:
                fullpath = get_path(folder + '/' + file, filepath)
                if fullpath:
                    return fullpath
            continue

        fullpath = os.path.join(folder, filepath)
        if os.path.isfile(fullpath):
            return fullpath


def get_folders():
    return sublime.active_window().folders()


def class_2_file(class_name):
    class_name = class_name
    filename = class_name.replace(',', '').replace('::class', '')
    filename = filename.replace('\\', '/').strip() + '.php'
    if filename.startswith('/'):
        filename = filename[1:]

    if filename.startswith('App/'):
        filename = filename.replace('App/', 'app/', 1)

    return filename
