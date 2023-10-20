import os

from . import unittest
from LaravelGoto.lib import workspace


class TestWorkspace(unittest.ViewTestCase):
    def test_get_file_content(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        content = workspace.get_file_content(folder, 'app/Http/Kernel.php')
        self.assertTrue(
            content.__contains__('class Kernel extends HttpKernel')
            )

        content = workspace.get_file_content(__file__)
        self.assertTrue(content.__contains__('TestWorkspace'))

    def test_get_path(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        fullpapth = workspace.get_path(folder, 'app/Http/Kernel.php', True)
        self.assertTrue(fullpapth.__contains__('app/Http/Kernel.php'))

        fullpapth = workspace.get_path(folder, 'unittest.py', True)
        self.assertTrue(fullpapth.__contains__('unittest.py'))

        fullpapth = workspace.get_path(folder, 'sample.php', True)
        self.assertTrue(fullpapth.__contains__('sample.php'))

    def test_get_recursion_files(self):
        folder = os.path.dirname(os.path.abspath(__file__)) +\
            '/fixtures/app/Console/Commands'
        files = workspace.get_recursion_files(folder)
        files.sort()
        self.assertTrue(files[0].endswith('SayGoodbye.php'), files[0])
        self.assertTrue(files[1].endswith('SayHello.php'), files[1])
        self.assertTrue(files[2].endswith('SendEmails.php'), files[2])

    def test_class_2_file(self):
        filename = workspace.class_2_file("\\App\\NS\\SayGoodbye::class,")
        self.assertEqual(filename, 'app/NS/SayGoodbye.php')
