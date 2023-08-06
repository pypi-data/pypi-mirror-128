import pathlib
from setuptools import setup, find_packages
from distutils.core import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='django-presentable-exception',
    url='https://github.com/tom-010/django-presentable-exception',
    version='0.0.1',
    author='Thomas Deniffel',
    author_email='tdeniffel@gmail.com',
    packages=['presentable_exception'], # find_packages(),
    license='Apache2',
    install_requires=[
        'Django>=3.2.0',
        'djangorestframework>=3.12.0',
        'find-class>=0.0.1'
        'exception-safe>=0.0.3'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    description='Presentable Exceptions for Django Restframework Projects',
    long_description=README,
    long_description_content_type="text/markdown",
    python_requires='>=3',
    include_package_data=True,
    entry_points={
    }
)