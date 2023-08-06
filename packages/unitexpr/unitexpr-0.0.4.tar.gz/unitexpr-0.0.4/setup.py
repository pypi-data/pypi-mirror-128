import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# read the contents of your README file
# from pathlib import Path
# this_directory = Path(__file__).parent
# long_description = (this_directory / "README2.md").read_text()

setuptools.setup(
    name="unitexpr",
    version="0.0.4",
    author="D Reschner",
    author_email="git@simphotonics.com",
    description="Units, unit expressions, and united arrays.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/simphotonics/units",
    project_urls={
        "Bug Tracker": "https://github.com/simphotonics/unitexpr/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
