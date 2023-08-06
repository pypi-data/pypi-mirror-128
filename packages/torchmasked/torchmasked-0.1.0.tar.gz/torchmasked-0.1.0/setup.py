from os import path
from setuptools import setup, find_packages

current_path = path.abspath(path.dirname(__file__))

def readme():
    readme_path = path.join(current_path, "README.md")
    with open(readme_path, "r", encoding="utf-8") as fp:
        return fp.read()

def dependencies():
    dep_path = path.join(current_path, "requirements.txt")
    with open(dep_path, "r", encoding="utf-8") as fp:
        return list(map(lambda x: x.strip(), fp.readlines()))

setup(
    name = "torchmasked",
    version = "0.1.0",
    packages = find_packages(),
    description = "Tensor operations with mask for PyTorch.",
    long_description = readme(),
    long_description_content_type = "text/markdown",
    classifiers = [
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    author = "Xiaohan Zou",
    license = 'MIT',
    author_email = "renovamenzxh@gmail.com",
    url = "https://github.com/Renovamen/torchmasked",
    python_requires = ">=3.6",
    install_requires = dependencies(),
    extras_require = {
        'dev': [
            'numpy>=1.14.0'
        ]
    }
)
