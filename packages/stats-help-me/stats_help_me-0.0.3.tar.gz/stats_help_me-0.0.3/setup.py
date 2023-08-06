

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stats_help_me",
    version="0.0.3",
    author="James",
    author_email="james@gmail.com",
    description="Description regarding the package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.educative.io/edpresso/publishing-packages-on-pypi",
    packages=['stats_help_me'],
    install_requires=['pandas','Pillow','ipython','urllib3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)