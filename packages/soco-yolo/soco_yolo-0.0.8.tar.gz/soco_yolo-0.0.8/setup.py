import setuptools
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="soco_yolo",
    packages = find_packages(),
    package_data={'': ['*.yaml']},
    include_package_data=True,
    version="0.0.8",
    author="kyusonglee",
    description="YOLO wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.soco.ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Free for non-commercial use",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "Pillow==8.2.0",
        "tqdm==4.56.0",
        "requests >= 2.25.0",
        "matplotlib>=3.2.2",
        "numpy>=1.18.5",
        "opencv-python>=4.1.2",
        "PyYAML>=5.3.1",
        "scipy>=1.4.1",
        "torch==1.8.1",
        "torchvision==0.9.1",
        "pandas",
        "seaborn>=0.11.0",
        "thop"
    ]
)
