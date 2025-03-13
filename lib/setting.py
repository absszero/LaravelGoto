import sublime

settings = None
extensions = None


class Setting:

    def __init__(self):
        global settings, extensions
        if not settings:
            settings = sublime.load_settings('LaravelGoto.sublime-settings')

            extensions = settings.get('default_static_extensions')
            exts = settings.get('static_extensions')
            if exts:
                extensions += exts

            # make sure extensions are lower case
            extensions = list(
                map(lambda ext: ext.lower(), extensions))

    def get(self, name):
        return settings.get(name)

    def exts(self):
        return extensions
