from . import unittest
from LaravelGoto.lib.livewire import Livewire


class testLivewire(unittest.ViewTestCase):
    livewire = Livewire()

    def test_blade_tag(self):
        place = self.livewire.get_place(
            'nav.show-post',
            """<livewire:nav.show-post>""")
        self.assertEqual("Nav/ShowPost.php", place.path)

    def test_directive(self):
        place = self.livewire.get_place(
            'nav.show-post',
            """@livewire("nav.show-post")""")
        self.assertEqual("Nav/ShowPost.php", place.path)
