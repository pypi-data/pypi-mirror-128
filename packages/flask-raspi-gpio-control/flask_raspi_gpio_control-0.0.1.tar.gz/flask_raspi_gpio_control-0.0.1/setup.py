from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

packages = ['flask_raspi_gpio_control']

setup(
    name="flask_raspi_gpio_control",

    version="0.0.1",

    packages=packages,
    install_requires=[
        'flask',
        'dataset',
    ],

    author="Grant miller",
    author_email="grant@grant-miller.com",
    description="Control GPIO on Raspberry Pi",
    long_description=long_description,
    license="PSF",
    keywords="grant miller flask database",
    url="https://github.com/GrantGMiller/flask_raspi_gpio_control",  # project home page, if any
    project_urls={
        "Source Code": "https://github.com/GrantGMiller/flask_raspi_gpio_control",
    }

)
