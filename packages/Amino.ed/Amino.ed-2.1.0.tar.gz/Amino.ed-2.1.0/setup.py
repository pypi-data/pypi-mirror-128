from setuptools import setup, find_packages


with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'Amino.ed',
    version = '2.1.0',
    url = 'https://github.com/Alert-Aigul/Amino.ed',
    download_url = 'https://github.com/Alert-Aigul/Amino.ed/archive/refs/heads/main.zip',
    license = 'MIT',
    author = 'Alert Aigul',
    author_email = 'alertaigul@gmail.com',
    description = 'A library to create Amino bots.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'amino.py',
        'amino.ed',
        'amino-ed',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'slimakoi',
        'unofficial',
        'alert',
        'fix',
        'ed'
    ],
    install_requires = [
        'setuptools',
        'six',
        'aiohttp',
        'ujson'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
