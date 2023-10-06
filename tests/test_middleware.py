import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.middleware import Middleware


class TestMiddleware(unittest.ViewTestCase):
    def test_all(self):
        middleware = Middleware(self.get_http_kernel())
        middlewares = middleware.all()

        self.assertEqual('App/Http/Middleware/Authenticate.php', middlewares.get('auth').path)
        self.assertEqual('Illuminate/Auth/Middleware/AuthenticateWithBasicAuth.php', middlewares.get('auth.basic').path)


    def test_collect_classnames(self):
        middleware = Middleware(self.get_http_kernel())
        classnames = middleware.collect_classnames(
            """
            use Illuminate\Foundation\Http\Kernel as HttpKernel;
            use App\Http\Middleware\Authenticate as Auth;
            """
        )

        self.assertEqual("""Illuminate\Foundation\Http\Kernel""", classnames.get('HttpKernel'))
        self.assertEqual("""App\Http\Middleware\Authenticate""", classnames.get('Auth'))
        self.assertEqual(None, classnames.get('Hello'))

