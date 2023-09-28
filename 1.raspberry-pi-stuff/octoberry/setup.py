from setuptools import setup

setup(
    name='octoberry',
    version='0.1',
    description='Octoberry - Raspberry Pi based jukebox',
    author='Itay Shoshani',
    install_requires=[
        'pygame==2.5.2',
        'requests==2.31.0'
    ],
    entry_points={
        'console_scripts': [
            'octoberry = octoberry.__main__:main'
        ]
    },
)