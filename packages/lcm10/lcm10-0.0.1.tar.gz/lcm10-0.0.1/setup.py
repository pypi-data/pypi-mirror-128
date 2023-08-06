from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Least common multiplication'
LONG_DESCRIPTION = 'Generate 10 random number from LCM'

# Setting up
setup(
    name="lcm10",
    version=VERSION,
    author="Developer Rohit",
    author_email="143rohitbehera@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy'],
    keywords=['python', 'random number', 'normal distribution', 'Least common multiplication', 'developerrohit'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
