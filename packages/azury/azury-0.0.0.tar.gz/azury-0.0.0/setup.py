from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='azury',
    version='0.0.0',
    description='Azury Python SDK (Under developement)',
    py_modules=["main"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Filippo Romani",
    author_email="mail@filipporomani.it",
    url="https://github.com/azurystudios/azury.py"
)