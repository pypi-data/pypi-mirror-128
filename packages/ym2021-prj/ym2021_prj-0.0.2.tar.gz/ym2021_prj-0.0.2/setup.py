import os
import setuptools
import versioneer


def read_long_description(fname):
    """Utility function to read the repository README.md file."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name="ym2021_prj",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Pete R. Jemian",
    author_email="prjemian@gmail.com",
    description=("Repository to test GitHub Actions Workflows."),
    license="CC0 1.0 Universal",
    keywords="Python test repository",
    url="https://github.com/prjemian/ym2021_prj",
    packages=setuptools.find_packages(),
    long_description="Repository to test GitHub Actions Workflows.",
    # long_description=read_long_description("README.md"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
    ],
)
