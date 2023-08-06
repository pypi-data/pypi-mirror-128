"""
The :mod:`***.gapfiller` module for filling gaps.
"""

# Author: Jie Li <jlli6t at gmail.com>
# License: GNU v3.0
# Copyright: 2020-2021

import os
import sys
from pandas import DataFrame as DF
import pandas as pd
from re import findall

from biosut import gt_file, gt_path, gt_exe, io_seq
from loguru import logger

# for test
from argparse import ArgumentParser


def read_params():
    p = ArgumentParser(description=__doc__)
    p.add_argument("-s", "--scaffold_file", required=True,
                   help="Input scaffold FASTA file.")
    p.add_argument("--fq1", required=True,
                   help="Input fastq 1 file.")
    p.add_argument("--fq2", required=True,
                   help="Input fastq 2 file.")
    p.add_argument("--outdir", default="./",
                   help="Directory for output files. [./]")
    p.add_argument("--gapfiller", action="store_true",
                   help="Set to run gapfiller.")
    p.add_argument("--gapcloser", action="store_true",
                   help="Set to run gapcloser.")
    p.add_argument("--abyss_sealer", action="store_true",
                   help="Set to run abyss_sealer.")
    p.add_argument("--insert_size", default=300, type=int,
                   help="Insert size of pair-end reads. [300]")
    p.add_argument("--min_seq_len", default=500, type=int,
                   help="Minimum sequence length. [500]")
    p.add_argument("--suffix", default="fa", type=str,
                   help="Suffix of output scaffolds file.")
    p.add_argument("--cpu", default=10, type=int,
                   help="Number of CPUs to use.")
    return p.parse_args()


class GapFiller:
    _order = ['genome size(M)', '# contig', 'max_contig', 'min_ctg',
              'n50', '# Ns', '# gap', 'gc(%)']

    def __init__(self, scaffold_file, fq1, fq2, outdir,
                 insert_size: int = 300, min_seq_len: int = 500,
                 suffix: str = "fa", cpu: int = 10, par=None):

        """Pipe up one of integrated gapfiller to solve gaps in scaffolds.
        And give a stat out how many gaps and bases have been resolved.

        :param
        scaffold_file : str
            Input scaffold file.
        fq1 : str
            Input fq1 file.
        fq2 : str
            Input fq2 file.
        outdir : str
            Output directory.
        insert_size = int, default `300`
            Insert_size of pair-end reads. [300]
        basename = str, default `None`
            Basename of outputs.
        min_seq_len = int, default `500`
            Minimum sequence length. [500]
        suffix = str, default `fa`
            Suffix of fasta file. [fa]
        cpu = int, default `10`
            Number of cpus to use. [10]
        par = ArgumentParser.add_argument.parse_args()

        :return
            Output gap resolved scaffold file.
        """

        self.scaffold_file = scaffold_file
        self.fq1 = fq1
        self.fq2 = fq2
        self.outdir = outdir
        self.insert_size = insert_size
        self.min_seq_len = min_seq_len
        self.suffix = suffix
        self.cpu = cpu
        self.par = par

        gt_file.check_file_exist(self.scaffold_file, self.fq1, self.fq2)

        final_stat = DF(columns=self._order)
        if par.gapfiller:
            gapfiller_stat = self.gapfiller(aligner="bwa",
                                            error_rate=0.25,
                                            read_type="FR")
            final_stat = final_stat.append(gapfiller_stat)
        if par.gapcloser:
            gapcloser_stat = self.gapcloser(read_len=150)
            final_stat = final_stat.append(gapcloser_stat)

        if par.abyss_sealer:
            sealer_stat = self.abyss_sealer()
            final_stat = final_stat.append(sealer_stat)
        final_stat.to_csv(f"{self.outdir}/Total.n50.xls", sep="\t")

    def gapfiller(self, aligner: str = "bwa", error_rate: float = 0.25,
                  read_type: str = "FR"):

        """Filling gaps with GapFiller.
        :param
        aligner = str, default `bwa`
            Aligner to use in gapfiller, bwa/bowtie. [bwa]
        error_rate = float, default `0.25`
            error rate of mappings to fill gaps, 0-1. [0.25]
        read_type = str, default `FR`
            sequencing read type, FR/FF/RR [FR]

        :return
            Gap resolved scaffolds file.
        """

        def count_gap_ns(txt):
            closed_gap, original_gap = findall(
                "Closed (\d+) out of (\d+) gaps", txt
            )[0]
            closed_n, original_n = findall(
                "Closed (\d+) out of (\d+) nucleotides", txt
            )[0]
            return int(closed_gap), int(original_gap), int(closed_n), int(original_n)

        def parse_gapfiller_summary(txt, num_gap, num_n):
            # gaps = re.findall("Closed (\d+) out of \d+ gaps", txt)[0][0]
            # ns = re.findall("Closed (\d+) out of \d+ nucleotides", txt)[0][0]
            n_scaffold = findall("Total number of scaffolds = (\d+)", txt)[0]
            total_length = findall("Sum \(bp\) = (\d+)", txt)[0]
            gc = findall("GC Content = (\d+.\d+)%", txt)[0]
            max_size = findall("Max scaffold size = (\d+)", txt)[0]
            min_size = findall("Min scaffold size = (\d+)", txt)[0]
            avg_size = findall(
                "Average scaffold size = (\d+)", txt
            )[0]
            n25 = findall("N25 = (\d+)", txt)[0]
            n50 = findall("N50 = (\d+)", txt)[0]
            n75 = findall("N75 = (\d+)", txt)[0]

            dt = {
                "# scaffolds": n_scaffold,
                "total_length": total_length,
                "# gaps": num_gap,
                "# Ns": num_n,
                "gc (%)": gc,
                "max_scaffold_size": max_size,
                "min_scaffold_size": min_size,
                "average_scaffold_size": avg_size,
                "N25": n25,
                "N50": n50,
                "N75": n75
            }
            return dt

        def stat_gapfiller(summary_file):
            summary_in = open(summary_file).read().split("After iteration")
            summary_df = {}
            for n, iteration in zip(range(1, len(summary_in)), summary_in[1:]):
                iteration = iteration.split("After gapclosing")
                if n == 1:
                    closed_gap, original_gap, closed_n, original_n = \
                        count_gap_ns(iteration[0])
                    dt = parse_gapfiller_summary(iteration[0],
                                                 original_gap,
                                                 original_n)
                    summary_df.setdefault("Original", dt)
                    dt = parse_gapfiller_summary(iteration[1],
                                                 original_gap - closed_gap,
                                                 original_n - closed_n)
                    summary_df.setdefault("Round 1", dt)
                    continue
                closed_gap, original_gap, closed_n, original_n = \
                    count_gap_ns(iteration[0])
                dt = parse_gapfiller_summary(iteration[1],
                                             original_gap - closed_gap,
                                             original_n - closed_n)
                summary_df.setdefault(f"Round {n}", dt)
            summary_df = DF.from_dict(summary_df)
            return summary_df

        logger.info("Filling gaps using GapFiller.")
        # old_dir = os.getcwd()
        sub_outdir = f"{self.outdir}/gapfiller"
        gt_path.sure_path_exist(sub_outdir)

        os.chdir(f"{sub_outdir}/..")
        with open(f"{sub_outdir}/lib", "w") as lib:
            lib.write(f"lib1 {aligner} {self.fq1} {self.fq2} "
                      f"{self.insert_size} {error_rate} {read_type}")

        cmd = f"GapFiller.pl -l {sub_outdir}/lib -s {self.scaffold_file}" \
              f"-T {self.cpu} -b gapfiller"

        gt_exe.exe_cmd(cmd, shell=False)
        # os.chdir(old_dir)

        prefix = f"{sub_outdir}/gapfiller"
        gapfiller_scaf = f"{prefix}.gapfilled.fa"
        cmd = f"mv {prefix}.gapfilled.final.fa {gapfiller_scaf}"
        gt_exe.exe_cmd(cmd, shell=True)
        gt_file.check_file_exist(gapfiller_scaf)

        summary = stat_gapfiller(f"{prefix}.summaryfile.final.txt")
        summary.T.to_csv(f"{prefix}.stat.xls", sep="\t")
        logger.info("Finished filling gaps with GapFiller.")
        gapfiller_scaf_filter = self.filter_scaffold(gapfiller_scaf)
        n50_stat = self.assess_genomes(gapfiller_scaf, gapfiller_scaf_filter)
        logger.info("Finished filling gaps using GapFiller.")
        # return gapfiller_scaf, gapfiller_scaf_filter  # not return fa, Jie
        return n50_stat  # return the statistics result

    def gapcloser(self, read_len: int = 150):
        """Run GapCloser to solve gaps.
        :param
        read_len = int, default `150`
            Read length. [150]

        :return
            Gaps resolved FASTA file.
        """
        logger.info("Filling gaps using GapCloser.")
        sub_outdir = f"{self.outdir}/gapcloser"
        gapcloser_scaf = f"{sub_outdir}/gapcloser.gapfilled.{self.suffix}"

        with open(f"{sub_outdir}/lib", 'w') as lib:
            lib.write(f"max_rd_len={read_len}\n"
                      f"[LIB]\navg_ins={self.insert_size}\n"
                      f"reverse_seq=0\nasm_flags=4\n"
                      f"rd_len_cutoff={read_len}\nrank=1\n"
                      f"pair_num_cutoff=3\nmap_len=32\n"
                      f"q1={self.fq1}\nq2={self.fq2}\n")

        cmd = f"GapCloser -a {self.scaffold_file} -b {sub_outdir}/lib " \
              f"-o {gapcloser_scaf} -l {read_len} -t {self.cpu}"

        gt_exe.exe_cmd(cmd, shell=True)
        gt_file.check_file_exist(gapcloser_scaf, check_empty=True)
        gapcloser_scaf_filter = self.filter_scaffold(gapcloser_scaf)
        n50 = self.assess_genomes(gapcloser_scaf, gapcloser_scaf_filter)
        # return gapcloser_scaf, gapcloser_scaf_filter
        logger.info("Finished filling gaps using GapCloser.")
        return n50

    def abyss_sealer(self):
        """Run abyss-sealer to solve gaps in scaffolds.

        :returns
            Return gap solved scaffolds file."""
        logger.info("Filling gaps using abyss-sealer.")
        sub_outdir = f"{self.outdir}/sealer"

        cmd = f"abyss-sealer -b40G " \
              f"-k128 -k120 -k110 -k100 -k90 -k80 -k70 -k60 -k50 -k40 -k30" \
              f"-o {sub_outdir}/sealer -j {self.cpu} -G {self.insert_size}" \
              f"-S {self.scaffold_file} {self.fq1} {self.fq2}"
        gt_exe.exe_cmd(cmd, shell=True)

        sealer_scaf = f"{sub_outdir}/sealer.gapfilled.fa"
        cmd = f"mv {sub_outdir}/sealer_scaffold.fa {sealer_scaf}"
        gt_exe.exe_cmd(cmd, shell=True)
        sealer_scaf_filter = self.filter_scaffold(sealer_scaf)
        n50 = self.assess_genomes(sealer_scaf, sealer_scaf_filter)
        logger.info("Finished filling gaps using abyss-sealer.")
        return n50

    def filter_scaffold(self, scaffold_file):
        """Add basename to the scaffold id to make it unique id. and filter
        sequence shorter thane a cutoff.
        """
        prefix = gt_file.get_seqfile_prefix(scaffold_file)
        filtered = f"{prefix}.more{self.min_seq_len}.{self.suffix}"
        with open(scaffold_file) as fh, open(f"{prefix}.temp", "w") as out, \
                open(filtered, "w") as flt:
            for t, seq, _ in io_seq.iterator(fh):
                out.write(f">{t}\n{seq}\n")
                if len(seq) >= self.min_seq_len:
                    flt.write(f">{t}\n{seq}\n")
        cmd = f"mv {prefix}.temp {prefix}.{self.suffix}"
        gt_exe.exe_cmd(cmd, shell=True)
        return filtered

    def assess_genomes(self, *genome):
        """Evaluate genomes, and return a matrix
        :param
        genome : str
            Genome(s) to evaluate.

        :returns
            Return a DataFrame of assessment of all genomes."""
        stats = {}
        for gn in genome:
            gn_name = gt_file.get_file_prefix(gn)
            stats.setdefault(gn_name, {})
            gn_size, ctg_num, n50, max_ctg, min_ctg, n, gap, gc = \
                io_seq.evaluate_genome(gn, len_cutoff=self.min_seq_len)

            stats[gn_name] = {"genome size(M)": gn_size / 1000000,
                              "# contigs": ctg_num,
                              "max_contig": max_ctg,
                              "min_ctg": min_ctg,
                              "n50": n50,
                              "# Ns": n,
                              "# gap": gap,
                              "gc(%)": gc}

        stats = DF.from_dict(stats).T[self._order]
        stats.to_csv(f"{gt_file.get_file_path(genome[0])}/n50.xls")
        return stats


# for test
if __name__ == "__main__":

    if len(sys.argv) == 1:
        sys.argv.append("-h")
    par = read_params()

    # print(par)
    # print(type(par))
    # gapfiller_wf = GapFiller(par.scaffold_file, par.fq1, par.fq2, par.outdir,
    #                         insert_size=par.insert_size,
    #                         min_seq_len=par.min_seq_len,
    #                         suffix=par.suffix,
    #                         cpu=par.cpu,
    #                         par=par)
    # 这里只需要实例化，不需要额外调用。
