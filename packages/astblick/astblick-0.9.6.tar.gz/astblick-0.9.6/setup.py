""" Setup file for astblick """

from setuptools import setup

setup(
    scripts = ['astblick-repo', 'astblickd'],
    include_package_data=True,
    package_data={'': ['style.css','favicon.ico','README.md']},
)
