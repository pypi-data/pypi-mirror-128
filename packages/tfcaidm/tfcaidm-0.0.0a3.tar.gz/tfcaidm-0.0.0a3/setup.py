# https://packaging.python.org/tutorials/packaging-projects/
from setuptools import setup, find_packages


with open("README.md", "r") as f:
    long_description = f.read()

packages = find_packages(include=["tfcaidm", "tfcaidm.*"])
install_requires = [
    lib.strip()
    for lib in open("/Users/owner/Code/ai/ml/pypi/tfcaidm/requirements.txt").readlines()
]

setup(
    name="tfcaidm",
    version="0.0.0a3",
    license="GPLv3",
    author="Brandhsu",
    author_email="brandondhsu@gmail.com",
    url="https://github.com/Brandhsu/tfcaidm",
    description="Deep learning pipeline for medical imaging",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "deep learning",
        "neural networks",
        "medical imaging",
        "computer vision",
    ],
    packages=packages,
    python_requires=">=3.6",
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
