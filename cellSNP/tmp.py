# main.py


import pysam
import sys
from .app import APP, VERSION
from .config import Config



def usage(conf, fp = sys.stdout):
    s =  "\n"
    s += "Version: %s (pysam %s)\n" % (VERSION, pysam.__version__)
    s += "Usage:   %s [options]\n" % APP
    s += "\n"
    s += "Options:\n"
    s += "  -s, --samFile STR        Indexed BAM/CRAM file(s), comma separated multiple samples.\n"
    s += "  -S, --samFileList FILE   A file listing BAM/CRAM files, each per line.\n"
    s += "  -O, --outDir DIR         Output directory for VCF and sparse matrices.\n"
    s += "  -R, --regionsVCF FILE    A vcf file listing all candidate SNPs, for fetch each variants.\n"
    s += "  -T, --targetsVCF FILE    Similar as -R, but the next position is accessed by streaming rather\n"
    s += "                           than indexing/jumping (like -T in samtools/bcftools mpileup).\n"
    s += "  -b, --barcodeFile FILE   A plain file listing all effective cell barcodes.\n"
    s += "  -i, --sampleList FILE    A list file containing sample IDs, each per line.\n"
    s += "  -I, --sampleIDs STR      Comma separated sample IDs.\n"
    s += "  -V, --version            Print software version and exit.\n"
    s += "  -h, --help               Show this help message and exit.\n"
    s += "\n"
    s += "Optional arguments:\n"
    s += "  --genotype           If use, do genotyping in addition to counting.\n"
    s += "  --gzip               If use, the output files will be zipped into BGZF format.\n"
    s += "  --printSkipSNPs      If use, the SNPs skipped when loading VCF will be printed.\n"
    s += "  -p, --nproc INT      Number of threads [%d]\n" % conf.NCORES
    s += "  -f, --refseq FILE    Faidx indexed reference sequence file. If set, the real (genomic)\n"
    s += "                       ref extracted from this file would be used for Mode 2 or for the\n"
    s += "                       missing REFs in the input VCF for Mode 1.\n"
    s += "  --chrom STR          The chromosomes to use, comma separated [1 to %d]\n" % conf.NCHROMS
    s += "  --cellTAG STR        Tag for cell barcodes, turn off with None [%s]\n" % conf.CELL_TAG
    s += "  --UMItag STR         Tag for UMI: UB, Auto, None. For Auto mode, use UB if barcodes are inputted,\n"
    s += "                       otherwise use None. None mode means no UMI but read counts [%s]\n" % conf.UMI_TAG
    s += "  --minCOUNT INT       Minimum aggragated UMI or read count [%d]\n" % conf.MIN_COUNT
    s += "  --minMAF FLOAT       Minimum minor allele frequency [%.2f]\n" % conf.MIN_MAF
    s += "\n"
    s += "Read filtering:\n"
    s += "  --inclFLAG STR|INT   Required flags: skip reads with all mask bits unset [%d]\n" % conf.INCL_FLAG
    s += "  --exclFLAG STR|INT   Filter flags: skip reads with any mask bits set [%d\n" % conf.EXCL_FLAG_UMI
    s += "                       (when use UMI) or %d (otherwise)]\n" % conf.EXCL_FLAG_XUMI
    s += "  --minLEN INT         Minimum mapped length for read filtering [%d]\n" % conf.MIN_LEN
    s += "  --minMAPQ INT        Minimum MAPQ for read filtering [%d]\n" % conf.MIN_MAPQ
    s += "  --maxDEPTH INT       At a position, read maximally INT reads per input file, to avoid\n"
    s += "                       excessive memory usage; 0 means highest possible value [%d]\n" % conf.MAX_DEPTH
    s += "  --countORPHAN        If use, do not skip anomalous read pairs.\n"
    s += "\n"
                                       
    fp.write(s)


                                       
def main():
    conf = Config()

    if len(sys.argv) <= 1:
        usage(conf.defaults, fp = sys.stdout)
        sys.exit(0)

    #init_logging(stream = sys.stdout)

    opts, args = getopt.getopt(
        args = argv[1:],
        shortopts = "", 
        longopts = [
            "sam=", "samList=", 
            "barcode=", "sampleList=",
            "snpvcf=", "region=",
            "outdir=",
            "gmap=", "eagle=", "paneldir=",
            "version", "help",

            "refCell=",
            "cellTAG=", "UMItag=",
            "minCOUNT=", "minMAF=",
            "ncores="
        ])

    for op, val in opts:
        if len(op) > 2:
            op = op.lower()
        if op in ("--label"): label = val
        elif op in ("--sam"): sam_fn = val
        elif op in ("--samlist"): sam_list_fn = val
        elif op in ("--barcode"): barcode_fn = val
        elif op in ("--samplelist"): sample_id_fn = val
        elif op in ("--snpvcf"): snp_vcf_fn = val
        elif op in ("--region"): region_fn = val
        elif op in ("--outdir"): out_dir = val
        elif op in ("--gmap"): gmap_fn = val
        elif op in ("--eagle"): eagle_fn = val
        elif op in ("--paneldir"): panel_dir = val
        elif op in ("--version"): sys.stdout.write(VERSION + "\n"); sys.exit(0)
        elif op in ("--help"): usage(); sys.exit(0)

        elif op in ("--refcell"): ref_cell_fn = val
        elif op in ("--celltag"): cell_tag = val
        elif op in ("--umitag"): umi_tag = val
        elif op in ("--mincount"): min_count = int(val)
        elif op in ("--minmaf"): min_maf = float(val)
        elif op in ("--ncores"): ncores = int(val)     # keep it in `str` format.
        else:
            error("invalid option: '%s'." % op)
            return(-1)
        
    ret = pipeline_wrapper(
        label = label,
        sam_fn = sam_fn, sam_list_fn = sam_list_fn, 
        barcode_fn = barcode_fn, sample_id_fn = sample_id_fn,
        snp_vcf_fn = snp_vcf_fn, region_fn = region_fn,
        out_dir = out_dir,
        gmap_fn = gmap_fn, eagle_fn = eagle_fn, panel_dir = panel_dir,
        ref_cell_fn = ref_cell_fn,
        cell_tag = cell_tag, umi_tag = umi_tag,
        min_count = min_count, min_maf = min_maf,
        ncores = ncores
    )
    
    info("All Done!")

    return(ret)