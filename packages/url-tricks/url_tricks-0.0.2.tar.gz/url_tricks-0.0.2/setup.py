from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.2'
DESCRIPTION = 'URL Manipulations that is widely used'
LONG_DESCRIPTION = 'URL Manipulations that is widely used'

# Setting up
setup(
    name="url_tricks",
    version=VERSION,
    author="Banura Randika Perera",
    author_email="<randika.banura@gmail.com>",
    description=DESCRIPTION,
    url="https://github.com/randikabanura/url_tricks",
    long_description_content_type="text/markdown",
    license='MIT',
    long_description=long_description,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'tricks', 'url', 'string', 'manipulation', 'fun'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)