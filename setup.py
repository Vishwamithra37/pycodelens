from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pycodelens",
    version="0.1.0",
    author="Code Analyzer",
    author_email="example@example.com",
    description="A tool to extract code elements from Python files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pycodelens",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.7",
    install_requires=[
        "astroid>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "pycodelens=pycodelens.cli:main",
        ],
    },
)
