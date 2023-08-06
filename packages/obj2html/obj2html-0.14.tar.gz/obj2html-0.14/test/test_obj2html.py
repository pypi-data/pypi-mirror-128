import unittest
from obj2html import obj2html
import os

class TestObj2Html(unittest.TestCase):
    def setUp(self):
        self.model_assets_path = 'test/assets/model.obj'

    def test_obj2html_without_output_file_path(self):
        string_out = obj2html(self.model_assets_path)

        self.assertTrue(isinstance(string_out, str))

    def test_obj2html_write_html_file(self):
        html_path = '/tmp/index.html'
        if os.path.isfile(html_path):
            os.remove(html_path) 

        self.assertFalse(os.path.isfile(html_path))
        
        obj2html(self.model_assets_path, html_path)

        self.assertTrue(os.path.isfile(html_path))
        os.remove(html_path) 

if __name__ == '__main__':
    unittest.main()
