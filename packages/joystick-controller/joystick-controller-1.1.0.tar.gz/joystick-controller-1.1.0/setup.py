import pathlib
from setuptools import setup, find_packages
import sys

# Python supported version checks
if sys.version_info[:2] < (2, 7):
    raise RuntimeError("Python version >= 2.7 required.")

# The directory containing this file
HERE = str(pathlib.Path(__file__).parent)

# The text of the README file
f = open(str(HERE + "/" + "README.md"))
README = f.read()
f.close()

# The package setup
setup(
    name = 'joystick-controller',
    version = '1.1.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'A simple library to map joystick inputs, or gamepad to a given control variable',
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/MarceloJacinto/joystick-controller',
    author = 'MarceloJacinto',
    author_email = 'marcelo.jacinto@tecnico.ulisboa.pt',
    license="MIT",
    classifiers = [],
    packages = find_packages(exclude=("tests","doc","example")),
    include_package_data=True,
    platforms = ["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    python_requires='>=2.7',
    install_requires=["pygame >= 2.0.3", "typing"]
)