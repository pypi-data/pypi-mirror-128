from setuptools import setup, find_packages

setup(
    name='torchlights',
    packages=find_packages(),
    version='0.3.1',
    install_requires=['munch', 'colorama', 'readchar', 'tqdm', 'qqdm', 'pyyaml', 'colorlog']
)