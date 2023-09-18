import sublime
from re import compile
from .namespace import Namespace
from .place import Place
from .middleware import parse
from . import workspace

config_patterns = [
    compile(r"""Config::[^'"]*(['"])([^'"]*)\1"""),
    compile(r"""config\([^'"]*(['"])([^'"]*)\1"""),
]

lang_patterns = [
    compile(r"""__\([^'"]*(['"])([^'"]*)\1"""),
    compile(r"""@lang\([^'"]*(['"])([^'"]*)\1"""),
    compile(r"""trans\([^'"]*(['"])([^'"]*)\1"""),
    compile(r"""trans_choice\([^'"]*(['"])([^'"]*)\1"""),
]

inertiajs_patterns = [
    compile(r"""Route::inertia\s*\([^,]+,\s*['"]([^'"]+)"""),
    compile(r"""Inertia::render\s*\(\s*['"]([^'"]+)"""),
    compile(r"""inertia\s*\(\s*['"]([^'"]+)"""),
]

livewire_patterns = [
    compile(r"""livewire:([^\s"'>]+)"""),
    compile(r"""@livewire\s*\(\s*['"]([^'"]+)"""),
]


env_pattern = compile(r"""env\(\s*(['"])([^'"]*)\1""")

path_helper_pattern = compile(r"""([\w^_]+)_path\(\s*(['"])([^'"]*)\2""")

find_pattern = """(['"]{1})%s\\1\\s*=>"""

class_controller_pattern = compile(r"""(.+)\.php\s*,\s*["']{1}(.+)""")

component_pattern = compile(r"""<\/?x-([^\/\s>]*)""")

blade_patterns = [
    compile(r"""view\(\s*(['"])([^'"]*)\1"""),
    compile(r"""[lL]ayout\(\s*(['"])([^'"]*)\1"""),
    compile(r"""View::exists\(\s*(['"])([^'"]*)\1"""),
    compile(r"""View::first[^'"]*(['"])([^'"]*)\1"""),
    compile(r"""\$view\s*=\s*(['"])([^'"]*)\1"""),
    compile(r"""view:\s*(['"])([^'"]*)\1"""),
    compile(r"""view\(\s*['"][^'"]*['"],\s*(['"])([^'"]*)\1"""),
    compile(r"""['"]layout['"]\s*=>\s*(['"])([^'"]*)\1"""),
    compile(r"""@include(If\b)?\(\s*(['"])([^'"]*)\2"""),
    compile(r"""@extends\(\s*(['"])([^'"]*)\1"""),
    compile(r"""@include(When|Unless\b)?\([^'"]+(['"])([^'"]+)"""),
    compile(r"""(resources\/views[^\s'"-]+)"""),
]

multi_views_patterns = [
    compile(r"""@includeFirst\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""),
    compile(r"""@each\(['"][^'"]+['"]\s*,[^,]+,[^,]+,[^)]+"""),
]

middleware_patterns = [
    compile(r"""[m|M]iddleware\(\s*\[?\s*(['"][^'"]+['"]\s*,?\s*)+"""),
    compile(r"""['"]middleware['"]\s*=>\s*\s*\[?\s*(['"][^'"]+['"]\s*,?\s*){1,}\]?"""),
]

extensions = []


def init_extensions():
    plugin_settings = sublime.load_settings("LaravelGoto.sublime-settings")
    user_settings = sublime.load_settings("Preferences.sublime-settings")

    # combine extensions
    extensions = user_settings.get("static_extensions", []) +\
        plugin_settings.get("static_extensions", [])
    # make sure extensions are lower case
    globals()['extensions'] = list(map(
        lambda ext: ext.lower(), extensions))


def get_place(selection):
    line = selection.get_line()
    path = selection.get_path()

    places = (
        path_helper_place,
        static_file_place,
        env_place,
        config_place,
        lang_place,
        inertiajs_place,
        livewire_place,
        blade_place,
        component_place,
        middleware_place,
        controller_place,
    )

    for fn in places:
        place = fn(path, line, selection)
        if place:
            return place


def set_controller_action(path, selected, blocks):
    ''' set the controller action '''

    path = path.replace('@', '.php@')
    path = path.replace('::class', '.php')
    if selected.is_class:
        matched = class_controller_pattern.search(path)
        if matched:
            path = matched.group(1) + '.php@' + matched.group(2)

    elif len(blocks) and blocks[0]['is_namespace'] is False:
        """resource or controller route"""
        new_path = blocks[0]['namespace']
        if new_path != path:
            path = new_path + '.php@' + path
        else:
            path = new_path + '.php'

    return path


def set_controller_namespace(path, selection, ns):
    ''' set the controller namespace '''

    if '\\' != path[0] and ns:
        # it's not absolute path namespace, get group namespace
        path = ns + '\\' + path.lstrip('\\')

    return path


def controller_place(path, line, selection):
    namespace = Namespace(selection.view)
    blocks = namespace.get_blocks(selection)
    is_controller = "Controller" in path or selection.is_class

    if is_controller is False and 0 == len(blocks):
        return False

    path = set_controller_action(path, selection, blocks)

    ns = namespace.find(blocks)
    path = set_controller_namespace(path, selection, ns)

    place = Place(path)
    place.is_controller = True
    return place


def config_place(path, line, selected):
    for pattern in config_patterns:
        matcheds = pattern.finditer(line)
        for matched in matcheds:
            if (matched and path == matched.group(2)):
                split = path.split('.')
                path = 'config/' + split[0] + '.php'
                location = None
                if (2 <= len(split)):
                    location = find_pattern % (split[1])
                return Place(path, location)

    return False


def inertiajs_place(path, line, selected):
    for pattern in inertiajs_patterns:
        matched = pattern.search(line)
        if (matched and matched.group(1) in path):
            return Place(matched.group(1))

    return False


def livewire_place(path, line, selected):
    for pattern in livewire_patterns:
        matched = pattern.search(line)
        if (matched):
            path = camel_case(matched.group(1))
            path = path.replace('.', '/') + '.php'
            return Place(path)

    return False


def camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])


def lang_place(path, line, selected):
    for pattern in lang_patterns:
        matched = pattern.search(line)
        if (matched and path == matched.group(2)):
            split = path.split(':')
            vendor = ''
            # it's package trans
            if (3 == len(split)):
                vendor = '/vendor/' + split[0]
            keys = split[-1].split('.')
            path = 'lang' + vendor + '/' + keys[0] + '.php'

            location = None
            if (2 <= len(keys)):
                location = find_pattern % (keys[1])
            return Place(path, location)

    return False


def static_file_place(path, line, selected):
    find = (path.split('.')[-1].lower() in extensions)
    if find is False:
        return False

    # remove dot symbols
    split = list(filter(
        lambda x: x != '..' and x != '.',
        path.split('/')))
    return Place('/'.join(split))


def env_place(path, line, selected):
    matched = env_pattern.search(line)
    find = (matched and path == matched.group(2))
    if find:
        return Place('.env', path)
    return False

def component_place(path, line, selected):
    matched = component_pattern.search(line)
    if matched:
        path = matched.group(1).strip()

        split = path.split(':')
        vendor = ''
        # vendor or namespace
        if (3 == len(split)):
            # vendor probably is lowercase
            if (split[0] == split[0].lower()):
                vendor = split[0] + '/'

        path = split[-1]
        path = vendor + path.replace('.', '/')
        path += '.php'

        return Place(path)


def transform_blade(path):
    split = path.split(':')
    vendor = ''
    # vendor or namespace
    if (3 == len(split)):
        # vendor probably is lowercase
        if (split[0] == split[0].lower()):
            vendor = split[0] + '/'

    path = split[-1]
    path = vendor + path.replace('.', '/')
    if path.endswith('/blade/php'):
        path = path[:-1*len('/blade/php')]

    path += '.blade.php'
    return path

def blade_place(path, line, selected):
    for pattern in blade_patterns:
        matched = pattern.search(line)
        if matched is None:
            continue

        groups = matched.groups()
        if path == groups[-1]:
            path = groups[-1].strip()
            path = transform_blade(path)
            return Place(path)

    for pattern in multi_views_patterns:
        if pattern.search(line):
            path = transform_blade(path)
            return Place(path)

    return False


def path_helper_place(path, line, selected):
    matched = path_helper_pattern.search(line)
    if (matched and path == matched.group(3)):
        prefix = matched.group(1) + '/'
        if 'base/' == prefix:
            prefix = ''
        elif 'resource/' == prefix:
            prefix = 'resources/'

        return Place(prefix + path)
    return False

def middleware_place(path, line, selected):
    kernel_content = None
    for folder in workspace.get_folders():
        kernel_content = workspace.get_file_content(folder, 'app/Http/Kernel.php')
        if kernel_content:
            break
    if not kernel_content:
        return False

    middlewares = parse(kernel_content)

    for pattern in middleware_patterns:
        matched = pattern.search(line)
        if not matched:
            continue
        # remove middleware parameters
        alias = path.split(':')[0]
        place = middlewares.get(alias)
        if place:
            return place
