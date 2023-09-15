import sublime
import re
from .place import Place


def parse(content):
    middlewares = {}
    # Before Laravel 10, middlewareAliases was called routeMiddleware. They work the exact same way.
    aliasPattern = """(\$\\bmiddlewareAliases\\b|\$\\brouteMiddleware\\b)\s*=\s*\[([^;]+)"""

    match = re.search(aliasPattern, content, re.M)
    if match is None:
        return middlewares;

    classnames = collect_classnames(content)


    pattern = re.compile("""['"]([^'"]+)['"]\s*=>\s*([^,\]]+)""")
    for match in pattern.findall(match.group()):
        classname = match[1].replace('::class', '').strip()
        if classnames.get(classname):
            classname = classnames.get(classname)
        classname = classname.replace('\\', '/') + '.php'

        if classname.startswith('/'):
            classname = classname[1:]

        middlewares[match[0]] = Place(classname)

    return middlewares



def collect_classnames(content):
    classnames = {}
    pattern = re.compile("""use\s+([^\s]+)\s+as+\s+([^;]+)""")
    for match in pattern.findall(content):
        classnames[match[1]] = match[0].strip()

    return classnames;
