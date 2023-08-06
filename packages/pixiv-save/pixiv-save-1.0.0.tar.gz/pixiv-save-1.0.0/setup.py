from setuptools import setup,find_packages

setup(
    name='pixiv-save',
    version='1.0.0',
    description='save pixiv user illusts',
    author='HIbian',
    author_email='hibianchen@gmail.com',
    requires=['pixivpy3','argparse'],
    packages=find_packages(),
    license='MIT'
)