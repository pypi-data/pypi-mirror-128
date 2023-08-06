import os
import pathlib

from setuptools import setup

def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

requirements = read('requirements.txt').splitlines()
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(name='ERL-Spanish',
      version='1.0.4',
      description='ERL: Emotion Recognition Library',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/estefaaa02/ERL',
      author='Mario Gómez, Estefanía Pérez, Victoria Núñez',
      author_email='mgomezcam@unbosque.edu.co, eperezt@unbosque.edu.co, vnunezd@unbosque.edu.co',
      license='GPLv3 License',
      packages=['ERL'],
      package_data={
        'ERL': ['models/*']
      },
      zip_safe=False,
      install_requires=requirements,
      include_package_data=True,
      )
