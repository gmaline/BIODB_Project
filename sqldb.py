import csv


def create_gene():
    outFile = open("create_gene_table.sql", "w")

    outFile.write("CREATE TABLE gene (\n")
    outFile.write("\tgene_id int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL UNIQUE,\n")
    outFile.write("\tgene_name varchar(500),\n")
    outFile.write("\tPRIMARY KEY (gene_id)\n")
    outFile.write(");")

def create_expression():
    outFile = open("create_expression_table.sql", "w")

    outFile.write("CREATE TABLE expression (\n")
    outFile.write("\teid int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tproject_id varchar(100),\n")
    outFile.write("\tsample_id varchar(100),\n")
    outFile.write("\tdirection varchar(100),\n")
    outFile.write("\tPRIMARY KEY (eid)\n")
    outFile.write(");")

def create_project():
    outFile = open("create_project_table.sql", "w")

    outFile.write("CREATE TABLE project (\n")
    outFile.write("\tproject_id varchar(30) NOT NULL,\n")
    outFile.write("\tauthors varchar(300) NOT NULL,\n")
    outFile.write("\tproj_date varchar(30),\n")
    outFile.write("\ttaxid varchar(10),\n")
    outFile.write("\tPRIMARY KEY (project_id)\n")
    outFile.write(");")

def create_GeneOntolgy():
    outFile = open("create_go_table.sql", "w")

    outFile.write("CREATE TABLE Gene_Ontology (\n")
    outFile.write("\tgo_id varchar(100) NOT NULL,\n")
    outFile.write("\tgo_term varchar(500) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (go_id)\n")
    outFile.write(");")

def create_KEGGPathway():
    outFile = open("create_kegg_table.sql", "w")

    outFile.write("CREATE TABLE KEGG_Pathway (\n")
    outFile.write("\tpathway_id varchar(100) NOT NULL,\n")
    outFile.write("\tpathway_name varchar(500) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (pathway_id)\n")
    outFile.write(");")

def create_FunctionsIn():
    outFile = open("create_functions_table.sql", "w")

    outFile.write("CREATE TABLE Functions_In (\n")
    outFile.write("\tpathway_name varchar(100) NOT NULL,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (pathway_name, gene_symbol)\n")
    outFile.write(");")

def create_DescribedBy():
    outFile = open("create_describes_table.sql", "w")

    outFile.write("CREATE TABLE Described_By (\n")
    outFile.write("\tgo_id varchar(100) NOT NULL,\n")
    outFile.write("\tproject_id varchar(100) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (go_id, project_id)\n")
    outFile.write(");")


def format_insert_gene(inFileName, OutFileName):
    outFile = open(OutFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        genes= {}
        # Save each gene symbol as a key and gene name as item.
        # To avoid duplicate entries in the gene db.
        for line in reader:
            gene_symbol = line[0]
            gene_name = line[1]
            genes[gene_symbol] = gene_name

        for symbol in genes.keys():
            if len(symbol) > 0:
                # Assign null if longer gene name is absent
                if len(genes[symbol]) == 0:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\""
                                  + symbol + "\", " + "null" + ");")
                else:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\""
                                  + symbol + "\", \"" + genes[symbol] + "\");")

    outFile.close()


def format_insert_expression(inFileName, outFileName):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            if len(line[0]) > 0:
                gene_symbol = line[0]
                project_id = line[4]
                sample_id = line[3]
                direction = line[2]
                outFile.write("\nINSERT INTO expression (gene_symbol, "
                              + "project_id, sample_id, direction) VALUES (\""
                              + gene_symbol + "\", \"" + project_id + "\", \"" + sample_id
                              + "\", \"" + direction + "\");")
    outFile.close()

def format_insert_KEGG(inFileName, outFileName):
    outFile = open(outFileName, "w")

    pathways = {}
    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            pathway_id = line[2]
            pathway_name = line[1]
            pathways[pathway_id] = pathway_name
        for pathway_id in pathways.keys():
            pathway_name = pathways[pathway_id]
            outFile.write("\nINSERT INTO KEGG_Pathway (pathway_id, pathway_name) VALUES (\""
                          + pathway_id + "\", \"" + pathway_name + "\");")
    outFile.close()

def format_insert_FunctionsIn(inFileName, outFileName):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            gene_symbol = line[0]
            pathway_name = line[2]
            outFile.write("\nINSERT INTO Functions_In (gene_symbol, pathway_name) VALUES (\""
                          + gene_symbol + "\", \"" + pathway_name + "\");")
    outFile.close()


def format_insert_GO(inFileName, outFileName):
    outFile = open(outFileName, "w")

    terms = {}
    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            go_id = line[0]
            go_term = line[3]
            terms[go_id] = go_term
        for go_id in terms.keys():
            go_term = terms[go_id]
            outFile.write("\nINSERT INTO Gene_Ontology (go_id, go_term) VALUES (\""
                          + go_id + "\", \"" + go_term + "\");")
    outFile.close()

def format_insert_DescribedBy(inFileName, outFileName, project):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            go_id = line[0]
            outFile.write("\nINSERT INTO Described_By (go_id, project_id) VALUES (\""
                          + go_id + "\", \"" + project + "\");")
    outFile.close()

def format_insert_project(inFileName, outFileName):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            project_id = line[0]
            authors = line[1]
            proj_date = line[2]
            taxid = line[3]
            outFile.write("\nINSERT INTO project (project_id, authors, proj_date, taxid) VALUES (\""
                          + project_id + "\", \"" + authors + "\", \"" + proj_date + "\", \"" + taxid + "\");")
    outFile.close()




# Creating the sql insert files.
create_gene()
create_expression()
create_project()
create_GeneOntolgy()
create_DescribedBy()
create_KEGGPathway()
create_FunctionsIn()

format_insert_gene("expression_data_GSE156544.csv", "insert_gene_GSE156544.sql")
format_insert_expression("expression_data_GSE156544.csv", "insert_expression_GSE156544.sql")
format_insert_KEGG("kegg_pathway_GSE156544.csv", "insert_kegg_GSE156544.sql")
format_insert_FunctionsIn("kegg_pathway_GSE156544.csv", "insert_functionsin_GSE156544.sql")
format_insert_GO("go_enrichmentGSE156544.csv", "insert_GO_GSE156544.sql")
format_insert_DescribedBy("go_enrichmentGSE156544.csv", "insert_describes_GSE156544.sql", "GSE156544")