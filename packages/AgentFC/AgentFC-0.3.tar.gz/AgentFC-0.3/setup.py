# Author: Acer Zhang
# Datetime: 2021/11/22 
# Copyright belongs to the author.
# Please indicate the source for reprinting.

from setuptools import setup
from setuptools import find_packages

__version__ = "0.3"

setup(
    name='AgentFC',
    version=__version__,
    packages=find_packages(),
    url='https://github.com/AgentMaker/AgentFaceCollector',
    license='Apache2',
    author='AgentMaker',
    author_email='agentmaker@163.com',
    description='人像变换辅助工具',
    install_requires=["opencv-python",
                      "paddlehub"],
    python_requires='>3.6',
    include_package_data=True,
)