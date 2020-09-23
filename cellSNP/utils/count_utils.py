# Utilility functions for count reads in each feature
# Author: Yuanhua Huang
# Date: 27/04/2020

## Note, this is a very basic read counting for features

import os
import gzip 
import sys
import pysam
import numpy as np
from .base_utils import id_mapping, unique_list
from .pileup_utils import check_pysam_chrom
from ..version import __version__

global CACHE_CHROM
global CACHE_SAMFILE
CACHE_CHROM = None
CACHE_SAMFILE = None

class Region:
    '''
    @abstract      A wrapper for different region formats, e.g. bed/gff
    @param chrom   Chromosome name [str]
    @param start   Start pos of this region: 1-based, included [int]
    @param stop    End pos of this region: 1-based, included [int]
    @param _id     Region ID [str]
    '''
    def __init__(self, chrom=None, start=None, stop=None, _id=None):
        self.chrom = chrom
        self.start = start
        self.stop = stop
        self.id = _id
    
def bed2reg(bed_file):
    """
    @abstract        Get list of regions (1-based) from bed file
    @param bed_file  Path to bed file [str]
    @return          A list of Region objects if success, None otherwise [list]
    """
    if not bed_file or not os.path.isfile(bed_file):
        return None

    lines = None
    if os.path.splitext(bed_file)[1] in (".gz", ".gzip"):
        with gzip.open(bed_file, "rt") as zfp:
            lines = zfp.readlines()
    else:
        with open(bed_file, "r") as fp:
            lines = fp.readlines()
    
    reg_list = []
    for idx, ln in enumerate(lines):   # it's probably fine to use enumerate here for bed files are usually small.
        parts = ln[:-1].split("\t")
        try:
            start, stop = int(parts[1]), int(parts[2])
            _id = "%s:%d-%d" % (parts[0], start + 1, stop)
        except (IndexError, ValueError) as e:
            print("Error: invalid bed record in No.%d line: %s" % (idx + 1, str(e)))
            return None
        reg_list.append(Region(parts[0], start + 1, stop, _id))

    return reg_list

def chr2reg(chrom, sam_fp, bin_size):
    """
    @abstract        Split the chromosome to several fixed-size bins.
    @param chrom     Chromosome name [str]
    @param sam_fp    The AlignmentFile object whose header will be used to extract chrom length [pysam.AlignmentFile]
    @param bin_size  Size of the bin, an integer [int]
    @return          A list of Region objects if success, None otherwise [list]
    """
    if chrom not in sam_fp.references:
        chrom = chrom[3:] if chrom.startswith("chr") else "chr" + chrom
        if chrom not in sam_fp.references:
            return None

    total_len = sam_fp.get_reference_length(chrom)
    bin_size = int(bin_size)
    if not total_len or total_len <= 0 or bin_size <= 0: 
        return None
    nbins = total_len // bin_size
    if total_len % bin_size != 0: nbins += 1

    reg_list = []
    for i in range(nbins):
        start = bin_size * i + 1
        stop = bin_size * (i + 1)
        _id = "%s:%d-%d" % (chrom, start, stop)
        reg_list.append(Region(chrom, start, stop, _id))
    
    return reg_list

def gene2reg(genes):
    """
    @abstract     Create regions from gff genes
    @param genes  A list/set/tuple of @class Genes [list/set/tuple]
    @return       A list of Region objects if success, None otherwise [list]
    """
    return [Region(g.chrom, g.start, g.stop, g.geneID) for g in genes]

def fetch_reads(sam_file, region, cell_tag="CR", UMI_tag="UR", min_MAPQ=20, 
                max_FLAG=255, min_LEN=30):
    """ Fetch all reads mapped to a given region.
    Filtering is also applied, including cell and UMI tags and read mapping 
    quality.
    """
    if sam_file is None or region is None:
        if sam_file is None:
            print("Warning: samFile is None")
        if region is None:
            print("Warning: region is None")
        return np.array([]), np.array([])

    samFile, _chrom = check_pysam_chrom(sam_file, region.chrom)
    
    UMIs_list, cell_list = [], []
    for _read in samFile.fetch(_chrom, region.start - 1, region.stop):
        ## filtering reads
        # this might be further speed up
        overhang = sum((np.array(_read.positions) >= (region.start - 1)) *   
                       (np.array(_read.positions) <= (region.stop - 1)))

        if _read.mapq < min_MAPQ or _read.flag > max_FLAG or overhang < min_LEN: 
            continue
            
        if cell_tag is not None and _read.has_tag(cell_tag) == False: 
            continue
        if UMI_tag is not None and _read.has_tag(UMI_tag) == False: 
            continue
            
        if UMI_tag is not None:
            UMIs_list.append(_read.get_tag(UMI_tag))
        if cell_tag is not None:
            cell_list.append(_read.get_tag(cell_tag))

    if len(cell_list) > 0 and len(cell_list) == len(UMIs_list):
        UMI_cell = [UMIs_list[x] + cell_list[x] for x in range(len(UMIs_list))]
        UMI_cell, idx, cnt = unique_list(UMI_cell)
        cell_list = [cell_list[x] for x in idx]
    
    cell_list_uniq, idx, read_count = unique_list(cell_list)

    return cell_list_uniq, read_count

def feature_count(sam_file, barcodes, region, reg_index, cell_tag, UMI_tag, 
    min_MAPQ, max_FLAG, min_LEN):
    """Fetch read count for a given feature.
    """
    cell_list_uniq, read_count = fetch_reads(sam_file, region, cell_tag, UMI_tag, 
        min_MAPQ, max_FLAG, min_LEN)

    if len(cell_list_uniq) > 0:
        match_idx = id_mapping(cell_list_uniq, barcodes, uniq_ref_only=True, 
            IDs2_sorted=True)
        match_idx = np.array(match_idx, dtype = float)

        idx1 = np.where(match_idx == match_idx)[0] #remove None
        idx2 = match_idx[idx1].astype(int)
        
        out_list = []
        for j in range(len(idx2)):
            out_list.append("%d\t%d\t%d" %(reg_index, idx2[j], read_count[idx1[j]]))
        return "\n".join(out_list) + "\n"
    else:
        return None
