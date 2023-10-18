from unittest.mock import patch
from . import unittest
from LaravelGoto.lib.middleware import Middleware


class TestMiddleware(unittest.ViewTestCase):
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_all(self, mock_get_folders):
        mock_get_folders.return_value = [self.get_test_dir()]

        middleware = Middleware()
        middlewares = middleware.all()

        self.assertEqual(
            middlewares.get('auth').path,
            'App/Http/Middleware/Authenticate.php'
            )
        self.assertEqual(
            middlewares.get('auth.basic').path,
            'Illuminate/Auth/Middleware/AuthenticateWithBasicAuth.php'
            )

    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_collect_classnames(self, mock_get_folders):
        mock_get_folders.return_value = [self.get_test_dir()]
        middleware = Middleware()
        classnames = middleware.collect_classnames(
            """
            use Illuminate\\Foundation\\Http\\Kernel as HttpKernel;
            use App\\Http\\Middleware\\Authenticate as Auth;
            """
        )

        self.assertEqual(
            classnames.get('HttpKernel'),
            """Illuminate\\Foundation\\Http\\Kernel"""
            )
        self.assertEqual(
            classnames.get('Auth'),
            """App\\Http\\Middleware\\Authenticate"""
            )
        self.assertEqual(classnames.get('Hello'), None)
