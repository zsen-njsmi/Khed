import os
from setuptools import setup,find_packages

__dir__ = os.path.dirname(__file__)

filename = os.path.join(__dir__,'README.rst')
with open(filename) as readme:
    long_description = readme.read()



def read_requirements(requirements):
    """
    Parse a requirements file

    :return: list of str for each package
    """
    file_path = os.path.join(__dir__,requirements)
    with open(file_path) as requirements:
        required = requirements.read().splitlines()
        return required

required = read_requirements('requirements.txt')
short_description = 'Free anime downloader, supporting resumable downloads and episodes playlist all at once.'

setup(
    name='khed',
    version='0.0.1',
    description=short_description,
    author='Bhanu Kashyap',
    author_email='kash.bhanu7@gmail.com',
    packages=find_packages(exclude=('tests')),
    install_requires=required,
    license='MIT',
    long_description=long_description,
    classifiers=[
        'Development Status :: 3-Alpha',
        'License :: OSI Approved :: MIT License',

        'Operating System :: POSIX :: Linux',
        'Environment :: Console',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.4',

        'Topic :: Multimedia :: Video'
                ],

    entry_points={
        'console_scripts': [
            'khed = khed.anime:main'
                        ]
                },
    include_package_data=True

)
