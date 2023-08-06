# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
from MetaAssemblyImprove.version import Version


setup(
    name="MetaAssemblyImprove",
    description="Improve the quality of metagenome assembly"
                "by scaffolding and gap solving.",
    version=Version.get_version(),
    url="https://github.com/jlli6t/MetaAssemblyImprove",
    author="Jie Li",
    author_email="jlli6t@gmail.com",
    maintainer="Jie Li",
    maintainer_email="jlli6t@gmail.com",

    long_description=Version.long_description(),
    long_description_content_type="text/markdown",

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
    ],
    keywords="biology bioinformatics",
    scripts=['bin/MetaAssemblyImprove'],
    # packages = find_packages(),
    packages=['MetaAssemblyImprove'],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=['biosut>=2.1.0', ],
)
