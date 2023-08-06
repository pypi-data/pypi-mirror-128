from setuptools import setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='whatajoke',
    version='1.1',
    packages=['whatajoke'],
    url='https://github.com/joaoduartepinto/whatajoke',
    download_url='https://github.com/joaoduartepinto/whatajoke/archive/refs/tags/v1.0.tar.gz',
    license='GPLv3',
    author='Joao Duarte Pinto',
    author_email='joaoduartepinto@outlook.com',
    description='Send a joke to a Whatsapp group!',
    entry_points={
        'console_scripts': ['wj=whatajoke.whatajoke:main']
    },
    install_requires=required,
)
