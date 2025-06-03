from setuptools import setup, find_packages

setup(
    name="pyspark-hubspot",
    version="0.1.0",
    install_requires=[
        "pyspark>=4.0.0",
        "requests",
    ],
    author="Diego Gomez",
    author_email="dagomezmoreno@outlook.com",
    description="A PySpark custom data source for reading data from HubSpot's CRM objects",
    url="https://github.com/dgomez04/pyspark-hubspot",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 