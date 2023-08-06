import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='shrinemaiden',
    packages=['shrinemaiden'],
    version='0.2.2',
    description='An auxiliary library for deep learning with Audio data',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/VirtuousCrane/shrinemaiden.git',
    author='VirtuousCrane',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=['librosa', 'tensorflow', 'numpy', 'keras', 'scikit-learn'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
