"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name="motc-tdx-proxy",
    version="0.0.2",
    description="台灣交通部「TDX運輸資料流通服務平臺」之python介接套件",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chihsuanwu/tdx-proxy",
    author="Chi-Hsuan Wu",
    author_email="chihsuanw@gmail.com",
    keywords="tdx",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9, <4",
    install_requires=["requests"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    project_urls={
        "Bug Reports": "https://github.com/chihsuanwu/tdx-proxy/issues",
        "Source": "https://github.com/chihsuanwu/tdx-proxy/",
    },
)