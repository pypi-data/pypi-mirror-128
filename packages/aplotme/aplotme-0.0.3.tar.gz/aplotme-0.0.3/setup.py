from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'plot pendulum simulation'
LONG_DESCRIPTION = 'ploting your pendulum datas extracted from apdl'

# Setting up
setup(
       # the name must match the folder name 'aplotme'
        name="aplotme", 
        version=VERSION,
        author="mohammad saeidi",
        author_email="mohammadsaeidi1551@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[['numpy', 'pandas', 'matplotlib']], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)