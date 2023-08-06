import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ml_dl_models",
    version="1.0.2",
    author="Laxman Maharjan",
    author_email="lxmnmrzn17@gmail.com",
    description="Module to access machine learning and deep learning module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laxmanmaharjan/ml-dl-models",
    project_urls={
        "Bug Tracker": "https://github.com/laxmanmaharjan/ml-dl-models/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=["requests","music21>=7"],
    python_requires=">=3.6",
)


