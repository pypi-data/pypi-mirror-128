from setuptools import setup
import io
import os

VERSION = '1.0.5'
DESCRIPTION = 'Metadata scraper for FFN and AO3'

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Setting up
setup(
    name="fanficapi",
    version=VERSION,
    author="lonely-code-cube",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['fanficapi', 'fanficapi.ao3essentials', 'fanficapi.ffnessentials'],
    install_requires=['bs4', 'requests', 'undetected-chromedriver'],
    keywords=['python', 'scraper', 'webscraper', 'metadata scraper', 'fanfiction', 'archiveofourown', 'fanfic scraper', 'fanfic api'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)