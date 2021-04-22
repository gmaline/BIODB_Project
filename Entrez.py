# Name: symbol2entrezid
# Summary: converts a gene symbols to its uid for entrez
# Parameters: gene_symbol - the shortened gene name/symbol term
#              to search with the entrez api
# Return: a uid (geneid)
def symbol2entrezid(gene_symbol):
    outfile = open('pathway_data_dump.csv', 'a')
    Entrez.email = 'gmaline@unomaha.edu'
    handle = Entrez.esearch(db="gene", term=gene_symbol + "[Gene Name] AND human[Organism]")
    record = Entrez.read(handle)
    handle.close()

    # Send the first uid retrieved on.
    return record["IdList"][0]