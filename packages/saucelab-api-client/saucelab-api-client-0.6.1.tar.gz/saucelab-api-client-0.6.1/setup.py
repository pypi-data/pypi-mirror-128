import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='saucelab-api-client',
    version='0.6.1',
    use_scm_version=False,
    description='SauceLab Api Python Client',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Biriukov Maksym',
    author_email='maximbirukov77@gmail.com',
    url="https://github.com/Slamnlc/saucelab-api-client",
    download_url='https://github.com/Slamnlc/saucelab-api-client/archive/refs/tags/v0.6.1.tar.gz',
    packages=setuptools.find_packages(exclude=("tests", "dev_tools")),
    install_requires=[
        'requests'
    ],
    entry_points={
        "saucelab_api_client": [
            "sauce_lab_api = saucelab_api_client.saucelab_api_client",
        ]
    },
)
