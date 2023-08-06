"""
The :mod:`MetaAssemblieImprove.Main` main workflow.
"""

# Author: Jie Li <jlli6t at gmail.com>
# License: GPLv3.0
# Copyright: 2020-2021

import argparse
from loguru import logger

from biosut import gt_exe, gt_file, gt_path

from .scaffolder import Scaffolder
from .gapfiller import GapFiller


class ReadPar:

    @classmethod
    def read(cls):
        p = argparse.ArgumentParser(description=__doc__)
        g = p.add_argument_group("Required parameters.")
        g.add_argument("-c", "--contig", metavar="contig", required=True,
                        help="Input contig file for scaffolding.")
        g.add_argument("-fq1", "--fq1", metavar="fq1", required=True,
                        help="Input fq1 file.")
        g.add_argument("-fq2", "--fq2", metavar="fq2", required=True,
                        help="Input fq2 file.")

        g = p.add_argument_group("Optional parameters.")
        g.add_argument("-o", "--outdir", default="./",
                        help="Output directory. [./]")
        g.add_argument("-is", "--insert_size", default=300, type=int,
                        help="Insert size of pair-end read.")
        g.add_argument("-m", "--min_seq_len", default=500, type=int,
                        help="Minimum sequence length.")
        g.add_argument("-t", "--cpu", default=10, type=int,
                        help="Number of cpu to use.")

        g = p.add_argument_group("Scaffolding tool set.")
        g.add_argument("-ss", "--sspace_standard", action="store_true",
                        help="Set to run sspace_standard for scaffolding.")

        g = p.add_argument_group("Gapfilling tool set.")
        g.add_argument("-gp", "--gapfiller", action="store_true",
                        help="Set to filling gaps with GapFiller.")
        g.add_argument("-gc", "--gapcloser", action="store_true",
                        help="Set to filling gaps with GapCloser.")
        g.add_argument("-as", "--abyss_sealer", action="store_true",
                        help="Set to filling gaps with abyss-sealer.")

        p.add_argument("-v", "--version", help="show version information")

        par = p.parse_args()
        cls._check_dependencies(par)

        par.fq1 = gt_path.abs_path(par.fq1)
        par.fq2 = gt_path.abs_path(par.fq2)
        par.contig = gt_path.abs_path(par.contig)

        return par

    @staticmethod
    def _check_dependencies(par):
        """Determing parameters dependencies."""

        if not par.sspace_standard:
            logger.error("At least one scaffolding tool has to be set.")
        if not par.gapfiller and not par.gapcloser and not par.abyss_sealer:
            logger.error("At least one gap filling tool has to be set.")

        if par.sspace_standard:
            gt_exe.is_executable("SSPACE_Standard_v3.0.pl")
        if par.gapfiller:
            gt_exe.is_executable("GapFiller.pl")
        if par.gapcloser:
            gt_exe.is_executable("GapCloser")
        if par.abyss_sealer:
            gt_exe.is_executable("abyss-sealer")


class Main:
    def exe():
        par = ReadPar.read()
        par.outdir = gt_path.sure_path_exist(par.outdir)

        scaffolding = Scaffolder(par.fq1, par.fq2, par.contig, par.outdir,
                                 insert_size=par.insert_size,
                                 min_seq_len=par.min_seq_len,
                                 cpu=par.cpu)

        if par.sspace_standard:
            scaffold_file = scaffolding.sspace_standard(aligner="bwa",
                                                        error_rate=0.25,
                                                        read_type="FR")

            GapFiller(scaffold_file, par.fq1, par.fq2,
                      f"{par.outdir}/sspace_standard",
                      insert_size=par.insert_size,
                      min_seq_len=par.min_seq_len,
                      cpu=par.cpu, par=par)


