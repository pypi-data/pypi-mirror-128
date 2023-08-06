import setuptools

import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setuptools.setup(
    name="pycontainerutils",  # 패키지 명
    version='0.0.0.3',
    license='MIT',
    author='greenrain',
    author_email='kdwkdw0078@gmail.com',
    description='docker container utilities',
    long_description=open('README.md').read(),
    url="https://github.com/greenrain78",
    packages=setuptools.find_packages(),
    test_suite='setup.my_test_suite',
)
