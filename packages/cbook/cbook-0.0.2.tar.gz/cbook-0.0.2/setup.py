import os
from setuptools import setup, find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

VERSION = '0.0.2'
DESCRIPTION = "Cookbook app: create, edit, show and filter recipes."

setup(
    name = "cbook",
    version = VERSION,
    author = "Joshua Schmucker",
    author_email = "joshua.schmucker@gmail.com",
    description = DESCRIPTION,
    license = "GNU GPLv3",
    keywords = ["cbook", "recpipes", "recipe management"],
    url = "https://github.com/br0uQ/cbook",
    packages=find_packages(),
    package_data={
        'cbook.view': [
            '*.ui',
            '*.svg',
        ],
    },
    install_requires=[
        'PyQt5',
        'Pillow',
    ],
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [
            'cbook = cbook.__main__:main'
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: German",
        "Operating System :: Unix",
        "Topic :: Utilities",
    ],
)
