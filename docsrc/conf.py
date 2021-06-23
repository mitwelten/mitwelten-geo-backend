import sys
import os

sys.path.insert(0, os.path.abspath('..'))

project = 'Mitwelten'

extensions = [
#    'sphinx.ext.extlinks',
    'sphinx.ext.autodoc',
    'sphinxarg.ext',
#    'sphinx.ext.todo',
#    'sphinx.ext.mathjax',
#    'sphinx.ext.viewcode',
#    'sphinx.ext.napoleon',
#    'pywps.ext_autodoc'
]

exclude_patterns = ['_build']
source_suffix = '.rst'
master_doc = 'index'

pygments_style = 'sphinx'

#html_static_path = ['_static']

htmlhelp_basename = 'MWdoc'
 
