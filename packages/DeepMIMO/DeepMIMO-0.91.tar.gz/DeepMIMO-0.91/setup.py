import setuptools

VERSION = '0.91' 
DESCRIPTION = 'DeepMIMO'
LONG_DESCRIPTION = 'DeepMIMOv2 dataset generator library'

# Setting up
setuptools.setup(
        name="DeepMIMO", 
        version=VERSION,
        author="Umut Demirhan",
        author_email="<udemirhan@asu.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license_files = ('LICENSE',),
        install_requires=['numpy',
                          'scipy',
                          'tqdm'
                          ],
        
        keywords=['python', 'Alpha'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
        ],
        package_dir={"": "src"},
        packages=setuptools.find_packages(where="src")
)