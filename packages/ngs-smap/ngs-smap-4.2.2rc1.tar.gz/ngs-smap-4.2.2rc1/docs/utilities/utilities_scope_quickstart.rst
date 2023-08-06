.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

###########################
Scope & Quick Start
###########################

Scope
-----

Setting the stage
-----------------


In Shotgun sequencing, haplotypes are defined by a set of SNPs in a dynamic Sliding frame (start and end positions of the locus). The Sliding frames are typically defined as a region around known SNPs.  
A special case is the detection of the junctions of large-scale inversions or deletions, in which the breakpoint is taken as variable position flanked by two Anchor points immediately upstream and downstream.  
Here, we explain the main difference and provide instructions for setting the correct parameter settings. 

Defining the start and end point for haplotyping in Shotgun loci
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the insert size of Shotgun libraries sequenced with Illumina instruments is relatively short (300-500 bp for paired-end libraries), paired-end reads (2x150 bp) usually do not overlap in the middle of the fragment and can not be merged during preprocessing. Read mapping should still be performed in paired mode to increase specificity of mapping with `BWA-MEM <https://janis.readthedocs.io/en/latest/tools/bioinformatics/bwa/bwamem.html>`_. Because Shotgun reads may be mapped in any orientation , mode ``-mapping_orientation ignore`` should be used because then all reads are considered independent of mapping orientation.
In case short regions of adjacent SNPs are haplotyped, it is logical to only consider reads that span the entire locus. Otherwise, reads that only cover a part of the locus would create additional haplotypes marking absence of read coverage.  


				  | Stepwise delineation of sliding frames for read-backed haplotyping based on a-priori known SNPs.
				  | 1. The first SNP on the scaffold becomes the first SNP of Locus 1.
				  | The upstream off-set distance or the first nucleotide of the scaffold defines the 5’ start site of Locus 1.
				  | 2. All SNPs within the frame_length are considered for Locus 1.
				  | 3. Of the overlapping SNPs, the position of the last SNP within the frame length is determined.
				  | 4. The 3’ end site of Locus 1 is positioned at the off-set distance after the last SNP in Locus 1.
				  | 5. The first SNP after an empty space with length frame_distance after the 3‘ end of Locus 2, becomes the first SNP of Locus 2.
				  | 6. The off-set distance defines the 5’ start site of Locus 2.
				  | 7. All SNPs within the frame_length are considered for Locus 2.
				  | 8. Of the overlapping SNPs, the position of the last SNP within the frame length is determined.
				  | 9. The 3’ end site of Locus 2 is positioned at the off-set distance after the last SNP in Locus 2.
				  | 10. The first SNP after length frame_distance after the 3‘ end of Locus 2 becomes the first SNP of Locus 3.
				  | SNPs positioned in the frame-distance regions are ignored.
				  | 11. The off-set distance defines the 5’ start site of Locus 3.
				  | 12. All SNPs within the frame_length are considered for Locus 3.
				  | 13. If only one SNP exists, this becomes the last SNP.
				  | 14. The 3’ end site of Locus 3 is positioned at the off-set distance after the last SNP in Locus 3.
				  | 15. The first SNP after length frame_distance after the 3‘ end of Locus 3 becomes the first SNP of Locus 4.
				  | 16. The off-set distance defines the 5’ start site of Locus 4.
				  | 17. If the frame_length exceeds the remaining length of the scaffold, it is set at the last nucleotide of the scaffold.
				  | 18. The position of the last SNP within the frame length is determined for Locus 4.
				  | 19. The 3’ end site of Locus 4 is positioned at the off-set distance after the last SNP, or at the last nucleotide of the scaffold.
				  | Special cases:
				  | Off-set distances are used to ensure the sequence context around the SNPs are also covered by the same read.
				  | In this case, the outer 5‘ and 3’ positions delineating the Locus are used as ‘anchor points’ rather than as polymorphic SNPs
				  | and are used for evaluation of complete coverage of the read across the Locus length (option --partial exclude).
				  | If an off-set distance is defined as 0, the 5’ end corresponds to the first SNP, and the 3’ end of the Locus corresponds to the last SNP.
				  | If only one SNP exists within the frame_length, then the Locus is limited to length 1 and only the single SNP is scored as haplotype.
				  | SNPs positioned in the frame-distance regions are ignored.
				  | If the frame_distance is defined as 0, loci may become adjacent.
				  | Overlap of neighboring loci is avoided by reduction of the 5’ off-set on the downstream locus.
				  | Frame_length must always be greater than or equal to off-set.
				  | Frame_length must always be shorter than longest read length (ideally about one-half to two-thirds).
				  | Frame_length is a measure for the maximum length per Locus.
				  | Effective Locus length depends on SNP density combined with off-set and frame_length.
				  | what happens if last SNP + off-set is positioned outside frame_length? 
				  

:navy:`Haplotyping Sliding frames with adjacent SNPs`


.. image:: ../images/sites/Sliding_frames_SNPs.png

In any situation in which neighboring SNPs are spaced apart within the length of a read, read-backed haplotyping can be used to phase SNPs. Defining Sliding frames in which to group adjacent SNPs is a trade off between read depth, read length, and the density of SNPs. We recommend to create a set of BED files with varying frame length and test these for locus and sample call completeness and correctness, and haplotype diversity (number of different haplotypes observed per locus across te sample set).
As a rule of thumb, frame length at about one-half to two-thirds of the read length provides an optimal balance between read depth and haplotype diversity and is a good starting point for further optimization.

The Python script in the **SMAP utilities** folder transforms a simple VCF-formatted list of SNPs into a BED file with Sliding frames for **SMAP haplotype-sites**.

::

	python3 SMAP_SNPwindows.py --options

The same VCF file is then used as input for the variant sites in **SMAP haplotype-sites**
Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  

::

    smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore --no_indels -c 30 -f 5 -p 8 --plot_type png -partial exclude --min_distinct_haplotypes 1 -o haplotypes_25bp_regions --plot all --discrete_calls dosage -i diploid -z 2 -u "" --locus_correctness 80


:navy:`Haplotyping the junction sites of large structural variants such as deletions and inversions`

.. image:: ../images/sites/NatMeth_Fig1b.png

Short reads obtained by Shotgun sequencing may partially map onto the region directly flanking the junction of large structural variants. Typically, the MEM that seeds the alignment places the longest half of the read adjacent to the breakpoint, and the other half of the read is softclipped, or not matched to the reference genomee. This results in a sudden and clear drop in read depth around the breakpoint. This read mapping profile can be coded as haplotype by SMAP, because read-reference alignments are transformed to haplotypes while considering absence/presence of read mapping. 
The approach to score clean drops in read depth at SV mapping breakpoints is to define 3-bp loci with the breakpoint nucleotide as the central position, immediately flanked by an upstream and a downstream nucleotide position and score absence/presence per position.  

The Python script in the Utilities folder transforms a simple VCF-formatted list of breakpoints into a BED file for SMAP haplotype-sites with the following settings:

::

	python3 SMAP_SNPwindows.py --options

The same VCF file is then used as imput for the variant sites in **SMAP haplotype-sites**
Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  

::

    smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation ignore --no_indels -c 30 -f 5 -p 8 --plot_type png -partial exclude --min_distinct_haplotypes 1 -o haplotypes_25bp_regions --plot all --discrete_calls dosage -i diploid -z 2 -u "" --locus_correctness 80



:navy:`SMAP haplotype-sites: using polymorphic sites (SNPs, SVs, and/or SMAPs) for read-backed haplotyping`

| **SMAP haplotype-sites** reconstructs multi-allelic haplotypes based on a predefined set of polymorphisms at Single Nucleotide Polymorphisms (SNPs), breakpoints of Structural Variants (SVs) and/or Stack Mapping Anchor Points (:ref:`SMAPs <SMAPdeldef>`) through read-backed haplotyping.
| **SMAP haplotype-sites** can be used for \`stacked´ \ read data such as Genotyping-By-Sequencing (GBS) or highly multiplex amplicon sequencing (HiPlex), and for random fragmented (e.g. Shotgun Sequencing) read data.  

.. image:: ../images/sites/NatMeth_Fig1b.png

.. image:: ../images/sites/SMAP_sites_introduction_scheme.png

:navy:`SMAP haplotype-sites only requires this input:`
	
	1. a single BED file to define the start and end points of loci (loci created by :ref:`SMAP delineate <SMAPdelHIW>` for GBS, amplicon regions for HiPlex, and sliding frames for Shotgun sequencing).
	2. a single VCF file containing bi-allelic SNPs obtained with third-party SNP calling software.
	3. a set of indexed BAM files for all samples that need to be compared.

| **SMAP haplotype-sites** performs read-backed haplotyping, per sample, per locus, per read, using positional information of read alignments and creates multi-allelic haplotypes from a short string of polymorphic *sites* (ShortHaps).
| **SMAP haplotype-sites** takes a conservative approach, without any form of imputation or phase extension, and strictly considers SNPs and/or SMAPs within a read for read-backed haplotyping.
| **SMAP haplotype-sites** filters out genotype calls of loci with low read counts, and low frequency haplotypes, to control for noise in the data.
| **SMAP haplotype-sites** creates a multi-allelic genotype call matrix listing haplotype calls, per sample, per locus, across the sample set.
| **SMAP haplotype-sites** always returns quantitative haplotype frequencies, useful for Pool-Seq data.
| **SMAP haplotype-sites** can also create discrete haplotype calls (expressed as either dominant or dosage calls) for individual samples.
| **SMAP haplotype-sites** plots the haplotype frequency distribution per sample.
| **SMAP haplotype-sites** plots a histogram of the number of haplotypes per locus across the sample set to show the haplotype diversity.

:navy:`Loci with sets of polymorphic sites`

| In the SMAP haplotype-sites workflow, the user first selects loci known to be covered by reads across the sample set. For HiPlex data, pairs of primers define locus positions. SNPs identified by third-party software that are located within these loci are combined into haplotypes, all other SNPs and all other non-polymorphic positions are excluded. For Shotgun data, dynamic sliding frames are used that bundle neighboring SNPs, based on a VCF file with known SNPs obtained by third-party software. For GBS data, read mapping polymorphisms (SMAPs, see :ref:`SMAP delineate <SMAPdelsepvmerg>`) define locus positions and may be combined with SNPs as molecular markers for haplotyping. (See for third-party SNP calling software: `SAMtools <http://www.htslib.org/>`_, `BEDtools <https://bedtools.readthedocs.io/en/latest/index.html>`_, `Freebayes <https://github.com/ekg/freebayes>`_, or `GATK <https://gatk.broadinstitute.org/hc/en-us>`_ for individuals, or `SNAPE-pooled <https://github.com/EmanueleRaineri/snape-pooled>`_ for Pool-Seq data. See also `Veeckman et al, 2019 <https://academic.oup.com/dnaresearch/article/26/1/1/5133005>`_ for a comparison of methods).

----
 
.. _SMAP_utilities_quickstart:
 
Quick Start
-----------

.. tabs::

   .. tab:: overview
	  
	  | The scheme below shows how **SMAP haplotype-sites** is integrated with `preprocessing <https://gbprocess.readthedocs.io/en/latest/index.html>`_, :ref:`SMAP delineate <SMAPdelindex>` and SNP calling (white rounded boxes).
	  | Functions of **SMAP haplotype-sites** are shown in grey ovals. Read-reference nucleotide pairs are retrieved by `pysam <https://pysam.readthedocs.io/en/latest/api.html>`_ 's ``get_aligned_pairs`` function, in which lower case nucleotides denote \"different from the reference"\.
	  
	  .. image:: ../images/sites/SMAP_delineate_haplotype_filter.png

   .. tab:: required input

	  .. tabs::

		 .. tab:: BED
		 
			Depending on the type of data (HiPlex, Shotgun, or GBS), a specific BED file must be created to define the start and end positions of loci.
			
			.. tabs::

			   .. tab:: HiPlex

				  .. image:: ../images/sites/BED_HiPlex.png  
				   
				  .. image:: ../images/sites/coordinates_HiPlex.png  
				   
				  For HiPlex data, the user needs to create a custom BED file listing the loci based on the primer binding sites. We recommend to keep primer sequences in HiPlex reads for mapping, but to define the region between the primers in the BED file used for **SMAP haplotype-sites**. This region is defined by the first nucleotide downstream of the forward primer binding site to the last nucleotide upstream of the reverse primer binding site.
				  
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  scaffold_312    56971  57046  scaffold_312_56971_57046     .                    \+ \    56971,57045       .              2        HiPlex_Set1  
				  scaffold_78     209790 209868 scaffold_78_209790_209868    .                    \+ \    209790,209867     .              2        HiPlex_Set1  
				  scaffold_157    107250 107307 scaffold_157_107250_107307   .                    \+ \    107250,107306     .              2        HiPlex_Set1  
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
			
				  The primer binding site coordinates need to be transformed as follows:
			
				  ================= =====================================================
				  BED                     INPUT
				  ================= =====================================================
				  Reference         reference sequence ID
				  Start             F-primer end position + 1
				  End               R-primer start position - 1
				  HiPlex_locus_name reference_start_end
				  Mean_Read_Depth   .
				  Strand            \+ \
				  SMAPs             F-primer end position + 1, R-primer start position - 2
				  Completeness      .
				  nr_SMAPs          2
				  Name              HiPlex_Set1
				  ================= =====================================================

			   .. tab:: Shotgun

				  .. image:: ../images/sites/BED_HiPlex.png  
				   
				  .. image:: ../images/sites/coordinates_Shotgun_SNPs.png  
				   
				  .. image:: ../images/sites/coordinates_Shotgun_SV.png  
				   
				  | Stepwise delineation of sliding frames for read-backed haplotyping based on a-priori known SNPs.
				  | 1. The first SNP on the scaffold becomes the first SNP of Locus 1.
				  | The upstream off-set distance or the first nucleotide of the scaffold defines the 5’ start site of Locus 1.
				  | 2. All SNPs within the frame_length are considered for Locus 1.
				  | 3. Of the overlapping SNPs, the position of the last SNP within the frame length is determined.
				  | 4. The 3’ end site of Locus 1 is positioned at the off-set distance after the last SNP in Locus 1.
				  | 5. The first SNP after an empty space with length frame_distance after the 3‘ end of Locus 2, becomes the first SNP of Locus 2.
				  | 6. The off-set distance defines the 5’ start site of Locus 2.
				  | 7. All SNPs within the frame_length are considered for Locus 2.
				  | 8. Of the overlapping SNPs, the position of the last SNP within the frame length is determined.
				  | 9. The 3’ end site of Locus 2 is positioned at the off-set distance after the last SNP in Locus 2.
				  | 10. The first SNP after length frame_distance after the 3‘ end of Locus 2 becomes the first SNP of Locus 3.
				  | SNPs positioned in the frame-distance regions are ignored.
				  | 11. The off-set distance defines the 5’ start site of Locus 3.
				  | 12. All SNPs within the frame_length are considered for Locus 3.
				  | 13. If only one SNP exists, this becomes the last SNP.
				  | 14. The 3’ end site of Locus 3 is positioned at the off-set distance after the last SNP in Locus 3.
				  | 15. The first SNP after length frame_distance after the 3‘ end of Locus 3 becomes the first SNP of Locus 4.
				  | 16. The off-set distance defines the 5’ start site of Locus 4.
				  | 17. If the frame_length exceeds the remaining length of the scaffold, it is set at the last nucleotide of the scaffold.
				  | 18. The position of the last SNP within the frame length is determined for Locus 4.
				  | 19. The 3’ end site of Locus 4 is positioned at the off-set distance after the last SNP, or at the last nucleotide of the scaffold.
				  | Special cases:
				  | Off-set distances are used to ensure the sequence context around the SNPs are also covered by the same read.
				  | In this case, the outer 5‘ and 3’ positions delineating the Locus are used as ‘anchor points’ rather than as polymorphic SNPs
				  | and are used for evaluation of complete coverage of the read across the Locus length (option --partial exclude).
				  | If an off-set distance is defined as 0, the 5’ end corresponds to the first SNP, and the 3’ end of the Locus corresponds to the last SNP.
				  | If only one SNP exists within the frame_length, then the Locus is limited to length 1 and only the single SNP is scored as haplotype.
				  | SNPs positioned in the frame-distance regions are ignored.
				  | If the frame_distance is defined as 0, loci may become adjacent.
				  | Overlap of neighboring loci is avoided by reduction of the 5’ off-set on the downstream locus.
				  | Frame_length must always be greater than or equal to off-set.
				  | Frame_length must always be shorter than longest read length (ideally about one-half to two-thirds).
				  | Frame_length is a measure for the maximum length per Locus.
				  | Effective Locus length depends on SNP density combined with off-set and frame_length.
				  | what happens if last SNP + off-set is positioned outside frame_length? 
				  

				  | For Shotgun data, the user needs to create a custom BED file listing the loci based on a VCF file with known SNPs and a sliding frame length. We recommend to define the region .... in the BED file used for **SMAP haplotype-sites**. This region is defined by a small region just upstream of a given SNP, and of a specific length that is shorter that the average read length. As rule of thumb, the ratio of the frame length to the half of the mean read length is the same as the ratio of the mean read depth to the minimum read depth required for genotype calling.  
				  
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
				  scaffold_312    56971  57046  scaffold_312_56971_57046     .                    \+ \    56971,57045       .              2        HiPlex_Set1  
				  scaffold_78     209790 209868 scaffold_78_209790_209868    .                    \+ \    209790,209867     .              2        HiPlex_Set1  
				  scaffold_157    107250 107307 scaffold_157_107250_107307   .                    \+ \    107250,107306     .              2        HiPlex_Set1  
				  =============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
			
				  The SNP coordinates need to be transformed into sliding frames as follows:
			
				  ================== ============================================================================
				  BED                     INPUT
				  ================== ============================================================================
				  Reference          reference sequence ID
				  Start              first SNP position - offset
				  End                last SNP position + offset
				  Shotgun_locus_name reference_start_end
				  Mean_Read_Depth    .
				  Strand             \+ \
				  SMAPs              First SNP position - offset, last SNP position + Offset - 1
				  Completeness       .
				  nr_SMAPs           2
				  Name               Shotgun_Set1
				  ================== ============================================================================

			   .. tab:: GBS
			   
				  .. image:: ../images/sites/BED_GBS.png  
				   
				  .. image:: ../images/sites/coordinates_GBS.png  
				   
				  | For GBS data, the user needs to run :ref:`SMAP delineate <SMAPdelHIW>` to create a BED file listing the loci with SMAPs (header is illustrative).

				  =============== ===== ===== =============================== =================== ======= ======================= ============== ======== =============
				  Reference       Start End   MergedCluster_name              Mean_read_depth     Strand  SMAPs                   Completeness   nr_SMAPs Name
				  =============== ===== ===== =============================== =================== ======= ======================= ============== ======== =============
				  scaffold_10030  15617 15711 scaffold_10030_15617_15711_+    1899                \+      15617,15621,15702,15710 13             4        2n_ind_GBS_SE
				  scaffold_10030  15712 15798 \scaffold_10030_15712_15798_\-  1930                \-      15712,15792,15797       9              3        2n_ind_GBS_SE
				  =============== ===== ===== =============================== =================== ======= ======================= ============== ======== =============
				  
				  | BED file entry listing all relevant features of two neighboring loci. On the + strand of the reference sequence, the start (15617) and end (15711) positions of the locus, together with the mean locus read depth (1899), the strand (\+), the internal SMAP positions (15621, 15702), the number of samples with data at that locus (completeness, 13), the number of SMAPs (4), and a custom label that denotes the dataset (2n_ind_GBS_SE). The second entry lists the locus and SMAP positions on the (\-) strand. 


		 .. tab:: VCF
		 
			==================== ===== == === === ======== ====== ==== ======
			##fileformat=VCFv4.2
			-----------------------------------------------------------------
			#CHROM               POS   ID REF ALT QUAL     FILTER INFO FORMAT
			==================== ===== == === === ======== ====== ==== ======
			scaffold_10030       15623 .  G   T   68888.7  .      .    GT
			scaffold_10030       15650 .  C   T   1097.13  .      .    GT
			scaffold_10030       15655 .  A   T   1097.13  .      .    GT
			scaffold_10030       15682 .  C   G   1097.13  .      .    GT
			scaffold_10030       15689 .  T   C   1097.13  .      .    GT
			scaffold_10030       15700 .  A   C   1097.13  .      .    GT
			scaffold_10030       15704 .  G   T   1097.13  .      .    GT
			scaffold_10030       15705 .  A   C   1097.13  .      .    GT
			scaffold_10030       15733 .  C   T   45538.80 .      .    GT
			scaffold_10030       15753 .  G   C   44581.50 .      .    GT
			scaffold_10030       15769 .  C   A   64858.50 .      .    GT
			scaffold_10030       15787 .  A   C   67454.00 .      .    GT
			scaffold_10030       15796 .  A   C   45281.60 .      .    GT
			==================== ===== == === === ======== ====== ==== ======
			
			VCF file listing the 13 SNPs identified at these two loci using third-party software (see also `Veeckman et al, 2018 <https://academic.oup.com/dnaresearch/article/26/1/1/5133005>`_). In order to comply with bedtools, which generates the locus \- \ SNP overlap, a 9-column VCF format with VCFv4.2-style header is required. However, only the first 2 columns contain essential information for **SMAP haplotype-sites**, the other columns may contain data, or can be filled with \"."\.

		 .. tab:: BAM
		 		 
			.. image:: ../images/sites/scaffold_10030_ref0030940_0070_edit.png
			
			| BAM file containing the alignments of single-end GBS read data of an individual genotype, illustrating the presence of various haplotypes. The GBS fragment is flanked on both sides by a *Pst* I restriction site (grey box) and contains two independent loci. The first locus contains single-end reads mapped on the forward (+) strand. 
			| The second locus contains reads mapped on the reverse (-) strand. Haplotypes are defined by combinations of neighboring SMAPs (light blue arrows) and SNPs (purple arrows). A SMAP at position 15622 is created by an InDel close to the \5' \ of the GBS-fragment combined with a misalignment (see :ref:`SMAP delineate <SMAPdelsepvmerg>` for details), while a SMAP at position 15792 is created by consistent soft clipping in a particular haplotype. Various sequencing read errors are present at positions other than the identified SNP positions, but are ignored as they are not listed in the VCF file. One of the SNPs (15793) is located in the soft clipped region.

   .. tab:: procedure
	  
	  | **SMAP haplotype-sites** reconstructs haplotypes based on SMAP positions and SNPs through read-backed haplotyping on a given set of BAM files.
	  | **SMAP haplotype-sites** first creates sets of polymorphic positions per locus on the reference genome by intersecting locus regions (obtained with :ref:`SMAP delineate <SMAPdelHIW>`) with a VCF file containing selected SNPs (obtained from any third-party SNP calling algorithm applied to the same set of BAM files). 
	  | In each BAM file, **SMAP haplotype-sites** then evaluates each read-reference alignment for the nucleotide aligned at the SMAP/SNP positions and scores as follows:

	  ========= ===================================================================================
	  CALL TYPE CLASSES
	  ========= ===================================================================================
	  .         absence of read mapping
	  0         presence of the reference nucleotide
	  1         presence of an alternative nucleotide (any nucleotide different from the reference)
	  \- \      presence of a gap in the alignment
	  ========= ===================================================================================
	
	  These calls are concatenated into a haplotype string of \'.01-'\s. For each discovered haplotype in the data, the total number of corresponding reads is counted per sample. Next, the haplotype counts of all samples are integrated into one master table, and expressed as relative haplotype frequency per locus per sample. Haplotypes with low frequency across all samples are removed to control for noise. The final table with haplotype frequencies per locus per sample is the end point for analysis of Pool-Seq data. Using the :ref:`option <SMAP_utilities_quickstartcommands>` ``--discrete_calls``, **SMAP haplotype-sites** transforms the haplotype frequency table into discrete haplotype calls for individuals.

	  Three modes may be chosen for discrete haplotype calling in individuals:
	  
	  ============================= =============
	  CALL TYPE                     CLASSES
	  ============================= =============
	  dosage calls in diploids      0, 1, 2
	  dosage calls in tetraploids   0, 1, 2, 3, 4
	  dominant calls                0, 1
	  ============================= =============

	  In the following sections, identification and quantification of haplotypes is illustrated on single-end GBS read data of a set of 8 diploid individuals at two partially overlapping loci. The content of the three example input files (BED, VCF, BAM) at this locus will be used to demonstrate the subsequent steps of **SMAP haplotype-sites**.
	  

----
	  
Output
------

**Tabular output**

.. tabs::

   .. tab:: General output

      By default, **SMAP haplotype-sites** will return two .tsv files.  
 
      :navy:`haplotype counts`
      
      **Read_counts_cx_fx_mx.tsv** (with x the value per option used in the analysis) contains the read counts (``-c``) and haplotype frequency (``-f``) filtered and/or masked (``-m``) read counts per haplotype per locus as defined in the BED file from **SMAP delineate**.  
      This is the file structure:
      
		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010      0       13      34      
		Chr1:100-200 01000      19      90      28      
		Chr1:100-200 00110      60      0       23      
		Chr1:450-600 0010       70      63      87      
		Chr1:450-600 0110       108     22      134     
		============ ========== ======= ======= ========

      :navy:`relative haplotype frequency`
      
      **Haplotype_frequencies_cx_fx_mx.tsv** contains the relative frequency per haplotype per locus in sample (based on the corresponding count table: Read_counts_cx_fx_mx.tsv). The transformation to relative frequency per locus-sample combination inherently normalizes for differences in total number of mapped reads across samples, and differences in amplification efficiency across loci.  
      This is the file structure:
      
		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010      0       0.13    0.40    
		Chr1:100-200 01000      0.24    0.87    0.33    
		Chr1:100-200 00110      0.76    0       0.27    
		Chr1:450-600 0010       0.39    0.74    0.39    
		Chr1:450-600 0110       0.61    0.26    0.61    
		============ ========== ======= ======= ========
		
   .. tab:: Additional output for individuals
   
      For individuals, if the option ``--discrete_calls`` is used, the program will return three additional .tsv files. Their content and order of creation is shown in :ref:`this scheme <SMAPhaplostep5>`.  
      
	  | :navy:`haplotype total discrete calls`
      
	  | The first file is called **haplotypes_cx_fx_mx_discrete_calls._total.tsv** and this file contains the total dosage calls, obtained after transforming haplotype frequencies into discrete calls, using the defined ``--frequency_interval_bounds``. The total sum of discrete dosage calls is expected to be 2 in diploids and 4 in tetraploids.

		============ ======= ======= ========
		Locus        Sample1 Sample2 Sample..
		============ ======= ======= ========
		Chr1:100-200 2       2       3       
		Chr1:450-600 2       2       2       
		============ ======= ======= ========
		
	  | :navy:`haplotype discrete calls`
	  
	  | The second file is **haplotypes_cx_fx_mx-discrete_calls_filtered.tsv**, which lists the discrete calls per locus per sample after ``--dosage_filter`` has removed loci per sample with an unexpected number of haplotype calls (as listed in haplotypes_cx_fx_mx_discrete_calls_total.tsv). The expected number of calls is set with option ``-z`` [use 2 for diploids, 4 for tetraploids].

		============ ========== ======= ======= ========
		Locus        Haplotypes Sample1 Sample2 Sample..
		============ ========== ======= ======= ========
		Chr1:100-200 00010         0       1       NA   
		Chr1:100-200 01000         1       1       NA   
		Chr1:100-200 00110         1       0       NA   
		Chr1:450-600 0010          1       1       1    
		Chr1:450-600 0110          1       1       1    
		============ ========== ======= ======= ========
		  
	  | :navy:`population haplotype frequencies`

	  | The third file, **haplotypes_cx_fx_mx_Pop_HF.tsv**, lists the population haplotype frequencies (over all individual samples) based on the total number of discrete haplotype calls relative to the total number of calls per locus.

		============ ========== ====== =====
		Locus        Haplotypes Pop_HF count
		============ ========== ====== =====
		Chr1:100-200 00010      25.0   4    
		Chr1:100-200 01000      50.0   4    
		Chr1:100-200 00110      25.0   4    
		Chr1:450-600 0010       50.0   6    
		Chr1:450-600 0110       50.0   6    
		============ ========== ====== =====

	  | For individuals, if the option ``--locus_correctness`` is used in combination with ``--discrete_calls`` and ``--frequency_interval_bounds``, the programm will create a new .bed file **haplotypes_cx_fx_mx_correctnessx_loci.bed** (loci filtered from the input .bed file) containing only the loci that were correctly dosage called (-z) in at least the defined percentage of samples. :ref:`See above <SMAPhaplostep5>`.

	  | :navy:`Loci with correct calls across the sample set`

		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Reference       Start  End    HiPlex_locus_name            Mean_read_depth      Strand  SMAPs             Completeness   nr_SMAPs Name
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		Chr1            100    200    Chr1_100-200                 .                    \+ \    100,199           .              2        HiPlex_Set1  
		Chr1            450    600    Chr1_450-600                 .                    \+ \    450,599           .              2        HiPlex_Set1  
		=============== ====== ====== ============================ ==================== ======= ================= ============== ======== =============
		
**Graphical output**

:navy:`haplotype diversity`

.. tabs::

   .. tab:: haplotype diversity across sampleset
	
	 By default, **SMAP haplotype-sites** will generate graphical output summarizing haplotype diversity. haplotype_diversity_across_sampleset.png shows a histogram of the number of distinct haplotypes per locus *across* all samples.  
     
   .. tab:: example graph
	
	  .. image:: ../images/sites/haplotype_counts.cigar.barplot.png


:navy:`haplotype frequency distribution per sample`

.. tabs::

   .. tab:: haplotype frequency distribution per sample
	 
     Graphical output of the haplotype frequency distribution for each individual sample can be switched **on** using the option ``--plot_all``. sample_haplotype_frequency_distribution.png shows the haplotype frequency distribution across all loci detected per sample. It is the graphical representation of each sample-specific column in **haplotypes_cx_fx_mx.tsv**. Using the option ``--discrete_calls``, this plot will also show the defined discrete calling boundaries.

   .. tab:: example graph
	
	  .. image:: ../images/sites/2n_ind_GBS_SE_001.bam.haplotype.frequency.histogram.png

:navy:`quality of genotype calls per locus and per sample (only for individuals)`

.. tabs::

   .. tab:: QC of loci and samples using discrete dosage calls  
	
     After discrete genotype calling with option ``--discrete_calls``, **SMAP haplotype-sites** will evaluate the observed sum of discrete dosage calls per locus per sample versus the expected value per locus (set with option ``-z``, recommended use: 2 for diploid, 4 for tetraploid). 
     
     The quality of genotype calls per *sample* is calculated in two ways: the fraction of loci with calls in that sample versus the total number of loci across all samples (sample_call_completeness); the fraction of loci with expected sum of discrete dosage calls (``-z``) versus the total number of observed loci in that sample (sample_call_correctness.tsv). These scores are calculated separately per *sample*, and **SMAP haplotype-sites** plots the distribution of those scores across the sample set (sample_call_completeness.png; sample_call_correctness.png).  
      
     Similarly, the quality of genotype calls per *locus* is calculated in two ways: the fraction of samples with calls for that locus versus the total number of samples (locus_call_completeness); the fraction of samples with expected sum of discrete dosage calls (``-z``) versus the total number of observed samples for that locus (locus_call_correctness.tsv). These scores are calculated separately per *locus*, and **SMAP haplotype-sites** plots the distribution of those scores across the locus set (locus_call_completeness.png; locus_call_correctness.png).  
      
     Both graphs and the corresponding tables (one for samples and one for loci) can be evaluated to identify poorly performing samples and/or loci. We recommend to eliminate these from further analysis by removing BAM files from the run directory and/or loci from the SMAP delineate BED file with SMAPs, and iterate through rounds of data analysis combined with sample and locus quality control.

   .. tab:: completeness and correctness across the sample set
	
	  .. image:: ../images/sites/sample_call_completeness_correctness_40canephora.png
	  
	  The sample call completeness plot shows the percentage of loci that have data across the samples after all filters. In read depth-saturated, low diversity datasets, the majority of samples should have high locus completeness and there should not be much variation in completeness between samples. In a high diversity or read depth-unsaturated sample set, locus completeness per sample will be lower and more spread out.
	  
	  The sample call correctness plot displays the percentage of correctly dosage called (``-z``) loci across the sampleset. Loci are only masked in samples with a dosage value different from ``-z`` but remain in the data set for all other samples with the expected dosage value.
	  
   .. tab:: completeness and correctness across the locus set
	
	  .. image:: ../images/sites/locus_call_completeness_correctness_40canephora.png

	  The locus call completeness plot displays the percentage of samples that have data (after every filter) on a locus for every locus. In read depth-saturated, low diversity sample sets, the majority of samples should have many high completeness loci and few low completeness loci. In a high diversity or read depth-unsaturated sample set, many loci will have a low completeness.
	  
	  The locus call correctness plot shows the percentage of samples that were correctly dosage called (``-z``) across the locus set. Loci with low correctness values indicate potential genotype calling artefacts and should be removed from the data set.

----

.. _SMAP_utilities_quickstartcommands:

  
Summary of Commands
-------------------

A detailed overview of the command line options can be found in section :ref:`Summary of Commands <SMAPhaplofreq>`
A typical command line example looks like this:

::

	smap haplotype-sites /path/to/BAM/ /path/to/BED/ /path/to/VCF/ -mapping_orientation stranded --no_indels -c 10 -f 5 -p 8 --plot_type png -partial include --min_distinct_haplotypes 2 -o haplotypes_SampleSet1

Command examples and options of **SMAP haplotype-sites** for a range of specific sample types are given under :ref:`haplotype frequency profiles <SMAPhaplofreq>`.  
Options may be given in any order.


