import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description_ = fh.read()

setuptools.setup(
    name="web_utils",
    version="0.0.1",
    author="Ishan-Mitra",
    author_email="ishanmitra020@gmail.com",
    description="A small example package",
    long_description=long_description_,
    long_description_content_type="text/markdown",
    url="https://github.com/Mitra-Electronics/web_util",
    project_urls={
        "Bug Tracker": "https://github.com/Mitra-Electronics/web_util/issues",
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
