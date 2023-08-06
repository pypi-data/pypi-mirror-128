import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikifeet",
    version="1.0.0",
    author="XXIV",
    description="WikiFeet (The collaborative celebrity feet website) crawler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sloppydaddy/wikifeet-py",
    project_urls={
        "Bug Tracker": "https://github.com/sloppydaddy/wikifeet-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
