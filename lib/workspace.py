import sublime
import os
from glob import glob


mTimes = {}
contents = {}

def get_file_content(folder, filepath):
    fullpath = get_path(folder, filepath, True)
    if fullpath:
        mTime = os.path.getmtime(fullpath)
        # from cache
        if mTimes.get(fullpath) == mTime:
            return contents.get(fullpath);

        # from disk
        with open(fullpath, mode = "r", encoding = "utf-8") as f:
            content = f.read()
            mTimes[fullpath] = mTime
            contents[fullpath] = content
            return content

def get_path(folder, filepath, recursion = False):
    top_dir = filepath.split('/')[0];

    for file in os.listdir(folder):
        if os.path.isdir(folder + '/' + file) is False:
            continue

        ## if not the right dictionary, search the sub dictionaries
        if top_dir != file:
            if recursion:
                fullpath = get_path(folder + '/' + file, filepath)
                if fullpath:
                    return fullpath;
            continue

        fullpath = os.path.join(folder, filepath)
        if os.path.isfile(fullpath):
            return fullpath;
