from setuptools import setup, find_packages
import pathlib

current_dir = pathlib.Path(__file__).parent
with open(current_dir / 'README.md') as readme:
    description_long = readme.read()

setup(
    name='bomberman-code-showdown',
    version='0.1.0',
    author='Vlad Calin',
    license='MIT',
    url='https://gitlab.com/vladcalin/bomberman-code-showdown',
    description='A bomberman game where you can control the characters through a HTTP API.',
    description_long=description_long,
    install_requires=[
        'pygame',
        'aiohttp'
    ],
    packages=find_packages(exclude=['tests']),
    package_data={
        'bomberman.objects': ['*.png'],
    },
    include_package_data=True,
    extras_require={
        'dev': [
            'pytest',
            'pytest-mock',
            'coverage',
            'flake8',
            'twine',
            'bump2version',
        ]
    },
    entry_points={
        'console_scripts': [
            'bomberman-code-showdown = bomberman.renderer:main'
        ]
    }
)
