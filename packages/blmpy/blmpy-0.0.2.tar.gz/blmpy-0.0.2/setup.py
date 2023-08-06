from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'Bluemanoid Package'
LONG_DESCRIPTION = 'Useful Python scripts for Bluemanoid workers'
AUTHOR = 'Gautier Rio'
AUTHOR_MAIL = 'gautier.rio@bluemanoid.com'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="blmpy", 
        version=VERSION,
        author=AUTHOR,
        author_email=AUTHOR_MAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[
            'json'
        ],
        
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