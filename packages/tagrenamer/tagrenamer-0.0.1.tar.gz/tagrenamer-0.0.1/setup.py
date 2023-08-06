#!/usr/bin/env python3

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.rst') as changelog_file:
    changelog = changelog_file.read()

requirements = ['pytaglib',
                'transliterate']

test_requirements = [ ]

setup(
    author="Niels van Mourik",
    author_email='niels@nielsvm.org',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Mass music collection renamer.",
    entry_points={
        'console_scripts': [
            'tagrenamer=tagrenamer.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + changelog,
    include_package_data=True,
    keywords='tagrenamer',
    name='tagrenamer',
    packages=find_packages(include=['tagrenamer', 'tagrenamer.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nielsvm/tagrenamer',
    version='0.0.1',
    zip_safe=False,
)
