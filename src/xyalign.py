from __future__ import division
import argparse
import os
import subprocess
import sys
from collections import Counter, defaultdict
from itertools import chain
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pybedtools
import pysam
import seaborn as sns

def main():
	""" Main program"""
	
	args = parse_args()
	
	## First round of Platypus calling and plotting
	if args.platypus_calling == "both" or "before":
		a = platypus_caller(args.bam, args.ref, args.chromosomes, args.cpus, args.output_dir + "/{}.noprocessing.vcf".format(args.sample_id))
		if a != 0:
			print "Error in initial Platypus calling."
			sys.exit(1)
		if args.no_variant_plots == True:
			plot_variants_per_chrom(args.chromosomes, args.output_dir + "/{}.noprocessing.vcf".format(args.sample_id),
									args.sample_id, args.output_dir, args.variant_quality_cutoff,
									args.marker_size, args.marker_transparency,
									get_length(pysam.AlignmentFile(args.bam, "rb"), i))
	
	## Analyze bam for depth and mapq
	samfile = pysam.AlignmentFile(args.bam, "rb")
	pass_df = []
	fail_df = []
	for chromosome in args.chromosomes:
		data = traverse_bam_fetch(samfile, chromosome, args.window_size)
		tup = make_region_lists(data["windows"], args.mapq_cutoff, args.depth_filter)
		pass_df.append(tup[0])
		fail_df.append(tup[1])
		plot_depth_mapq(data, args.output_dir)
	output_bed(os.path.join(args.output_dir, args.high_quality_bed), *pass_df)
	output_bed(os.path.join(args.output_dir, args.low_quality_bed), *fail_df)
	
	## Infer ploidy
	
	## Remapping
	
	
	## Final round of calling and plotting
									
			




		
	
def parse_args():
	"""Parse command-line arguments"""
	parser = argparse.ArgumentParser(description="XYalign.  A tool to estimate sex chromosome ploidy and use this information to correct mapping and variant calling on the sex chromosomes.")
	parser.add_argument("--bam", required=True,
						help="Input bam file.")
	parser.add_argument("--ref", required=True,
						help="Path to reference sequence (including file name).")
	parser.add_argument("--chromosomes", "-c", nargs="+", default=["chrX","chrY","chr19"],
						help="Chromosomes to analyze.")
	parser.add_argument("--sample_id", "-id", default="sample",
						help="Name/ID of sample - for use in plot titles and file naming.")
	parser.add_argument("--platypus_calling", default="both",
						help="Platypus calling withing the pipeline (before processing, after processing, both, or neither). Options: both, none, before, after.")
	parser.add_argument("--no_variant_plots", action="store_false", default=True,
						help="Include flag to prevent plotting read balance from VCF files.")
	parser.add_argument("--variant_quality_cutoff", "-vqc", type=int, default=20,
						help="Consider all SNPs with a quality greater than or equal to this value. Default is 20.")
	parser.add_argument("--marker_size", type=float, default=1.0,
						help="Marker size for genome-wide plots in matplotlib.")
	parser.add_argument("--marker_transparency", "-mt", type=float, default=0.5,
						help="Transparency of markers in genome-wide plots.  Alpha in matplotlib.")
	parser.add_argument("--cpus", type=int, default=1,
						help="Number of cores/threads to use.")
	parser.add_argument("--window_size", "-w", type=int, default=50000,
						help="Window size (integer) for sliding window calculations.")
	parser.add_argument("--mapq_cutoff", "-mq", type=int, default=20,
						help="Minimum mean mapq threshold for a window to be considered high quality.")
	parser.add_argument("--depth_filter", "-df", type=float, default=4.0,
						help="Filter for depth (f), where the threshold used is mean_depth +- (f * square_root(mean_depth)).")
	parser.add_argument("--high_quality_bed", "-hq", default="highquality.bed",
						help="Name of output file for high quality regions.")
	parser.add_argument("--low_quality_bed", "-lq", default="lowquality.bed",
						help="Name of output file for high quality regions.")
	parser.add_argument("--output_dir", "-o",
						help="Output directory")
						
	args = parser.parse_args()
	
	#Validate arguments
	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)
	if args.platypus_calling not in ["both", "none", "before", "after"]:
		print "Error. Platypus calling must be both, none, before, or after. Default is both."
		sys.exit(1)
		
	# Return arguments namespace
	return args
	

def get_length(bamfile, chrom):
	""" Extract chromosome length from BAM header.
	
	args:
		bamfile: pysam AlignmentFile object
		chrom: chromosome name (string)
		
	returns:
		Length (int)
	
	"""

						
def platypus_caller(bam, ref, chroms, cpus, output_file):
	""" Uses platypus to make variant calls on provided bam file
	
	bam is input bam file
	ref is path to reference sequence
	chroms is a list of chromosomes to call on, e.g., ["chrX", "chrY", "chr19"]
	cpus is the number of threads/cores to use
	output_file is the name of the output vcf
	"""
	regions = ','.join(map(str,chroms))
	command_line = "platypus callVariants --bamFiles {} -o {} --refFile {} --nCPU {} --regions {} --assemble 1".format(bam, output_file, ref, cpus, regions)
	return_code = subprocess.call(command_line, shell=True)
	return return_code
		
def parse_platypus_VCF(filename, qualCutoff, chrom):
	""" Parse vcf generated by Platypus """
	infile = open("{}".format(filename),'r')
	positions = []
	quality = []
	readBalance = []
	for line in infile:
		if line[0] != chrom:
			continue
		cols=line.strip('\n').split('\t')
		pos = int(cols[1])
		qual = float(cols[5])
		if qual < qualCutoff:
			continue
		TR = cols[7].split(';')[17].split('=')[1]
		TC = cols[7].split(';')[14].split('=')[1]
		if ',' in TR or ',' in TC:
			continue
		if (float(TR)==0) or (float(TC) == 0):
			continue
		ReadRatio = float(TR)/float(TC)
		
		# Add to arrays
		readBalance.append(ReadRatio)
		positions.append(pos)
		quality.append(qual)
	return (positions,quality,readBalance)
	
def plot_read_balance(chrom, positions, readBalance, sampleID, output_prefix, MarkerSize, MarkerAlpha, Xlim):
    """ Plots read balance at each SNP along a chromosome """
    if "x" in chrom.lower():
        Color="green"
    elif "y" in chrom.lower():
        Color = "blue"
    else:
    	Color = "red"
    fig = plt.figure(figsize=(15,5))
    axes = fig.add_subplot(111)
    axes.scatter(positions,readBalance,c=Color,alpha=MarkerAlpha,s=MarkerSize,lw=0)
    axes.set_xlim(0,Xlim)
    axes.set_title(sampleID)
    axes.set_xlabel("Chromosomal Coordinate")
    axes.set_ylabel("Read Balance")
    #print(len(positions))
    plt.savefig("{}_{}_ReadBalance_GenomicScatter.svg".format(output_prefix, chrom))
    plt.savefig("{}_{}_ReadBalance_GenomicScatter.png".format(output_prefix, chrom))
	#plt.show()
	
def hist_read_balance(chrom, readBalance, sampleID, output_prefix):
    """ Plot a histogram of read balance """
    if "x" in chrom.lower():
        Color="green"
    elif "y" in chrom.lower():
        Color = "blue"
    else:
    	Color = "red"
    fig = plt.figure(figsize=(8,8))
    axes = fig.add_subplot(111)
    axes.set_title(sampleID)
    axes.set_xlabel("Read Balance")
    axes.set_ylabel("Frequency")
    axes.hist(readBalance,bins=50,color=Color)
    plt.savefig("{}_{}_ReadBalance_Hist.svg".format(output_prefix, chrom))
    plt.savefig("{}_{}_ReadBalance_Hist.png".format(output_prefix, chrom))
	#plt.show()

def plot_variants_per_chrom(chrom_list, vcf_file, sampleID, output_directory, qualCutoff, MarkerSize, MarkerAlpha, Xlim):
	for i in chrom_list:
		parse_results = parse_platypus_VCF(vcf_file, qualCutoff, i)
		plot_read_balance(i, parse_results[0], parse_results[1], sampleID, output_directory + "{}.noprocessing".format(sampleID), MarkerSize, MarkerAlpha, Xlim, i)
		hist_read_balance(i, readBalance, sampleID, output_directory + "{}.noprocessing".format(sampleID))
	pass
	

def traverse_bam_fetch(samfile, chrom, window_size):
	"""Analyze the `samfile` BAM file for various metrics and statistics.
	Currently, this function looks at the following metrics across genomic windows:
	- Read depth
	- Mapping quality
	The average of each metric will be calculated for each window of
	size `window_size` and stored altogether in a pandas data frame.
	Returns a dictionary of pandas data frames with the following key:
	- windows: The averages for each metric for each window
	"""
	chr_len = get_length(samfile, chrom)
	num_windows = chr_len // window_size + 1
	if chr_len % num_windows == 0:
		last_window_len = window_size
	else:
		last_window_len = chr_len % num_windows
	
	window_id = 0
	win_pos = 0
	
	chr_list = [chrom] * num_windows
	start_list = []
	stop_list = []
	depth_list = []
	mapq_list = []
	
	start = 0
	end = window_size
	for window in range(0, num_windows):
		mapq = []
		num_reads = 0
		total_read_length = 0
		for read in samfile.fetch(chrom, start, end):
			num_reads += 1
			total_read_length += read.infer_query_length()
			mapq.append(read.mapping_quality)
		start_list.append(start)
		stop_list.append(end)
		depth_list.append(total_read_length / window_size)
		mapq_list.append(np.mean(np.asarray(mapq)))
		
		window_id += 1
		if window_id == num_windows - 1:
			start += window_size
			end += last_window_len
		else:
			start += window_size
			end += window_size

		# Print progress
		print "{} out of {} windows processed on {}".format(window_id, num_windows, chrom)

	# Convert data into pandas data frames
	windows_df = pd.DataFrame({
		"chrom": np.asarray(chr_list),
		"start": np.asarray(start_list),
		"stop": np.asarray(stop_list),
		"depth": np.asarray(depth_list),
		"mapq": np.asarray(mapq_list)
	})[["chrom", "start", "stop", "depth", "mapq"]]

	results = {"windows": windows_df}
	return results

def make_region_lists(depthAndMapqDf, mapqCutoff, sd_thresh):
	"""
	(pandas.core.frame.DataFrame, int, float) -> (list, list)
	return two lists of regions (keepList, excludeList) based on cutoffs for depth and mapq
	"""
	depth_mean = depthAndMapqDf["depth"].mean()
	depth_sd = depthAndMapqDf["depth"].std()

	depthMin = depth_mean - (sd_thresh * (depth_sd ** 0.5))
	depthMax = depth_mean + (sd_thresh * (depth_sd ** 0.5))

	good = (depthAndMapqDf.mapq > mapqCutoff) & (depthAndMapqDf.depth > depthMin) & (depthAndMapqDf.depth < depthMax)
	dfGood = depthAndMapqDf[good]
	dfBad = depthAndMapqDf[~good]
	
	return (dfGood, dfBad)


def output_bed(outBed, *regionDfs):
    '''
    (list, list, str) -> bedtoolsObject
    Take two sorted lists.  Each list is a list of tuples (chrom[str], start[int], end[int])
    Return a pybedtools object and output a bed file.
    '''
    dfComb = pd.concat(regionDfs)
    regionList = dfComb.ix[:, "chrom":"stop"].values.tolist()
    merge = pybedtools.BedTool(regionList).sort().merge()
    with open(outBed, 'w') as output:
    	output.write(str(merge))
    pass
	
def chromsomeWidePlot(chrom, positions, y_value, measure_name, chromosome, sampleID, MarkerSize, MarkerAlpha, Xlim, Ylim):
    '''
    Plots values across a chromosome, where the x axis is the position along the
    chromosome and the Y axis is the value of the measure of interest.
    
    positions is an array of coordinates 
    y_value is an array of the values of the measure of interest
    measure_name is the name of the measure of interest (y axis title)
    chromsome is the name of the chromosome being plotted
    sampleID is the name of the sample
    MarkerSize is the size in points^2
    MarkerAlpha is the transparency (0 to 1)
    Xlim is the maximum X value
    Ylim is the maximum Y value
    '''
    if "x" in chrom.lower():
        Color="green"
    elif "y" in chrom.lower():
        Color = "blue"
    else:
    	Color = "red"
    fig = plt.figure(figsize=(15,5))
    axes = fig.add_subplot(111)
    axes.scatter(positions,y_value,c=Color,alpha=MarkerAlpha,s=MarkerSize,lw=0)
    axes.set_xlim(0,Xlim)
    axes.set_ylim(0,Ylim)
    axes.set_title("%s - %s" % (sampleID, chromosome))
    axes.set_xlabel("Chromosomal Position")
    axes.set_ylabel(measure_name)
    plt.savefig("%s_%s_%s_GenomicScatter.svg" % (sampleID, chromsome, measure_name))
    plt.savefig("%s_%s_%s_GenomicScatter.png"% (sampleID, chromsome, measure_name))
    #plt.show()

def plot_depth_mapq(data_dict, output_dir):
	"""
	Takes a dictionary (output from traverseBam) and outputs histograms and
	genome-wide plots of various metrics.
	Args:
		data_dict: Dictionary of pandas data frames
		output_dir: Directory where the PNG file with the plots will be stored
	Returns:
		None
	"""

	window_df = None if "windows" not in data_dict else data_dict["windows"]
	depth_hist = None if "depth_freq" not in data_dict else data_dict["depth_freq"]
	readbal_hist = None if "readbal_freq" not in data_dict else data_dict["readbal_freq"]
	mapq_hist = None if "mapq_freq" not in data_dict else data_dict["mapq_freq"]

	chrom = window_df["chrom"][1]

	# Create genome-wide plots based on window means
	if window_df is not None:
		# depth plot
		depth_genome_plot_path = os.path.join(output_dir, "depth_windows." + chrom + ".png")
		depth_genome_plot = sns.lmplot('start', 'depth', data=window_df, fit_reg=False,
										scatter_kws={'alpha': 0.3})
		depth_genome_plot.savefig(depth_genome_plot_path)
		# mapping quality plot
		mapq_genome_plot_path = os.path.join(output_dir, "mapq_windows." + chrom + ".png")
		mapq_genome_plot = sns.lmplot('start', 'mapq', data=window_df, fit_reg=False)
		mapq_genome_plot.savefig(mapq_genome_plot_path)

	# Create histograms
	# TODO: update filenames dynamically like window_df above
	# TODO: update Count column name
	if depth_hist is not None:
		depth_bar_plot = sns.countplot(x='depth', y='Count', data=depth_hist)
		depth_bar_plot.savefig("depth_hist.png")
	if readbal_hist is not None:
		balance_bar_plot = sns.countplot(x='ReadBalance', y='Count', data=readbal_hist)
		balance_bar_plot.savefig("readbalance_hist.png")
	if mapq_hist is not None:
		mapq_bar_plot = sns.countplot(x='Mapq', y='Count', data=mapq_hist)
		mapq_bar_plot.savefig("mapq_hist.png")

if __name__ == "__main__":
	main()
	

	