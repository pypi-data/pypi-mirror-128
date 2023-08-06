import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smarterai",
    version="0.0.1",
    author="Nevine Soliman and Carlos Medina",
    author_email="nevine@smarter.ai, carlos@smarter.ai",
    description="smarter.ai Python API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.smarter.ai/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=setuptools.find_packages(where="smarterai"),
    python_requires=">=3.6",
    flake8={"max-line-length": 120}
)
