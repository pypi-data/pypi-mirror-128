from setuptools import setup, find_packages
import re


with open("crazylog/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]


with open("README.md", encoding="utf-8") as f:
    readme = f.read()


with open("requirements.txt", encoding="utf-8") as f:
    requirements = [r.strip() for r in f]


setup(
    name="crazylog",
    version=version,
    packages=find_packages(),
    url="https://github.com/afarntrog/crazylog",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Aaron Farntrog",
    description="A Python package to add extensive logs to each execution statement",
    keywords="log logging debug monitor python3 python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires=">=3.6",
)