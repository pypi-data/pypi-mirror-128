from setuptools import setup, find_packages

VERSION = '0.0.6' 
DESCRIPTION = 'Bluemanoid Package'
LONG_DESCRIPTION = 'Useful Python scripts for Bluemanoid workers'
AUTHOR = 'Gautier Rio'
AUTHOR_MAIL = 'gautier.rio@bluemanoid.com'

# Setting up
setup(
    name="blmpy", 
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    
    keywords=['python', 'Bluemanoid', 'BLM'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)