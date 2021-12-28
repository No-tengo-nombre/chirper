import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="signal-py",
    version="1.0",
    author="Cristobal Allendes",
    author_email="callendes.molina@gmail.com",
    description="Package for signal analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/No-tengo-nombre/signpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
)