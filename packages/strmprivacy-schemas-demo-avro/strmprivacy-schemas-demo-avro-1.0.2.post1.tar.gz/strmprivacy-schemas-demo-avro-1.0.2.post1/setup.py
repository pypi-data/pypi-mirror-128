#!/usr/bin/env python
from setuptools import setup, find_packages

with open('top_package') as t:
    top_package = t.read().rstrip()

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Stream Machine B.V.",
    author_email='apis@strmprivacy.io',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    description="Python classes for demo",
    install_requires=[
        "avro-gen==0.3.0",
        "tzlocal==2.1"
        # avro-gen has no restriction on tzlocal version and requires .localize() which is not present in the 3.x rewrite of tzlocal
    ],
    long_description=readme,
    include_package_data=True,
    keywords='strmprivacy api client driver schema',
    name='strmprivacy-schemas-demo-avro',
    packages=find_packages(),
    package_data={top_package: ['schema.avsc']},
    setup_requires=[],
    version='1.0.2-1',
    zip_safe=False,
)
