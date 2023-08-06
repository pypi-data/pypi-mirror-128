import setuptools

setuptools.setup(
    name="bda-service-template",
    version="0.0.1",
    author="Alida research team",
    author_email="salvatore.cipolla@eng.it",
    description="Bda templates to build python services for Alida",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires = [
        "hdfs>=2.0.0"
        ],
)
