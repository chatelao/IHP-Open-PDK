# Configuration file for the Sphinx documentation builder.

project = 'IHP SG13G2 Open PDK'
copyright = '2025, IHP PDK Authors'
author = 'IHP PDK Authors'
release = '0.0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx_symbiflow_theme',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_symbiflow_theme'

html_logo = '_static/logo.png'

html_theme_options = {
    'nav_title': 'IHP SG13G2 Open PDK',

    'color_primary': 'red',
    'color_accent': 'red',

    # Set the repo location to get a badge with stats
    'github_url': 'https://github.com/IHP-GmbH/IHP-Open-PDK',
    'repo_name': 'IHP-GmbH/IHP-Open-PDK',

    'globaltoc_depth': 4,
    'globaltoc_collapse': False,

    # Hide the symbiflow links
    'hide_symbiflow_links': True,
    'license_url' : 'https://www.apache.org/licenses/LICENSE-2.0',
}

html_static_path = ['_static']

html_css_files = ['extra.css']
