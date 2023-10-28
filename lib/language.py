import os
from . import workspace
from .logging import log
from .place import Place


routes = {}


class Language:
    find_pattern = """(['"]{1})%s\\1\\s*=>"""
    FILENAME = 'lang/%(vendor)s%(file)s.php'
    LANG_FILENAME = '%(vendor)s%(lang)s/%(file)s.php'

    def __init__(self):
        self.base = None
        self.langs = []

        for folder in workspace.get_folders():
            dirs = workspace.get_folder_path(folder, 'resources/lang/*')
            if dirs:
                self.base = os.path.dirname(dirs[0])
                self.langs = []
                for dir in dirs:
                    self.langs.append(os.path.basename(dir))
                log('lang base', self.base)
                log('langs', self.langs)
                return

    def get_place(self, path):
        split = path.split(':')
        vendor = ''
        # it's package trans
        if (3 == len(split)):
            vendor = 'vendor/' + split[0] + '/'
        keys = split[-1].split('.')
        path = self.FILENAME % {'vendor': vendor, 'file': keys[0]}

        uris = []
        paths = []
        for lang in self.langs:
            lang_path = self.LANG_FILENAME % {
                'vendor': vendor,
                'lang': lang,
                'file': keys[0],
            }
            paths.append('lang/' + lang_path)

            uri = os.path.join(self.base, lang_path)
            if workspace.is_file(uri):
                uris.append(uri)

        location = None
        if (2 <= len(keys)):
            location = self.find_pattern % (keys[1])

        place = Place(path, location)
        place.paths = paths
        place.paths.sort()
        place.uris = uris

        return place
