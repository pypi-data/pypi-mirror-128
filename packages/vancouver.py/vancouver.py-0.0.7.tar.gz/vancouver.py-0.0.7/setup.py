import os

from setuptools import setup


requirements = """asyncio
discord.py"""

setup(
    name         = 'vancouver.py',
    version      = '0.0.7',
    project_urls = {
        "Alikoon": "https://discord.gg/7yn4X9kuHt"
    },
    url = None,
    include_package_data = True,
    description  = '[SV] Alikoon Vancouver',
    author       = 'Allan BlackWell',
    license      = 'AMB',
    zip_safe     = False,
    author_email = "allan_blackwell@list.ru",
    classifiers  = [
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 5 - Production/Stable',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    platforms        = ['any'],
    packages         = [
        'vancouver',
    ],
    python_requires  = '>=3.6, <4',
    install_requires = requirements,
)
