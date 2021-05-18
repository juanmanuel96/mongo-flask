from setuptools import setup
from mongo_flask.about import __version__, __description__, __author__


setup(
    name='mongo_flask',
    version=__version__,
    description=__description__,
    url=None,
    author=__author__,
    author_email=None,
    license='BSD-2-Clause License',
    packages=['mongo_flask'],
    install_requires=['flask', 'pymongo'],
    classifiers=[
        'Development Status :: 2 - Development',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ]
)
