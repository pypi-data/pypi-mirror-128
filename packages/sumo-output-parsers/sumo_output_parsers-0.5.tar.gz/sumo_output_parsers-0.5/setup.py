# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sumo_output_parsers',
 'sumo_output_parsers.csv_based_parser',
 'sumo_output_parsers.definition_parser',
 'sumo_output_parsers.models',
 'sumo_output_parsers.tree_parser',
 'sumo_output_parsers.visualizer']

package_data = \
{'': ['*']}

install_requires = \
['Cython',
 'SumoNetVis',
 'dataclasses',
 'geopandas',
 'geoviews',
 'h5py',
 'hvplot',
 'joblib',
 'more_itertools',
 'moviepy<1.0.2',
 'nptyping>=1.4.1,<2.0.0',
 'numpy',
 'pandas',
 'requests',
 'scikit-learn',
 'scipy',
 'tabulate',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'sumo-output-parsers',
    'version': '0.5',
    'description': 'Fast and lightweight file parsers for SUMO(traffic simulator) output',
    'long_description': "# What's this?\n\nFast and lightweight file parsers for Eclipse SUMO(traffic simulator) output.\n\nThe SUMO outputs are huge in size and hard to handle.\n\nSUMO team provides scripts to convert from xml into CSV, however, the procedure is troublesome (downloading XSD, executing python script...)\n\nAlso, machine learning users take care of matrix data format.\n\nThis package provides an easy-to-call python interface to obtain matrix form from SUMO xml files.\n\n# Contributions\n\n- easy-to-call python interfaces to obtain matrix form from SUMO xml files\n- easy-to-call python interfaces to visualize SUMO simulations\n\n![Example of animation](https://user-images.githubusercontent.com/1772712/135924848-4a938dd2-b2d3-4dfe-bfd6-94904086c382.gif)\n\n# Sample\n\nSee `sample.py`\n\n# Test\n\n```\npytest tests\n```\n\n# License\n\n```\n@misc{sumo-output-parsers,\n  author = {Kensuke Mitsuzawa},\n  title = {sumo_output_parsers},\n  year = {2021},\n  publisher = {GitHub},\n  journal = {GitHub repository},\n  howpublished = {\\url{}},\n}\n```",
    'author': 'Kensuke Mitsuzawa',
    'author_email': 'kensuke.mit@gmail.com',
    'maintainer': 'Kensuke Mitsuzawa',
    'maintainer_email': 'kensuke.mit@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
