import sublime
from fnmatch import filter
from glob import glob
from os import path
from os import walk

mTimes = {}
contents = {}

def get_file_content(folder, filepath):
    # folders = sublime.active_window().folders()
    for cwd, subfolders, filenames in walk(folder):
        for filename in filenames:
            fullpath = path.join(cwd, filename)
            if fullpath.endswith(filepath):
                mTime = path.getmtime(fullpath)
                # from cache
                if mTimes.get(fullpath) == mTime:
                    return contents[fullpath];

                # from disk
                with open(fullpath, 'r') as f:
                    content = f.read()
                    mTimes[fullpath] = mTime
                    contents[fullpath] = contents
                    return content
