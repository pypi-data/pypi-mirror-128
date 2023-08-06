from setuptools import setup, find_packages
import runpy
from pathlib import Path
BASE_DIR = Path(__file__).parent
long_description = (BASE_DIR / "README.md").read_text()

pygems = runpy.run_path(BASE_DIR/'src'/'pygems'/'__init__.py')

setup(
    name='pygems',
    version=pygems['__version__'],
    description='Python gems from Baobab',
    url='https://github.com/ivangeorgiev/py-gems',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'':'src'},
    packages=find_packages(),
    entry_points={
        'console_scripts': ['pygems=pygems.cli:main']
    },
    install_requires=[
    ],
)
