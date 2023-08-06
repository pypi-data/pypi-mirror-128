import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='find_class',
    url='https://github.com/tom-010/find_class',
    version='0.0.1',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['find_class'], # find_packages(),
    license='Apache2',
    install_requires=[
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Finds a python-thing, like a class, a function or a variable by string and loads it',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    include_package_data=True,
    entry_points={
    }
)