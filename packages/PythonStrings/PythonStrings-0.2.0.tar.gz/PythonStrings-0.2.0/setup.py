from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='PythonStrings',
    packages=find_packages(include=['PythonStrings']),
    version='0.2.0',
    long_description_content_type="text/markdown",
    long_description=README,
    description='A library made to make string easier to use in python',
    license='MIT',
    url='https://github.com/Sas2k/PythonStrings',
    author='Sasen Perera',
    author_email='sasen.learnings@gmail.com',
    keywords='PythonStrings'
)