import setuptools


with open("README.md", "r") as fh:

    long_description = fh.read()


setuptools.setup(

    name="MRI_PulseSim", # Replace with your package name

    version="0.0.2",

    author="Ties Tensen",

    author_email="ties.tensen@gmail.com",

    description="Description of your Python package",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/totensen/MRI_PulseSim",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.6',

)