import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jqqb",
    version="0.0.1",
    author="Nicolas Ramy",
    author_email="nicolas.ramy@darkelda.com",
    description="Python parsing, evaluation and inspection tools "
                "for jQuery-QueryBuilder rules",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Connecting-Food/jQueryQueryBuilder",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pytimeparse~=1.1.8'
    ],
    python_requires='>=3.6',
)
