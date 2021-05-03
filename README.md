# BIODB_Project
This code is under the GNU General Public License v3.0 (https://choosealicense.com/licenses/gpl-3.0/).


## Generating Gene Expression Data:
1. Download SOFT format file from GEO (https://ftp.ncbi.nlm.nih.gov/geo/series/GSE156nnn/GSE156544/soft/)
2. Run **SOFT.py** - selects samples that compare COVID-19 vs Healthy (GSM4733279, GSM4733280, GSM4733281, GSM4733282), converts gene project id to gene symbol, extracts project info data, and creates expression_dataProjectID.csv

## Generating GO Enrichment Data:
1. Generate Gene Expression Data files
2. Run **GO.py** - searches gene ids from Entrez from gene symbols in the gene expression data files, creates an input file for the GO Enrichment, Runs GO Enrichment with GOATOOLS

## Generating KEGG Pathway Data:
1. Generate Gene Expression Data files
2. Run **KEGG_Pathways.py** - converts gene symbol to entrez id, entrez id to kegg id, kegg id to pathway id, pathway id to pathway info, and then writes to an output file.

## Generating mySQL DDL and DML
1. Generate Gene Expression Data files
2. Generate GO Enrichment Data files
3. Generate KEGG_Pathway Data files
4. Consolidate KEGG, GO, and Expression data files into additoinal "_all" files
5. run **sqldb.py** - pulls data from the files, generates insert statements, creates executable .sql files.
6. run "mysql gmaline < filename.sql" to create the database tables and population

## Analyses
1. Create the database with all previous steps
2. run **pathway_analysis.py** - queries the Functions_In table and creates some bar charts with matplotlib
3. run **go_analysis.py** - queries the Described_By table and finds overlaps, manual annotation step in between, creates pie chart with matplotlib
