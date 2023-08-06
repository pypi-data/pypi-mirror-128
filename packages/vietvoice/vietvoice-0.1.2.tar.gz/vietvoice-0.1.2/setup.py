import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vietvoice",
    version="0.1.2",
    author="pbcquoc",
    author_email="pbcquoc@gmail.com",
    description="text2speech for vietnamese voice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbcquoc/vietvoice",
    packages=setuptools.find_packages(),
    install_requires=[
        'gdown==3.11.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
