# Analyses from Webster et al. 2018
This directory contains scripts and information for reproducing the analyses that
accompany the initial publication of XYalign (Webster et al., 2018).

Analyses are written in Snakemake (Koster and Rahmann, 2012), which you can find out more about [here](https://snakemake.readthedocs.io/en/stable/index.html)

## Data
For these analyses, we used two different publicly-available datasets:

1) Exome, low-coverage whole-genome, and high-coverage whole-genome data from
two individuals in the 1000 genomes project (HG00512 - male, HG00513 - female)

Fastqs downloaded from:
```
HG00512

Exome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR034/­ERR034508/­ERR034508_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR034/­ERR034508/­ERR034508_2.­fastq.­gz

Low-coverage whole-genome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016114/­ERR016114_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016114/­ERR016114_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016116/­ERR016116_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016116/­ERR016116_2.­fastq.­gz

High-coverage whole genome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894725/­ERR894725_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894725/­ERR894725_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894726/­ERR894726_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894726/­ERR894726_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899712/­ERR899712_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899712/­ERR899712_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899713/­ERR899713_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899713/­ERR899713_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR903/­ERR903029/­ERR903029_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR903/­ERR903029/­ERR903029_2.­fastq.­gz

HG00513

Exome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR034/­ERR034509/­ERR034509_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR034/­ERR034509/­ERR034509_2.­fastq.­gz

Low-coverage whole-genome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016118/­ERR016118_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016118/­ERR016118_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016119/­ERR016119_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016119/­ERR016119_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016121/­ERR016121_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR016/­ERR016121/­ERR016121_2.­fastq.­gz

High-coverage whole-genome
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894727/­ERR894727_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894727/­ERR894727_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894728/­ERR894728_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR894/­ERR894728/­ERR894728_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899714/­ERR899714_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899714/­ERR899714_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899715/­ERR899715_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899715/­ERR899715_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899716/­ERR899716_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR899/­ERR899716/­ERR899716_2.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR903/­ERR903027/­ERR903027_1.­fastq.­gz
ftp:/­/­ftp.­sra.­ebi.­ac.­uk/­vol1/­fastq/­ERR903/­ERR903027/­ERR903027_2.­fastq.­gz
```

2) 24 high-coverage whole-genomes from the 1000 genomes project

BAM files downloaded from:

```
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00096/high_coverage_alignment/HG00096.wgs.ILLUMINA.bwa.GBR.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01879/high_coverage_alignment/HG01879.wgs.ILLUMINA.bwa.ACB.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG03052/high_coverage_alignment/HG03052.wgs.ILLUMINA.bwa.MSL.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01051/high_coverage_alignment/HG01051.wgs.ILLUMINA.bwa.PUR.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA19625/high_coverage_alignment/NA19625.wgs.ILLUMINA.bwa.ASW.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01583/high_coverage_alignment/HG01583.wgs.ILLUMINA.bwa.PJL.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG03742/high_coverage_alignment/HG03742.wgs.ILLUMINA.bwa.ITU.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA20502/high_coverage_alignment/NA20502.wgs.ILLUMINA.bwa.TSI.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA18525/high_coverage_alignment/NA18525.wgs.ILLUMINA.bwa.CHB.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG02922/high_coverage_alignment/HG02922.wgs.ILLUMINA.bwa.ESN.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA19648/high_coverage_alignment/NA19648.wgs.ILLUMINA.bwa.MXL.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00419/high_coverage_alignment/HG00419.wgs.ILLUMINA.bwa.CHS.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01112/high_coverage_alignment/HG01112.wgs.ILLUMINA.bwa.CLM.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA19017/high_coverage_alignment/NA19017.wgs.ILLUMINA.bwa.LWK.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00268/high_coverage_alignment/HG00268.wgs.ILLUMINA.bwa.FIN.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG02568/high_coverage_alignment/HG02568.wgs.ILLUMINA.bwa.GWD.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01500/high_coverage_alignment/HG01500.wgs.ILLUMINA.bwa.IBS.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA18939/high_coverage_alignment/NA18939.wgs.ILLUMINA.bwa.JPT.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG03642/high_coverage_alignment/HG03642.wgs.ILLUMINA.bwa.STU.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG03006/high_coverage_alignment/HG03006.wgs.ILLUMINA.bwa.BEB.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00759/high_coverage_alignment/HG00759.wgs.ILLUMINA.bwa.CDX.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/NA20845/high_coverage_alignment/NA20845.wgs.ILLUMINA.bwa.GIH.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01595/high_coverage_alignment/HG01595.wgs.ILLUMINA.bwa.KHV.high_cov_pcr_free.20140203.bam
ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG01565/high_coverage_alignment/HG01565.wgs.ILLUMINA.bwa.PEL.high_cov_pcr_free.20140203.bam
```

## Reference Genomes
These analyses require two different reference genomes:

1) hg19 - We downloaded the UCSC version of hg19 available from the Broad Institute's
Resource bundle: https://software.broadinstitute.org/gatk/download/bundle

2) The 24 1000 genomes bam files require a specific build of the Grch37 reference
called "human_g1k_v37_decoy.fasta", also available from the Broad's resource
Bundle: https://software.broadinstitute.org/gatk/download/bundle

## Directory Structure
This directory - "Webster_etal_2018" - should contain the main snakefile ("snakefile"), the configuration file for the snakefile ("Webster_etal_2018_xyalign.config.json"),
a .gitignore, two conda environment files (ending in .yml), and five subdirectories ("fastqs", "misc", "processed_bams", "reference", and "xyalign_analyses").

Of the five subdirectories, "fastqs" and "reference" are provided as options for
depositing the raw fastqs and reference genomes (see above) for easy organization
and access.  However, the files don't have to be in these directories.  Either way,
at the top of the snakefile, you need to set a handful of variables including
the fastq directory that you're using and the paths to your various reference genomes.

## Running snakemake
Snakemake requires Python 3 and can easily be installed via pip or conda.  See
the [Snakemake documentation for more information about installing](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html).

XYalign, however, requires Python 2 (a requirement for Platypus), so we recommend
installing an XYalign-specific conda environment.  The snakefile is designed
to activate this environment for rules involving XYalign.  The [installation section
of the XYalign documentation has information about how to set up this environment](http://xyalign.readthedocs.io/en/latest/installation.html).

To reproduce our analyses exactly, we have included yml files with the contents
(including versions) of the Anaconda environments we used. You can create these environments
with the commands (from this directory):

```
conda env create -f snakemake_environment.yml
conda env create -f xyalign_environment.yml
```
Note that these environments will only work as-is in Linux environments and
might require a bit of tweaking to install on a Mac

Then, to run analyses, simply call Snakemake and provide it the path to the snakefile.
However, Snakemake allows users to distribute jobs across a cluster, so we added parameters
to enable this functionality.  We ran our analyses on a cluster using Slurm with the following command from this directory:

```
snakemake --snakefile snakefile -j 8 --cluster "sbatch -n 4 --nodes 1 -t 96:00:00 "
```

## Citations
Koster and Rahmann. 2012. Snakemake - a scalable bioinformatics workflow engine.
Bioinformatics 28: 2520-2522.

Webster TH et al. 2018. Identifying, understanding, and correcting technical
biases on the sex chromosomes in next-generation sequencing data.
