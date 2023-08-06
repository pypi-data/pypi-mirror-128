import os

from setuptools import setup


# TODO: this needs to change!
# with open('requirements.txt') as f:
#   required = f.read().splitlines()

# def requirements():
#     root_dir = os.path.dirname(os.path.abspath(__file__))
#     with open(f"{root_dir}/requirements.txt") as f:
#         content = f.readlines()
#     # you may also want to remove whitespace characters like `\n` at the end of each line
#     li = [x.strip() for x in content]
#     return li


setup(
    name='whatajoke',
    version='1.1.4',
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
    install_requires=['click==8.0.3',
                      'requests==2.26.0',
                      'selenium==4.1.0',
                      'setuptools==57.0.0',
                      'webdriver_manager==3.5.2'],
)
