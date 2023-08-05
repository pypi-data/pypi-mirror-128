from setuptools import find_packages, setup
setup(
    name='PythonStrings',
    packages=find_packages(include=['PyString']),
    version='0.1.0',
    description='A library made to make string easier to use in python',
    author='Sasen Perera',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
)