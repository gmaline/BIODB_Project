from Bio import Entrez
from Bio.KEGG.KGML.KGML_parser import read
import csv
import os
import Entrez

# Name: entrezid2KEGGid
# Summary: reads in entrez geneids (uid) and converts to KEGG ids using the
#          API from KEGG
# Parameters: uid - a geneid from entrez
# Return: a KEGG gene id
def entrezid2KEGGid(uid):
    url = 'curl http://rest.kegg.jp/conv/genes/ncbi-geneid:' + uid
    out = os.popen(url).read()
    keggid = out.split()[1]
    return keggid

# Name: keggID2PathwayID
# Summary: reads in KEGG gene ids and searches the database for pathways
# Parameters: keggid - a KEGG gene id
# Return: a list of pathways that gene is associated with
def keggId2PathwayId(keggid):
    url = 'curl http://rest.kegg.jp/link/pathway/' + keggid
    out = os.popen(url).read()
    pathids = []
    for x in out.split():
        if x != keggid:
            pathids.append(x)
    return pathids

# Name: pathwayID2PathwayInfo
# Summary: reads in KEGG pathway id and pulls name of pathway
# Parameters: pid - KEGG pathway id
# Return: an xml representation of pathway info
def pathwayId2PathwayInfo(pid):
    url2 = 'curl http://rest.kegg.jp/get/' + pid + '/kgml'
    out = os.system(url2 + "> pathway.xml")
    pathway = read(open("pathway.xml"))
    return pathway

# Name: pullKEGGPathways
# Summary: Container method to run the whole KEGG pathway process.
#          Reads in a list of gene info where gene symbol is column 0.
# Parameters: inFileName - the name of the input file
# Return: NA - writes results to output file
def pullKEGGPathways(inFileName, outFileName):
    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        gene_symbols = {}
        # Save each gene symbol as a key and gene name as item.
        # To avoid duplicate entries in the gene db.
        for line in reader:
            gene_symbols[line[0]] = line[1]

        for key in gene_symbols:
            if len(key) > 0:
                try:
                    uid = Entrez.symbol2entrezid(key)
                    keggid = entrezid2KEGGid(uid)
                    pathids = keggId2PathwayId(keggid)
                    with open(outFileName, 'w', newline='') as outfile:
                        writeFile = csv.writer(outfile)
                    for pathid in pathids:
                        pathway_info = pathwayId2PathwayInfo(pathid)
                        pathway_name = (str(pathway_info).split("\n"))[0].split(":")[1]
                        pathway_id = (str(pathway_info).split("\n"))[1].split(":")[2]
                        outfile.writerow([key, pathway_name, pathway_id])
                    outfile.close()
                except:
                    print(key + ": bad")
                    continue

    inFile.close()


pullKEGGPathways("expression_data_GSE156544.csv", "kegg_pathway_GSE156544.csv")

