import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utility-liron_revah",
    version="0.0.11",
    author="Liron Revah",
    author_email="revahliron@gmail.com",
    description="A small utility package for my own projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liron7722/Utility",
    project_urls={
        "Bug Tracker": "https://github.com/liron7722/Utility/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["CMRESHandler","numpy","pymongo","requests","dnspython"],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)