from os import path

from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='yeelight-atmosphere',
    version='0.5.0',
    description='Change your yeelight lamp color to scene atmosphere.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    author='Nikita Savilov',
    author_email="niksavilov@gmail.com",
    url="https://github.com/NikSavilov/yeelight-atmosphere/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},

    install_requires=[
        'yeelight==0.7.8',
        'Pillow==8.4.0',
        'sqlalchemy==1.4.26',
        'colorthief==0.2.1',
        'psutil==5.8.0'
    ]
)
