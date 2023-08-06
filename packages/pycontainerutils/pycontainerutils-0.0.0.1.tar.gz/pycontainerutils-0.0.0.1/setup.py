from setuptools import setup, find_packages

setup(
      name="pycontainerutils",    # 패키지 명
      version='0.0.0.1',
      license='MIT',
      author='greenrain',
      author_email='kdwkdw0078@gmail.com',
      description='docker container utilities',
      long_description=open('README.md').read(),
      url="https://github.com/greenrain78",
      packages=find_packages(),
)
