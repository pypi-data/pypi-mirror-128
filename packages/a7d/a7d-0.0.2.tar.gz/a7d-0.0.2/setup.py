import setuptools

with open("../readme.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="a7d",
    version="0.0.2",
    author="Uladzislau Khamkou",
    description="a7d8473 archiver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: Public Domain',
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    py_modules=["a7d"],
    package_dir={"": "."},
    install_requires=[],
)
