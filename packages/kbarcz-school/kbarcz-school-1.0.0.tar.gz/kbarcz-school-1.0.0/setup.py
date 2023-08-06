import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="kbarcz-school",
    version="1.0.0",
    packages=["pypi_school_kb"],
    description="Biblioteka do wyświetlania klas",
    long_description=README,
    long_description_content_type="text/markdown",
)