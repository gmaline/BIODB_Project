import csv

import goatools
from goatools.anno.genetogo_reader import Gene2GoReader
from goatools.obo_parser import GODag
from goatools.base import download_ncbi_associations
from goatools.base import download_go_basic_obo
import genes_NCBI_9606_ProteinCoding
import KEGG_Pathways

GeneID2nt_hum = genes_NCBI_9606_ProteinCoding.GENEID2NT

obo_fname = download_go_basic_obo()

fin_gene2go = download_ncbi_associations()

obodag = GODag("go-basic.obo")

# Read NCBI's gene2go. Store annotations in a list of namedtuples
objanno = Gene2GoReader(fin_gene2go, taxids=[9606])

# Get namespace2association where:
#    namespace is:
#        BP: biological_process
#        MF: molecular_function
#        CC: cellular_component
#    assocation is a dict:
#        key: NCBI GeneID
#        value: A set of GO IDs associated with that gene
ns2assoc = objanno.get_ns2assc()

for nspc, id2gos in ns2assoc.items():
    print("{NS} {N:,} annotated human genes".format(NS=nspc, N=len(id2gos)))

print(len(GeneID2nt_hum))

from goatools.goea.go_enrichment_ns import GOEnrichmentStudyNS

goeaobj = GOEnrichmentStudyNS(
    GeneID2nt_hum.keys(),  # List of mouse protein-coding genes
    ns2assoc,  # geneid/GO associations
    obodag,  # Ontologies
    propagate_counts=False,
    alpha=0.05,  # default significance cut-off
    methods=['fdr_bh'])  # defult multipletest correction method

with open("genes.csv", 'r') as gene_symbols:
    geneid2symbol = {}
    read_genes = csv.reader(gene_symbols)
    for line in read_genes:
        gene_id = KEGG_Pathways.symbol2entrezid(line[0])
        geneid2symbol[gene_id] = line[0]
gene_symbols.close()

with open("geneids.csv", 'w') as outfile:
    out_genes = csv.writer(outfile)
    for gene in geneid2symbol:
        out_genes.writerow(gene)
outfile.close()

geneids_study = geneid2symbol.keys()
goea_results_all = goeaobj.run_study(geneids_study)
goea_results_sig = [r for r in goea_results_all if r.p_fdr_bh < 0.05]


goeaobj.wr_xlsx("go_enrichment.xlsx", goea_results_sig)
goeaobj.wr_txt("go_enrichment.txt", goea_results_sig)