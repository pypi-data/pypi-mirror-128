"""
The :mod:`MetaAssemblieImprove.version` print and show version information.
"""

# Author: Jie Li <jlli6t at gmail.com>
# License: GPLv3.0
# Copyright: 2020-2021

from os.path import join, isfile, split, dirname
from biosut.gt_path import abs_path
from loguru import logger


class Version:
    global _f_dir
    _f_dir = dirname(abs_path(__file__))

    # @classmethod
    def get_version():
        ver1 = f"{_f_dir}/version"
        ver2 = f"{_f_dir}/../version"

        if isfile(ver1):
            logger.info("Got ya!1")
            return open(ver1).readline().strip()
        if isfile(ver2):
            logger.info("Got ya!2")
            return open(ver2).readline().strip()
        return "Unknown version"

    @classmethod
    def show_version(cls):
        ver = cls.get_version()
        name = split(dirname(__file__))[1]
        print("\n\n\t\t%s version * %s *\n\n" % (name, ver))

    def long_description():
        readme1 = join(_f_dir, "/README.md")
        readme2 = join(_f_dir, "/../README.md")
        if isfile(readme1):
            return open(readme1).read()
        if isfile(readme2):
            return open(readme2).read()
        return "No detailed description"
