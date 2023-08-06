"""Dynamic configuration for setuptools."""
import os
import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

with open(os.path.join('redmx', 'VERSION')) as version_file:
    version = version_file.read().strip()

setuptools.setup(
    name='redmx',
    version=version,
    author='League of Crafty Programmers Ltd.',
    author_email='info@locp.co.uk',
    description='Rate, Errors and Duration Metrics.',
    keywords='metrics',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/locp/redmx',
    project_urls={
        'Bug Tracker': 'https://github.com/locp/redmx/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    package_data={'redmx': ['VERSION']},
    package_dir={'redmx': 'redmx'},
    packages=setuptools.find_packages(where='.'),
    python_requires='>=3.8')
