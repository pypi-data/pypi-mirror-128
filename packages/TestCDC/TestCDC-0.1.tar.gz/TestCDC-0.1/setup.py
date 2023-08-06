from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 10",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name='TestCDC',
    version="0.1",
    description="CDC Log Based API",
    long_description=open('Readme.txt').read() +'\n\n',
    author='KIIT',
    license='MIT',
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=['']
    
)