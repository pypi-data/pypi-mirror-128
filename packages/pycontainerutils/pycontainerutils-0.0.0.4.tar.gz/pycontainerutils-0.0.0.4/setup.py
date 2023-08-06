import setuptools

import unittest


def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setuptools.setup(
    name="pycontainerutils",  # 패키지 명
    version='0.0.0.4',
    license='MIT',
    author='greenrain',
    author_email='kdwkdw0078@gmail.com',
    description='docker container utilities',
    long_description=open('README.md', encoding='UTF-8').read(),
    url="https://github.com/greenrain78",
    packages=setuptools.find_packages(),
    test_suite='setup.my_test_suite',
    install_requires=[
        "coloredlogs==15.0.1",
        "greenlet==1.1.2",
        "humanfriendly==10.0",
        "numpy==1.21.4",
        "pandas==1.3.4",
        "psycopg2==2.9.2",
        "pyreadline3==3.3",
        "python-dateutil==2.8.2",
        "pytz==2021.3",
        "six==1.16.0",
        "SQLAlchemy==1.4.27",
    ]
)
