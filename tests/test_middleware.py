import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.middleware import parse, collect_classnames
from LaravelGoto.lib.workspace import get_file_content


class TestMiddleware(unittest.ViewTestCase):
    def test_parse(self):
        content = self.get_kernel()
        middlewares = parse(content)

        self.assertEqual('App/Http/Middleware/Authenticate.php', middlewares.get('auth').path)
        self.assertEqual('Illuminate/Auth/Middleware/AuthenticateWithBasicAuth.php', middlewares.get('auth.basic').path)


    def test_collect_classnames(self):
        classnames = collect_classnames(
            """
            use Illuminate\Foundation\Http\Kernel as HttpKernel;
            use App\Http\Middleware\Authenticate as Auth;
            """
        )

        self.assertEqual("""Illuminate\Foundation\Http\Kernel""", classnames.get('HttpKernel'))
        self.assertEqual("""App\Http\Middleware\Authenticate""", classnames.get('Auth'))
        self.assertEqual(None, classnames.get('Hello'))

