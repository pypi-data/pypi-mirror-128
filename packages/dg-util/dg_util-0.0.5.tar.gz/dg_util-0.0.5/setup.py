from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Common tools'
LONG_DESCRIPTION = 'Some common tools for image and video processing'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="dg_util", 
        version=VERSION,
        author="DataGrid",
        author_email="",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['image_preprocessing'],
        install_requires=['numpy', 'tqdm', 'opencv-python', 'pillow'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'Tools for Internal Use Only'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            # "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux",
            "Operating System :: Unix"
        ]
)