from setuptools import setup

setup(
    name="movie",
    version="1.0",
    author="Mihail",
    author_email="liahim13@example.com",
    description="A package for reading CSV and analyzing movies data files using pandas.",
    packages=['movie'],
    install_requires=["pandas>=2.0.3",
                      "numpy>=1.26.0"]
    )
