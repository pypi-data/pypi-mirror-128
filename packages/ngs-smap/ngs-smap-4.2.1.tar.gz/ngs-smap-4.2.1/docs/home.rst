####
home
####


Introduction
------------

Welcome to the manual of the SMAP-package.

**SMAP** is a software package that analyzes read mapping distributions and performs haplotype calling to create multi-allelic molecular markers.  
**SMAP** haplotyping works on:  

* all types of **samples**, including (di- and polyploid) individuals and Pool-Seq.  
* reads of various **library types**, including Genotyping-by-Sequencing (GBS), highly multiplex amplicon sequencing (HiPlex), and Shotgun sequencing (including Whole Genome Sequencing (WGS), targetted resequencing like Probe Capture, and RNA-Seq).  
* all NGS **sequencing technologies** like Illumina short reads and PacBio or Oxford Nanopore long reads.  

**SMAP delineate** analyses read mapping distributions for GBS read mapping QC, defines read mapping polymorphisms *within* loci and *across* samples, and selects high quality loci across the sample set for downstream analyses.  
**SMAP compare** identifies the overlap between two sets of loci (e.g. common loci across two runs of SMAP delineate).  
**SMAP haplotype-sites** performs read-backed haplotyping using *a priori* known polymorphic SNP sites, and creates \`ShortHaps´\. SMAP haplotype-sites also captures GBS read mapping polymorphisms (here called \`SMAPs´\) as a *novel* genetic diversity marker type, and integrates those with SNPs for ShortHap haplotyping.

----

Global overview
---------------

The scheme below displays a global overview of the functionalities of the SMAP-package. White ovals are external operations and grey ovals are components of SMAP. Square boxes show the output of each of the components. Arrows show how output from various components are required input for the next component in the workflow for each of the NGS library types (GBS (red), HiPlex (purple), Shotgun (yellow)), file formats are shown in uppercase italics.
Haplotype calling is implemented in the component **haplotype-sites** (for ShortHaps).

.. image:: ./images/SMAP_global_overview_sites_WGS.png

----

Installation
------------

The latest release of the SMAP-package can be found on the `Gitlab repository <https://gitlab.com/truttink/smap/-/releases/>`_, where `INSTALL.md <https://gitlab.com/truttink/smap/-/blob/master/INSTALL.md>`_ describes the installation guidelines.
Running SMAP on GBS data requires special preprocessing of reads before read mapping. Please use instructions and software for GBS read preprocessing as described in the manual of `GBprocesS <https://gbprocess.readthedocs.io/en/latest/index.html>`_. 

Quick installation in a virtual environment::

    git clone https://gitlab.com/truttink/smap.git
    cd smap
    git checkout master
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install .

Or, using Docker::

    docker run dschaumont/smap --help
    
| SMAP is only available for linux operating systems.
| A basic guide for running software on the linux command line can be found on `Ubuntu <https://ubuntu.com/tutorials/command-line-for-beginners#1-overview>`_'s site.

----

Detailed information of components
----------------------------------

Check out detailed information on each of the three components:

* **SMAP** :ref:`delineate <SMAPdelindex>` analyses reference-aligned GBS reads by building a catalogue of loci within BAM files, whereby the start and end of \`Stacks´ \ of reads define Stack Mapping Anchor Points (SMAPs). SMAP delineate then merges Stacks within a BAM file to create StackClusters. These StackClusters are then merged across multiple BAM files to build a catalogue of MergedClusters. Thus, SMAP delineate creates an overview of read mapping positions of GBS loci across sample sets and provides for quality control of read preprocessing and mapping procedures, before SNP calling and haplotyping.
* **SMAP** :ref:`compare <SMAPcompindex>` identifies the number of common loci across two runs of SMAP delineate. It is a useful tool to determine the number of common loci targeted by different NGS methods, in different populations, sample sets, or bioinformatics filtering procedures, etc. This, in turn, helps to optimize NGS library preparation parameters and bioinformatics parameters throughout the entire workflow.
* **SMAP** :ref:`haplotype-sites <SMAPhaploindex>` generates haplotype calls (ShortHaps) using sets of polymorphic \`sites´ \ for read-backed haplotyping on reference-aligned sequencing reads. Polymorphic \`sites´ \ include Stack Mapping Anchor Points (SMAPs, defined in a BED file created with SMAP delineate) and SNPs (as VCF obtained from third-party algorithms) for the same set of BAM files. It creates an integrated table (sample x genotype call matrix) with discrete haplotype calls (for individuals) or relative haplotype frequencies (for Pool-Seq) for any number of samples and loci.
* **SMAP** :ref:`Utilities <SMAP_utilities_index>` contain python scripts to create BED files with SMAPs to delineate loci for HiPlex and Shotgun data.

