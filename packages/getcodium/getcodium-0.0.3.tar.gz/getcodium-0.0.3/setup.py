import re

import setuptools

from getcodium import __appauthor__, __version__


long_description = open("README.md", "r", encoding="utf-8").read()

setuptools.setup(
    name="getcodium",
    version=__version__,
    author=__appauthor__,
    author_email="",
    description="getcodium",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/larryw3i/getcodium",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'getcodium=getcodium:run',
        ]
    },
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=True,
)
