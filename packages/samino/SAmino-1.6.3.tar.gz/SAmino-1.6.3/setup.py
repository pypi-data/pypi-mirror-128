import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="SAmino",
    version="1.6.3",
    url="https://github.com/SirLez/SAmino",
    download_url="https://github.com/SirLez/SAmino/archive/refs/heads/main.zip",
    description="Amino Bots with python!",
    long_description=README,
    long_description_content_type="text/markdown",
    author="SirLez",
    author_email="SirLezDV@gmail.com",
    license="MIT",
    keywords=[
        'capture',
        'captureS'
        'capture-bot',
        'capture-chat',
        'capture-lib',
        'cptr',
        'cptr.co',
        'api',
        'python',
        'python3',
        'python3.x',
        'SirLez',
        'sirlez',
        'srlz',
        'سيرلز'
        'bovonos',
        'Texaz'
        'Smile'
        'Bovo',
        'Marshall Amino',
        'Texaz Amino',
        'a7rf',
        'A7RF',
        'A7rf',
        'bovonus',
        'Amino',
        'samino',
        'samino py'
        'S-Amino',
        'samino',
        'samino',
        'samino-bot',
        'samino-bots',
        'samino-bot',
        'ndc',
        'narvii.apps',
        'aminoapps',
        'samino-py',
        'samino',
        'samino-bot',
        'narvii',
        'api',
        'python',
        'python3',
    ],
    include_package_data=True,
    install_requires=[
        'setuptools',
        'requests',
        'websocket-client==0.57.0',
    ],
    setup_requires=[
        'wheel'
    ],
    packages=find_packages(),
)
