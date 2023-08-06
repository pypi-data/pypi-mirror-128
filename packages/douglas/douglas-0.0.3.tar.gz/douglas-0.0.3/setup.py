import setuptools

setuptools.setup(
    name="douglas",                     # This is the name of the package
    version="0.0.3",                        # The initial release version
    author="José Valencia Figueroa",                     # Full name of the author
    author_email="joel.jvalencia@gmail.com",
    description="This project aims at generating datasets so that statistics methods can be applied.",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    keywords = ['insurance', 'actuarial science', 'non life insurance',
                'python', 'spain', 'motor', 'general insurance', 'property', 'casualty'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    install_requires=['pandas>=0.25.3',
                      'numpy>=1.17.4'])   # Install other dependencies if any
