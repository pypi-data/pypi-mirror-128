from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="sylpy",
    version="0.4",
    description="sylviorus API wrapper",
    py_modules=["sylpy"],
    package_dir={'': 'sylviorus'},
    install_requires=["requests", "typing"],
    extras_require={
                      "dev":[
                          "pytest",
                      ],},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NksamaX/Syl-Py",
    author="Nksamax"

)
