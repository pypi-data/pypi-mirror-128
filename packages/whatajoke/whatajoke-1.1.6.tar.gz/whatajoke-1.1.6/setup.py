from setuptools import setup

setup(
    name='whatajoke',
    version='1.1.6',
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
    install_requires=['whatajoke==1.1.6',
                      'click==8.0.3',
                      'requests==2.26.0',
                      'selenium==4.1.0',
                      'setuptools==57.0.0',
                      'webdriver_manager==3.5.2'],
)
