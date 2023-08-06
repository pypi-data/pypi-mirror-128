# pygenricher
---
Pygenricher is a tool that enables Gene Set Enrichment Analysis on a list of genes and a custom pathway database. This tool utilizes the GSEApy library for
easy access to the enrichr method as a Python script. Pygenricher also visualizes the most relevant findings in a Webbrowser with an interactive and downloadable
plot, using the plotly framework. Furthermore the user can specify if the list of genes is already pre-ordered and thus run a different algorithm that takes
the order of genes into consideration.

# Installation
---
```
pip install pygenricher
```

# Usage
---
## Requirements
The following files are needed for running pygenricher:

* .gmt file consisting of the pathway related geneIDs (Is already in the repository under pygenricher/src/pygenricher/Data)
* .csv file with at least the following three columns "fisher_p_withinCluster", "fisher_q_withinCluster" and "geneID"
* The nomenclature of the geneIDs in the .csv file has to match the nomenclature of the geneIDs in the .gmt file.
* Example of a line in a .gmt file depicting a pathway:

```
BIOCARTA_GRANULOCYTES_PATHWAY	http://www.gsea-msigdb.org/gsea/msigdb/cards/BIOCARTA_GRANULOCYTES_PATHWAY	CXCL8	IFNG	IL1A	CSF3	SELP	ITGAM	ITGAL	TNF	ITGB2	PECAM1	ICAM2	C5	SELPLG	ICAM1	SELL											
```


# Command Line
---
In the /src directory the GeneEnrichment.py script is found and can be used in the following way.
```
pygenricher --db DATABASE --gene_list /path/to/csvfile (optional: --ranked True)
```
With the --db flag the user can choose between the different databases in the GMT file that is provided in the repository.
# Results
---

Pygenricher not only produces a downloadable plot but also a table, which summarizes the results of the Gene Set Enrichment Analysis for further investigation
of the found pathways. The new table is saved as a csv file in the directory EnrTables that is initially created by running the code.
