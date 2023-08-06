import setuptools

with open("README.md", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="cantera_adaptive_testing",
    version="0.0.1",
    author="Anthony Walker",
    author_email="walkanth@oregonstate.edu",
    license='MIT License',
    description="This package is used for testing preconditioner additions to Cantera and running studies on the additions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anthony-walker/cantera-adaptive-testing",
    entry_points={
        'console_scripts': ['adaptive-testing=cantera_adaptive_testing.commandline:commandLineMain','adaptive-testing.mpi_run_all=cantera_adaptive_testing.commandline:MPIRunAll']
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'cantera_adaptive_testing': ['mechanisms/*',]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['cantera', 'mpi4py']
)
