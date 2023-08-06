"""
The :mod:`*********` scaffolding contig.
"""

# Author: Jie Li <jlli6t at gmail.com>
# License: GNU v3.0
# Copyright: 2020-2021

import os
from biosut import gt_file, gt_exe
from loguru import logger


class Scaffolder:
    def __init__(self, fq1, fq2, contig, outdir,
                 insert_size: int = 300, min_seq_len: int = 500,
                 suffix: str = "fa", cpu: int = 10):
        """Pile up tool(s) to do scaffolding.
        :param
        fq1: str
            Input fq1.
        fq2: str
            Input fq2.
        contig: str
            Input contig FASTA file.
        outdir: str
            Input output directory.
        insert_size: int, default `300`
            Insert size of pair-end read. [300]
        min_seq_len = int, default `500`
            Minimum sequence length cutoff. [500]
        suffix = str, default `fa`
            Suffix of output sequence file. [fa]
        cpu = int, default 10.
            Number of cpus to use. [10]

        :return
            Output scaffolds.
        """

        self.fq1 = fq1
        self.fq2 = fq2
        self.contig = contig
        self.outdir = outdir
        self.insert_size = insert_size
        self.min_seq_len = min_seq_len
        self.suffix = suffix
        self.cpu = cpu

        gt_file.check_file_exist(self.fq1, self.fq2, self.contig)

    def sspace_standard(self, aligner: str = "bwa", error_rate: float = 0.25,
                        read_type: str = "FR"):
        """Run SSPACE_Standard to do scaffolding.
        :parameter
        aligner = str, default is bwa
            Aligner to use, bwa or bowtie, default is bwa.
        read_type = str, default is FR
            Read type, FR/FF/RR, default is FR
        error_rate = float, default 0.25
            error rate tolerance, 0-1, default 0.25.

        :returns
            Output sspace_standard scaffolds file.
        """
        k = "sspace_standard"
        logger.info("Scaffolding with sspace_standard.")
        # sub_outdir = f"{self.outdir}/sspace_standard"
        # old_dir = os.getcwd()
        os.chdir(f"{self.soutdir}")
        with open(f"{self.outdir}/{k}.lib", "w") as lib:
            lib.write(f"lib1 {aligner} {self.fq1} {self.fq2} "
                      f"{self.insert_size} {error_rate} {read_type}")

        cmd = f"SSPACE_Standard_v3.0.pl -l {self.outdir}/{k}.lib " \
              f"-s {self.contig} -x 0 -T {self.cpu} -b {k}"
        gt_exe.exe_cmd(cmd, shell=True)

        # os.chdir(old_dir)

        scaffold_file = f"{self.outdir}/{k}/{k}.final.scaffolds.fasta"
        logger.info(f"Finished scaffolding with sspace_standard.")
        return scaffold_file
