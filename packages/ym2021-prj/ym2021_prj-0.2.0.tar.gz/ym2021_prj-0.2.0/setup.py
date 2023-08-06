import pathlib
import setuptools
import versioneer


# read the contents of your README file
this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
# long_description = (pathlib.Path(__file__).parent / "README.md").read_text()


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
    # long_description="Repository to test GitHub Actions Workflows.",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    entry_points={
        # create & install scripts in <python>/bin
        "console_scripts": ["ym2021_prj=ym2021_prj.cli:main", ],
        # 'gui_scripts': [],
    },
    test_suite="ym2021_prj/tests",
)
