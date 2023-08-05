from setuptools import find_packages, setup

with open('README.md') as readme_file:
    README = readme_file.read()

setup(
    name='PythonStrings',
    packages=find_packages(include=['PyString']),
    version='0.1.5',
    long_description_content_type="text/markdown",
    long_description=README,
    description='A library made to make string easier to use in python',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
    author='Sasen Perera',
    author_email='sasen.learnings@gmail.com'
)