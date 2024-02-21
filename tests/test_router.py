
from unittest.mock import patch
from . import unittest
from LaravelGoto.lib.router import Router


class TestRouter(unittest.ViewTestCase):
    @patch('subprocess.check_output')
    @patch('LaravelGoto.lib.workspace.set_unchanged')
    @patch('LaravelGoto.lib.workspace.is_changed')
    @patch('LaravelGoto.lib.workspace.get_path')
    @patch('LaravelGoto.lib.workspace.get_folder_path')
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_all(
        self,
        m_get_folders,
        m_get_folder_path,
        m_get_path,
        m_is_changed,
        m_set_unchanged,
        m_check_output
    ):
        m_get_folders.return_value = [self.get_test_dir()]
        m_get_folder_path.return_value = 'dir'
        m_get_path.return_value = 'artisan'
        m_is_changed.return_value = True
        m_set_unchanged.return_value = None
        m_check_output.return_value = bytes('[{"name":"admin.index","action":"App\\\\Http\\\\Controllers\\\\AdminController@index","middleware":[]},{"name":null,"action":"Closure","middleware":[]},{"name":null,"action":"Closure","middleware":[]}]', 'utf-8')

        router = Router()
        router.update()
        routes = router.all()

        self.assertEqual(
            routes.get("admin.index").path,
            'app/Http/Controllers/AdminController.php'
            )
