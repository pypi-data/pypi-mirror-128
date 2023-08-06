.. raw:: html

    <style> .navy {color:navy} </style>
	
.. role:: navy

.. raw:: html

    <style> .white {color:white} </style>

.. role:: white

.. raw:: html

    <style> .green {color:green} </style>
	
.. role:: green

##################################################################
Comparisons across data sets, shared and unique loci
##################################################################

General Introduction
--------------------

**SMAP compare** analyzes the overlap (shared and unique loci) between two GBA data sets that have both been processed with :ref:`SMAP delineate <SMAPdelindex>`.
**SMAP compare** can be used to compare:

	1.	parameter settings during read `preprocessing <https://gbprocess.readthedocs.io/en/latest/gbs_data_processing.html>`_. 
	#.  parameter settings during read mapping (e.g. `BWA-MEM <http://bio-bwa.sourceforge.net/bwa.shtml>`_).
	#.  parameter settings during locus delineation (:ref:`SMAP delineate <SMAPdelindex>`).
	#.	sets of progeny derived from independent breeding lines to estimate transferability of marker sets across a breeding program.
	#.	a set of pools against their constituent individuals to estimate sensitivity of detection across the allele frequency spectrum (example shown below).
	#.	GBS experiments performed in different labs, to investigate if similar protocols lead to similar sets of loci, *i.e.* comparability of own data to external data.
	
----
	
Command to run SMAP compare
---------------------------

::

	smap compare <Set1.bed> <Set2.bed> 

----

Input
-----

**SMAP compare** only needs two final BED files containing loci, created with :ref:`SMAP delineate <SMAPdelHIW3>`.

Examples of input BED files are shown below:  

| Set1 contains GBS samples of 48 diploid individuals.  
| Set2 contains 16 replicate Pool-Seq GBS samples of those constituent 48 individuals.

.. tabs::

   .. tab:: Set1 BED (individuals)
	  
	  ========================= ====== ====== ================= ======= ====== =============== ========== ========= ========== =============
	  Reference                 Start  End    SMAPs             nr_SMAP Strand Cigar           Read_Depth nr_Stacks nr_Samples Label
	  ========================= ====== ====== ================= ======= ====== =============== ========== ========= ========== =============
	  scaffold_0_ref0040988     41456  41542  41456,41541       2       \+\    86M             604        3         3          2n_ind_GBS_SE
	  scaffold_0_ref0040988     41487  41570  41487,41569       2       \-\    55M3I28M        579        3         3          2n_ind_GBS_SE
	  scaffold_0_ref0040988     42705  42779  42705,42778       2       \+\    12S74M          61         2         2          2n_ind_GBS_SE
	  scaffold_0_ref0040988     42799  42885  42799,42884       2       \-\    86M             72         2         2          2n_ind_GBS_SE
	  scaffold_0_ref0040988     77858  77944  77858,77943       2       \+\    86M             43         3         3          2n_ind_GBS_SE
	  scaffold_0_ref0040988     156607 156693 156607,156692     2       \-\    86M             1067       37        37         2n_ind_GBS_SE
	  scaffold_10000_ref0012905 2531   2597   2531,2596         2       \+\    22S15M1D8M1D41M 39         3         3          2n_ind_GBS_SE
	  scaffold_10000_ref0012905 33660  33726  33660,33725       2       \+\    66M20S          18         1         1          2n_ind_GBS_SE
	  scaffold_10000_ref0012905 34733  34807  34733,34806       2       \+\    63M1I11M,74M    8090       45        45         2n_ind_GBS_SE
	  scaffold_10000_ref0012905 34733  34807  34733,34806       2       \-\    74M             7268       47        47         2n_ind_GBS_SE
	  scaffold_10004_ref0012901 36268  36335  36268,36296,36334 3       \+\    15S39M,67M      6169       54        36         2n_ind_GBS_SE
	  scaffold_10004_ref0012901 36268  36335  36268,36334       2       \-\    15M13D39M,67M   9150       48        48         2n_ind_GBS_SE
	  scaffold_10006_ref0012903 23081  23167  23081,23166       2       \-\    86M             20023      48        48         2n_ind_GBS_SE
	  ========================= ====== ====== ================= ======= ====== =============== ========== ========= ========== =============

   .. tab:: Set2 BED (pools)
   
	  ========================= ====== ====== ================= ======= ====== ============= ========== ========= ========== ===============
	  Reference                 Start  End    SMAPs             nr_SMAP Strand Cigar         Read_Depth nr_Stacks nr_Samples Label
	  ========================= ====== ====== ================= ======= ====== ============= ========== ========= ========== ===============
	  scaffold_0_ref0040988     41456  41542  41456,41541       2       \+\    86M           42         1         1          2n_pools_GBS_SE
	  scaffold_0_ref0040988     41487  41570  41487,41569       2       \-\    55M3I28M      111        3         3          2n_pools_GBS_SE
	  scaffold_0_ref0040988     156607 156693 156607,156692     2       \-\    86M           915        16        16         2n_pools_GBS_SE
	  scaffold_10000_ref0012905 34733  34807  34733,34806       2       \+\    74M           3403       16        16         2n_pools_GBS_SE
	  scaffold_10000_ref0012905 34733  34807  34733,34806       2       \-\    74M           3284       16        16         2n_pools_GBS_SE
	  scaffold_10004_ref0012901 36268  36335  36268,36296,36334 3       \+\    15S39M,67M    4242       32        16         2n_pools_GBS_SE
	  scaffold_10004_ref0012901 36268  36335  36268,36334       2       \-\    15M13D39M,67M 4209       16        16         2n_pools_GBS_SE
	  scaffold_10006_ref0012903 23081  23167  23081,23166       2       \-\    86M           13882      16        16         2n_pools_GBS_SE
	  ========================= ====== ====== ================= ======= ====== ============= ========== ========= ========== ===============
	  
How It Works
------------

| **SMAP compare** uses `BEDtools intersect <https://bedtools.readthedocs.io/en/latest/content/tools/intersect.html>`_ to identify shared loci by positional overlap between loci of two **SMAP delineate** BED files.
| **SMAP compare** then calculates summary statistics of features of overlapping loci, such as completeness scores and mean read depth per respective sample set.

For instance:

	1.	locus :green:`scaffold_0_ref0040988_41456-41542/+` is shared between the two sample sets.
	#.	in Set1, locus :green:`scaffold_0_ref0040988_41456-41542/+` is observed in 3 (out of 48) individual samples, and with cumulative read depth of 604.
	#.	in Set2, locus :green:`scaffold_0_ref0040988_41456-41542/+` is observed in 1 (out of 16) pool-Seq samples, and with cumulative read depth of 42.
	#.	locus :green:`scaffold_0_ref0040988_77858-77944/+` is only found in 3 out of 48 individuals and in none of the 16 pools.
	#.	locus :green:`scaffold_10006_ref0012903_23081-23167/-` is found in 48 out of 48 individuals, and also in 16 out of 16 pools.

| Since for each locus in either BED file, **SMAP compare** extracts the completeness scores in Set1 and Set2, respectively, it can create a pivot table with the number of **shared** loci for a given **combination of completeness scores in the two respective sets**.
| For instance, locus :green:`scaffold_0_ref0040988_41456-41542/+` is one example out of 8 shared loci that are found in 3 out of 48 individuals and also in 1 out of 16 pools, while locus :green:`scaffold_10006_ref0012903_23081-23167/-` is one example out of 8 shared loci that are found in 48 out of 48 individuals, and also in 16 out of 16 pools.
| For each set of shared loci for a given combination of completeness scores, **SMAP compare** also calculates the mean read depth across all those loci per sample set. This usually shows that loci with low completeness scores in one of both sample sets may be due to low read depth (and thus missed by undersampling during sequencing) in that sample set.  

----

Graphical output
----------------

**SMAP compare** will plot four heatmaps. The top two heatmaps show the number of loci per combination of Completeness scores in the two respective sample sets. The position in this Completeness score matrix defines in how many samples a locus is observed in each of the two sample sets (Set1 on the x-axis, Set2 on the y-axis), the color in the heatmap shows the number of loci with this combination of Completeness scores.  
Two heatmaps show the mean read depth in the same Completeness score matrix (one plot per sample set).

:navy:`Completeness`

| The first two heatmaps allow to evaluate the expected number of common loci across two sample sets.
| For instance, in this example data, Set1 contains the loci observed across 48 individuals, while Set2 contains the loci observed across 16 replicate pools of these constituent individuals.
| The first heatmap shows that most loci are observed in only one of 48 individuals (Completeness \`1´ \, left-hand side of the graph), showing that the vast majority of GBS fragments is unique to a single individual.
| The heatmap further shows that these same loci are never covered by reads in any of the 16 pools (Completeness \`0´ \), despite being created from the same 48 individuals, revealing the bias against low frequency (MAF 1-2%) allele observations in Pool-Seq data.  
| Conversely, the lower-right corner of the completeness matrix shows that the loci that are commonly found across all replicate pools (Completeness near \`16´ \ on the y-axis), are the same loci that were also commonly found in the individuals (Completeness near \`48´ \on the x-axis)

| The first heatmap shows the Completeness score matrix, including the non-overlapping classes (\`0´ \, observed in one set but not the other set).
| Below, the completeness graphs originally obtained with **SMAP delineate** per sample set are shown at the top (Set1, individuals) and right hand side (Set2, pools) of the **SMAP compare** heatmap for comparison.

	.. image:: ../images/compare/SMAP-compare_graph1.png

The second heatmap shows the Completeness score matrix with only the overlapping classes. Note the difference in the (false colour) scale that is adjusted to the total number of *common* loci in the two sample sets.

.. image:: ../images/compare/SMAP-compare_graph2.png

:navy:`read depth`

The last two graphs show if sufficient reads were mapped per sample set. These data can be compared to the saturation curves (add link to trouble shooting and recommendations) obtained after running **SMAP delineate**.

The third heatmap shows the mean read depth per locus observed in Set1, across the Completeness score matrix.

.. image:: ../images/compare/SMAP-compare_graph3.png

The fourth heatmap shows the mean read depth per locus observed in Set2, across the Completeness score matrix.

.. image:: ../images/compare/SMAP-compare_graph4.png	  