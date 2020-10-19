#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Flask',
    'Click>=7.0',
    'bcrypt',
    'Flask-Security-Too',
    'flask-mongoengine',
    'Flask-Caching',
    'itsdangerous',
    'Jinja2',
    'MarkupSafe',
    'Werkzeug',
    'gunicorn'
]

setup_requirements = []

test_requirements = [
    'factory_boy'
]

setup(
    author="Flask Packages",
    author_email='llazzaro@dc.uba.ar',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Flack Packages Web page",
    entry_points={
        'console_scripts': [
            'manage=flask_packages.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='flask_packages',
    name='flask_packages',
    packages=find_packages(include=['flask_packages', 'flask_packages.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/llazzaro/flask_packages',
    version='0.1.0',
    zip_safe=False,
)
