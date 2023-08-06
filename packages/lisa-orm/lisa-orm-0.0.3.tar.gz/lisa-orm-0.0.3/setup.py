from setuptools import setup

# reading the contents of README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='lisa-orm',
    version='0.0.3',
    description='lisa is an orm system like django orm',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://linktr.ee/marawan6569',
    author='marawan mohamed',
    author_email='marawan6569@gmail.com',
    packages=['lisa_orm', 'lisa_orm.db'],
    classifiers=['Development Status :: 1 - Planning'],
)

