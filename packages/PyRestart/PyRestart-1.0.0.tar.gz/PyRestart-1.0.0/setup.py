import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyRestart",
    version="1.0.0",
    author="MXPSQL",
    author_email="2000onetechguy@gmail.com",
    description="Restart module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MXP2095onetechguy/PyRestart",
    project_urls={
        "Bug Tracker": "https://github.com/MXP2095onetechguy/PyRestartissues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)