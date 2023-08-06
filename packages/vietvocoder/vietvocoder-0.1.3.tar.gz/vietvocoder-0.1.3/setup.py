import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vietvocoder",
    version="0.1.3",
    author="pbcquoc",
    author_email="pbcquoc@gmail.com",
    description="WaveGlow finetune for vietnamese voice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbcquoc/vietvocoder",
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
