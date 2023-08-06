from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'Package For Quick Data Overview For Analysis.'

# Setting up
setup(
    name="icxpackage_data_characteristics",
    version=VERSION,
    author="InfinityCodeX (Hardik Vegad)",
    author_email="vegadhardik7@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description="This package give us following results: Shape of data, Number of Rows & Columns, data information which include Column names with Non-Null Values & Dtype, Number of numerical features with there name, Number of categorical with there name, Number of null values present in data, Visualization of percentage of null values present in data & head of the data.",
    packages=find_packages(),
    install_requires=['numpy', 'pandas', 'matplotlib', 'seaborn'],
    keywords=['python', 'numpy', 'pandas', 'data analysis', 'data science', 'data', 'seaborn', 'matplotlib'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
