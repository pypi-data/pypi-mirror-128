from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='escpos_gen',
    version='0.0.2',
    description='Generator of printable binary files with helper methods based on ESC/POS protocol',
    py_modules=["escpos_gen"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/fercorbar/escpos_gen',
    author='Fernando Córdova',
    author_email='fernando@cbin.mx',
    
)