import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyLody",
    version="1.0.0",
    author="Gulg",
    author_email="gulgdevs@yandex.com",
    description="A small package designed to create simple melodies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Multimedia :: Sound/Audio",
        "Programming Language :: Python :: 2",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.6",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
    ],
    keywords="melody sound music",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=2.6, !=3.0.*, !=3.1.*, !=3.2.*",
)
