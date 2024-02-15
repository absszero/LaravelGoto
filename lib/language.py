import os
from . import workspace
from .logging import info
from .place import Place


routes = {}


class Language:
    find_pattern = """(['"]{1})%s\\1\\s*=>"""
    FILENAME = 'lang/%(vendor)s%(file)s.php'
    LANG_FILENAME = '%(vendor)s%(lang)s/%(file)s.php'

    def __init__(self):
        self.base = None
        self.langs = {}

        for folder in workspace.get_folders():
            dir = workspace.get_folder_path(folder, 'lang')
            if not dir:
                continue

            self.base = dir
            self.langs = {}
            dirs = os.listdir(dir)
            for dir in dirs:
                if os.path.isdir(os.path.join(self.base, dir)):
                    self.langs[dir] = True
                elif dir.endswith('.json'):
                    self.langs[dir] = False
            info('lang base', self.base)
            info('langs', self.langs)
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
        locations = {}
        for lang, is_dir in self.langs.items():
            lang_path = lang
            if is_dir:
                lang_path = self.LANG_FILENAME % {
                    'vendor': vendor,
                    'lang': lang,
                    'file': keys[0],
                }
            else:
                jsonKey = '\\.'.join(keys)
                locations[lang] = jsonKey
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
        place.locations = locations

        return place
