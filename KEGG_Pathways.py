from Bio import Entrez
from Bio.KEGG.KGML.KGML_parser import read
import csv
import os

def pullPathways(inFileName):
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
                    uid = symbol2entrezid(key)
                    writeOutPathway(uid)
                except:
                    print(key + ": bad")
                    continue

    inFile.close()

def symbol2entrezid(gene_symbol):
    outfile = open('pathway_data_dump.csv', 'a')
    Entrez.email = 'gmaline@unomaha.edu'
    handle = Entrez.esearch(db="gene", term=gene_symbol + "[Gene Name] AND human[Organism]")
    record = Entrez.read(handle)
    handle.close()

    # Send the first uid retrieved on.
    return record["IdList"][0]

def writeOutPathway(uid):

    keggid = entrezid2KEGGid(uid)
    pathids = KEGGId2PathwayId(keggid)

    for pathid in pathids:
        pathway_info = pathwayId2PathwayInfo(pathid)
        pathway_name =  (str(pathway_info).split("\n"))[0].split(":")[1]
        pathway_id = (str(pathway_info).split("\n"))[1].split(":")[2]
        outfile.write(gene_symbol + ", " + pathway_name + ", " + pathway_id + "\n")

    outfile.close()





def entrezid2KEGGid(uid):
    url = 'curl http://rest.kegg.jp/conv/genes/ncbi-geneid:' + uid
    out = os.popen(url).read()
    keggid = out.split()[1]
    return keggid


def KEGGId2PathwayId(keggid):
    url = 'curl http://rest.kegg.jp/link/pathway/' + keggid
    out = os.popen(url).read()
    pathids = []
    for x in out.split():
        if x != keggid:
            pathids.append(x)
    return pathids


def pathwayId2PathwayInfo(pid):
    url2 = 'curl http://rest.kegg.jp/get/' + pid + '/kgml'
    out = os.system(url2 + "> pathway.xml")
    pathway = read(open("pathway.xml"))
    return pathway