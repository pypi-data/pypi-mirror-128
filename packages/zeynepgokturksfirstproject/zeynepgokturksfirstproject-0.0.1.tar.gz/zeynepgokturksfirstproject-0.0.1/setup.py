from setuptools import setup, find_packages

classidiers = [
    'Development Status :: 5 -Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python ::3'
]
setup(name='zeynepgokturksfirstproject',
version='0.0.1',
description='Testing installation of Package',
author='Zeynep Gokturk',
author_email='h.zeynepgokturk@gmail.com',
packages=['my_first_package'],
license='MIT',
keywords= 'first try',
long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
install_requires=[''],)