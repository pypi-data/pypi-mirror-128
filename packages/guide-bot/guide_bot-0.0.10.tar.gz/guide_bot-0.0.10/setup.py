from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='guide_bot',
    version='0.0.10',
    author="Mads Bertelsen",
    author_email="Mads.Bertelsen@ess.eu",
    description="Neutron guide optimization package",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.esss.dk/highness/guide_bot",
    install_requires=["pyswarm", "dill", "numpy", "matplotlib", "PyYAML", "mcstasscript", "ipywidgets", "ipympl"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering"

    ])
