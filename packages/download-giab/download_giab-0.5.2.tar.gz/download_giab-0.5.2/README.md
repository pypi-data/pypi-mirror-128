# download_giab

Utility Python package to download Genome-in-a-Bottle (GIAB) data from their 
[index files](https://github.com/genome-in-a-bottle/giab_data_indexes/).

This requires Python 3.6 or later.

To install, run the following:

```bash
pip install download_giab
```

If you're installing on a cluster, this might be more like:

```bash
pip install --user download_giab
```

To use, run something like the following:

```bash
download_giab https://raw.githubusercontent.com/genome-in-a-bottle/giab_data_indexes/master/AshkenazimTrio/sequence.index.AJtrio_Illumina300X_wgs_07292015.HG002
```

This will download everything in the linked index to the directory the utility is run from.
It can also download from local index files.

If you want to download lots of data and not have the program hang up upon session disconnect,
you can use `nohup` and `&`:

```bash
nohup download_giab https://raw.githubusercontent.com/genome-in-a-bottle/giab_data_indexes/master/AshkenazimTrio/sequence.index.AJtrio_Illumina300X_wgs_07292015.HG002 &
```

If you are downloading paired-end reads and want to concatenate all FASTQ files into two files,
you can use the `--cat-paired` flag. This will generate two files per sample: `[sample]_1.fastq.gz`
and `[sample]_2.fastq.gz`. If a sample ID is not present, the literal text `paired` will be used.
