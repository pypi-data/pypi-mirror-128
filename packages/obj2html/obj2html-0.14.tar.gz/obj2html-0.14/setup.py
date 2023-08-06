from distutils.core import setup

import os
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pipy_readme.rst'), 'r') as f:
  long_des = f.read()

setup(
  name = 'obj2html',
  packages = ['obj2html'],
  version = '0.14',
  license='MIT',
  description = 'Create an html with three.js that contains the given .obj file.',
  long_description = long_des,
  author = 'Nicola Landro',
  author_email = 'nicolaxx94@live.it',
  url = 'https://gitlab.com/nicolalandro/obj2html',
  keywords = ['3D', '.obj', '.html', 'jupyter', '3D viewer'],
  project_urls={
    'Source': 'https://gitlab.com/nicolalandro/obj2html',
  },
  include_package_data = True,
  package_data = {
    '' : ['*.html'],
  }
)