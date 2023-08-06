from setuptools import setup, find_packages

VERSION = '1.0.2'
DESCRIPTION = 'Metadata scraper for FFN and AO3'

# Setting up
setup(
    name="fanficapi",
    version=VERSION,
    author="lonely-code-cube",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="README.md",
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