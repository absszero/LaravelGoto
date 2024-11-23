from . import unittest
from LaravelGoto.lib.inertia import Inertia


class TestInertia(unittest.ViewTestCase):
    inertia = Inertia()

    def test_inertia_function(self):
        place = self.inertia.get_place(
            'About/AboutComponent',
            """inertia("About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)

        place = self.inertia.get_place(
            'About/AboutComponent',
            """inertia(component: "About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)

    def test_inertia_render(self):
        place = self.inertia.get_place(
            'About/AboutComponent',
            """Inertia::render("About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)

        place = self.inertia.get_place(
            'About/AboutComponent',
            """Inertia::render(component: "About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)

    def test_inertia_route(self):
        place = self.inertia.get_place(
            'About/AboutComponent',
            """Route::inertia("/about", "About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)

        place = self.inertia.get_place(
            'About/AboutComponent',
            """Route::inertia("/about", component: "About/AboutComponent");""")
        self.assertEqual("About/AboutComponent", place.path)
