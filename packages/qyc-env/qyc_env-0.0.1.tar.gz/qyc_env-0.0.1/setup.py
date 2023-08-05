import setuptools
from pathlib import Path

setuptools.setup(
    name='qyc_env',
    version='0.0.1',
    description='A OpenAI Gym for qyc',
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="qyc_env*"),
    install_requires=['gym']  #以及其他需要的dependencies
)