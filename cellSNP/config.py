# config.py - configuration


import sys


class Config:
    def __init__(self):
        self.defaults = Defaults()

        # command-line arguments/parameters.
        self.sam_fn = None
        self.sam_list_fn = None
        self.barcode_fn = None
        self.sample_ids = None
        self.sample_id_fn = None
        self.snp_fn = None
        self.out_dir = None
        self.debug = self.defaults.DEBUG

        self.chrom_str = None
        self.refseq_fn = None
        self.cell_tag = self.defaults.CELL_TAG
        self.umi_tag = self.defaults.UMI_TAG
        self.ncores = self.defaults.NCORES
        
        # snp filtering.
        self.min_count = self.defaults.MIN_COUNT
        self.min_maf = self.defaults.MIN_MAF
        
        # read filtering.
        self.min_mapq = self.defaults.MIN_MAPQ
        self.min_len = self.defaults.MIN_LEN
        self.max_depth = self.defaults.MAX_DEPTH
        self.incl_flag = self.defaults.INCL_FLAG
        self.excl_flag = -1
        self.no_orphan = self.defaults.NO_ORPHAN


        # internal parameters.
        
        # is_target : bool
        #   Whether the provided SNP list should be used as target
        #   (like -T in samtools/bcftools mpileup).
        self.is_target = False

        # is_out_zip : bool
        #   Whether output files need to be zipped.
        self.is_out_zip = False
        
        # is_genotype : bool
        #   Whether need to do genotyping in addition to pileup.
        self.is_genotype = False
        
        # out_prefix : str
        #   The prefix of the output files.
        self.out_prefix = COMMAND
        

    def show(self, fp = None, prefix = ""):
        if fp is None:
            fp = sys.stdout

        s =  "%s\n" % prefix
        s += "%ssam_file = %s\n" % (prefix, self.sam_fn)
        s += "%ssam_list_file = %s\n" % (prefix, self.sam_list_fn)
        s += "%sbarcode_file = %s\n" % (prefix, self.barcode_fn)
        s += "%ssample_ids = %s\n" % (prefix, self.sample_ids)
        s += "%ssample_id_file = %s\n" % (prefix, self.sample_id_fn)
        s += "%ssnp_file = %s\n" % (prefix, self.snp_fn)
        s += "%sout_dir = %s\n" % (prefix, self.out_dir)
        s += "%sdebug_level = %d\n" % (prefix, self.debug)
        s += "%s\n" % prefix

        s += "%schrom_str = %s\n" % (prefix, self.chrom_str)
        s += "%srefseq_fn = %s\n" % (prefix, self.refseq_fn)
        s += "%scell_tag = %s\n" % (prefix, self.cell_tag)
        s += "%sumi_tag = %s\n" % (prefix, self.umi_tag)
        s += "%snumber_of_cores = %d\n" % (prefix, self.ncores)
        s += "%s\n" % prefix
        
        # snp filtering.
        s += "%smin_count = %d\n" % (prefix, self.min_count)
        s += "%smin_maf = %f\n" % (prefix, self.min_maf)
        s += "%s\n" % prefix

        # read filtering.
        s += "%smin_mapq = %d\n" % (prefix, self.min_mapq)
        s += "%smin_len = %d\n" % (prefix, self.min_len)
        s += "%smax_depth = %d\n" % (prefix, self.max_depth)
        s += "%sinclude_flag = %d\n" % (prefix, self.incl_flag)
        s += "%sexclude_flag = %d\n" % (prefix, self.excl_flag)
        s += "%sno_orphan = %s\n" % (prefix, self.no_orphan)
        s += "%s\n" % prefix

        
        # internal parameters.
        s += "%sis_target = %s\n" % (prefix, str(self.is_target))
        s += "%sis_out_zip = %s\n" % (prefix, str(self.is_out_zip))
        s += "%sis_genotype = %s\n" % (prefix, str(self.is_genotype))
        s += "%sout_prefix = %s\n" % (prefix, self.out_prefix)
        s += "%s\n" % prefix

        fp.write(s)


    def use_barcodes(self):
        return self.cell_tag is not None

    def use_umi(self):
        return self.umi_tag is not None



class Defaults:
    def __init__(self):
        self.DEBUG = 0
        self.NCORES = 1
        
        self.NCHROMS = 22
        self.CELL_TAG = "CB"
        self.UMI_TAG = "UB"
        self.UMI_TAG_BC = "UB"    # the default umi tag for 10x data.

        self.MIN_COUNT = 20
        self.MIN_MAF = 0.0
        
        self.MIN_MAPQ = 20
        self.MIN_LEN = 30
        self.MAX_DEPTH = 0        # max depth for one site of one file, 0 means highest possible value.
        self.INCL_FLAG = 0
        self.EXCL_FLAG_UMI = 772
        self.EXCL_FLAG_XUMI = 1796
        self.NO_ORPHAN = True



if __name__ == "__main__":
    conf = Config()
    conf.show()
