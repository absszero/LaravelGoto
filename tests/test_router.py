
from unittest.mock import patch
from . import unittest
from LaravelGoto.lib.router import Router


class TestRouter(unittest.ViewTestCase):
    @patch('subprocess.check_output')
    @patch('LaravelGoto.lib.workspace.get_path')
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_all(self, mock_get_folders, mock_get_path, mock_check_output):
        mock_get_folders.return_value = [self.get_test_dir()]
        mock_get_path.return_value = 'artisan'
        mock_check_output.return_value = bytes('[{"name":"admin.index","action":"App\\\\Http\\\\Controllers\\\\AdminController@index","middleware":[]},{"name":null,"action":"Closure","middleware":[]},{"name":null,"action":"Closure","middleware":[]}]', 'utf-8')  # noqa: E501

        router = Router()
        routes = router.all()

        self.assertEqual(
            routes.get("admin.index").path,
            'app/Http/Controllers/AdminController.php'
            )
