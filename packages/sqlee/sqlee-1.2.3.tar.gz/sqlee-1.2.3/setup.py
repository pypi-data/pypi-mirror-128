import setuptools
from sqlee import __version__

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name = "sqlee",
    version = __version__,
    author = "Entropy <fu050409@163.com>",
    author_email = "fu050409@163.com",
    description = "Database Powerd by Gitee",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://gitee.com/qu-c/sqlee",
    project_urls = {
        "Bug Tracker": "https://gitee.com/qu-c/sqlee/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license = "MIT",
    packages = setuptools.find_packages(),
    install_requires = [
        'requests',
        'prompt_toolkit',
    ],
    python_requires=">=3",
    
)
