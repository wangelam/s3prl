# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sphinx-apidoc -d 3 --separate --implicit-namespace -o docs ./s3prl s3prl/downstream s3prl/interface s3prl/preprocess s3prl/pretrain s3prl/problem s3prl/sampler s3prl/submit s3prl/superb s3prl/upstream s3prl/utility s3prl/wrapper s3prl/__init__.py s3prl/hub.py s3prl/optimizers.py s3prl/run_downstream.py s3prl/run_pretrain.py s3prl/run_while.sh s3prl/schedulers.py'
copyright = '2023, Angela'
author = 'Angela'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'python'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
