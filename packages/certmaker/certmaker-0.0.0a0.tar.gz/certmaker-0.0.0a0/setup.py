import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

__tag__ = "0.0.0"
__build__ = 0
__version__ = f"{__tag__}a{__build__}".format(__tag__)

setuptools.setup(
    name="certmaker",
    version=__version__,
    author="Denis Vasilìk",
    author_email="contact@denisvasilik.com",
    url="https://certmaker.denisvasilik.com",
    project_urls={
        "Bug Tracker": "https://github.com/denisvasilik/certmaker/issues/",
        "Documentation": "https://certmaker.readthedocs.io/en/latest/",
        "Source Code": "https://github.com/denisvasilik/certmaker/",
    },
    description="Binary Data Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
    ],
    dependency_links=[],
    package_dir={"certmaker": "certmaker"},
    package_data={},
    data_files=[("", ["CHANGELOG.md"])],
    setup_requires=[],
    install_requires=[
        "certmaker",
        "click>=5.1",
    ],
    # entry_points='''
    #     [certmaker.commands]
    #     patch=certmaker.cli:certmaker
    # ''',
    entry_points={"console_scripts": ["certmaker = certmaker.cli:main"]},
)
