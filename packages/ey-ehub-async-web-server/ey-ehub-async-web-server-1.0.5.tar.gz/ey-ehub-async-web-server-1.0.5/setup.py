# Copyright (c) Ernst & Young LLP. All rights reserved.

from setuptools import setup, find_packages


__version__ = '1.0.5'


requirements = [
    "requests==2.23.0",
    "Flask==1.1.2",
    "msal==1.16.0"
]

setup(
    name='ey-ehub-async-web-server',
    version=__version__,
    description='The package includes an implementation of web app service library to handle requests asynchronously.',
    url='', # TODO
    maintainer='EY Ecosystems Hub team',
    maintainer_email='', # TODO
    packages=find_packages(),
    dependency_links=[],
    install_requires=requirements,
    python_requires='>=3.6,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
    extras_require={
        ':python_version=="2.7"': ['typing>=3.6'],  # allow typehinting PY2
        'all': requirements,
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
