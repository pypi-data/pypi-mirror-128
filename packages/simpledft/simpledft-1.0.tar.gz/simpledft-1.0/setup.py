from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='simpledft',
    version='1.0',
    description='A simple density funtional theory code.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/nextdft/simpledft',
    author='Wanja Timm Schulze',
    author_email='wangenau@protonmail.com',
    license='APACHE2.0',
    packages=find_packages(),
    install_requires=['numpy', 'scipy'],
    include_package_data=True,
    zip_safe=False
)
