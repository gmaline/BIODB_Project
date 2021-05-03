import csv

# Name: create_gene
# Summary: create the gene table DDL
# Parameters: NA
# Return: NA
def create_gene():
    outFile = open("DDL_and_DML/create_gene_table.sql", "w")

    outFile.write("CREATE TABLE gene (\n")
    outFile.write("\tgene_id int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tgene_name varchar(500),\n")
    outFile.write("\tPRIMARY KEY (gene_id)\n")
    outFile.write(");")

# Name: create_expression
# Summary: create the expression table DDL
# Parameters: NA
# Return: NA
def create_expression():
    outFile = open("DDL_and_DML/create_expression_table.sql", "w")

    outFile.write("CREATE TABLE expression (\n")
    outFile.write("\teid int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tproject_id varchar(100),\n")
    outFile.write("\tsample_id varchar(100),\n")
    outFile.write("\tdirection varchar(100),\n")
    outFile.write("\tPRIMARY KEY (eid)\n")
    outFile.write(");")

# Name: create_project
# Summary: create the project table DDL
# Parameters: NA
# Return: NA
def create_project():
    outFile = open("DDL_and_DML/create_project_table.sql", "w")

    outFile.write("CREATE TABLE project (\n")
    outFile.write("\tproject_id varchar(30) NOT NULL,\n")
    outFile.write("\tauthors varchar(300) NOT NULL,\n")
    outFile.write("\tproj_date varchar(30),\n")
    outFile.write("\ttaxid varchar(10),\n")
    outFile.write("\ttissue varchar(100),\n")
    outFile.write("\tPRIMARY KEY (project_id)\n")
    outFile.write(");")

# Name: create_GeneOntology
# Summary: create the Gene_Ontology table DDL
# Parameters: NA
# Return: NA
def create_GeneOntolgy():
    outFile = open("DDL_and_DML/create_go_table.sql", "w")

    outFile.write("CREATE TABLE Gene_Ontology (\n")
    outFile.write("\tgo_id varchar(100) NOT NULL,\n")
    outFile.write("\tgo_term varchar(500) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (go_id)\n")
    outFile.write(");")

# Name: create_KEGGPathway
# Summary: create the KEGG_Pathway table DDL
# Parameters: NA
# Return: NA
def create_KEGGPathway():
    outFile = open("DDL_and_DML/create_kegg_table.sql", "w")

    outFile.write("CREATE TABLE KEGG_Pathway (\n")
    outFile.write("\tpathway_id varchar(100) NOT NULL,\n")
    outFile.write("\tpathway_name varchar(500) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (pathway_id)\n")
    outFile.write(");")

# Name: create_FunctionsIn
# Summary: create the Functions_In table DDL
# Parameters: NA
# Return: NA
def create_FunctionsIn():
    outFile = open("DDL_and_DML/create_functions_table.sql", "w")

    outFile.write("CREATE TABLE Functions_In (\n")
    outFile.write("\tpathway_name varchar(100) NOT NULL,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (fid)\n")
    outFile.write(");")

# Name: create_DescribedBy
# Summary: create the Described_By table DDL
# Parameters: NA
# Return: NA
def create_DescribedBy():
    outFile = open("DDL_and_DML/create_describes_table.sql", "w")

    outFile.write("CREATE TABLE Described_By (\n")
    outFile.write("\tgo_id varchar(100) NOT NULL,\n")
    outFile.write("\tproject_id varchar(100) NOT NULL,\n")
    outFile.write("\tPRIMARY KEY (go_id, project_id)\n")
    outFile.write(");")

# Name: format_insert_gene
# Summary: create the insert statements for the gene table
# Parameters: inFileName - the data file
# Return: OutFileName - the sql file with insert statements
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
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name)\n"
                                  + "VALUES (\""
                                  + symbol + "\", " + "null" + ");")
                else:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) \n"
                                  + "VALUES (\""
                                  + symbol + "\", \"" + genes[symbol] + "\");")

    outFile.close()

# Name: format_insert_expression
# Summary: create the insert statements for the expression table
# Parameters: inFileName - the data file
#             OutFileName - the sql file with insert statements
#             project_id - the project id
# Return: NA
def format_insert_expression(inFileName, outFileName, project_id):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            if len(line[0]) > 0:
                gene_symbol = line[0]
                sample_id = line[3]
                direction = line[2]
                outFile.write("\nINSERT INTO expression (gene_symbol, "
                              + "project_id, sample_id, direction) \nVALUES (\""
                              + gene_symbol + "\", \"" + project_id + "\", \""
                              + sample_id + "\", \"" + direction + "\");")
    outFile.close()

# Name: format_insert_KEGG
# Summary: create the insert statements for the KEGG_Pathway table
# Parameters: inFileName - the data file
#             OutFileName - the sql file with insert statements
# Return: NA
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
            outFile.write("\nINSERT INTO KEGG_Pathway (pathway_id,"
                          + " pathway_name) \nVALUES (\""
                          + pathway_id + "\", \"" + pathway_name + "\");")
    outFile.close()

# Name: format_insert_FunctionsIn
# Summary: create the insert statements for the Functions_In table
# Parameters: inFileName - the data file
#             OutFileName - the sql file with insert statements
# Return: NA
def format_insert_FunctionsIn(inFileName, outFileName):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        pairs = {}
        for line in reader:
            gene_symbol = line[0]
            pathway_name = line[2]
            pairs[gene_symbol + " " + pathway_name] = [gene_symbol, pathway_name]
        for pair in pairs.keys():
            outFile.write("\nINSERT INTO Functions_In (gene_symbol, "
                          + "pathway_name) \nVALUES (\"" + pairs[pair][0]
                          + "\", \"" + pairs[pair][1] + "\");")
    outFile.close()

# Name: format_insert_GO
# Summary: create the insert statements for the Gene_Ontology table
# Parameters: inFileName - the data file
#             OutFileName - the sql file with insert statements
# Return: NA
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
            outFile.write("\nINSERT INTO Gene_Ontology (go_id, go_term) \nVALUES"
                          + " (\"" + go_id + "\", \"" + go_term + "\");")
    outFile.close()

# Name: format_insert_DescribedBy
# Summary: create the insert statements for the Described_By table
# Parameters: inFileName - the data file
#             OutFileName - the sql file with insert statements
#             project - the project id
# Return: NA
def format_insert_DescribedBy(inFileName, outFileName, project):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            go_id = line[0]
            outFile.write("\nINSERT INTO Described_By (go_id, project_id) "
                          + "\nVALUES (\"" + go_id + "\", \"" + project
                          + "\");")
    outFile.close()

# Name: format_insert_project
# Summary: create the insert statements for the expression table
# Parameters: inFileName - the data file
#             outFileName - the sql file with insert statements
# Return: NA
def format_insert_project(inFileName, outFileName):
    outFile = open(outFileName, "w")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            project_id = line[0]
            authors = line[1]
            proj_date = line[2]
            taxid = line[3]
            tissue = line[4]
            outFile.write("\nINSERT INTO project (project_id, authors,"
                          + " proj_date, taxid, tissue) \nVALUES (\""
                          + project_id + "\", \"" + authors + "\", \""
                          + proj_date + "\", \"" + taxid + "\", \"" + tissue
                          + "\");")
    outFile.close()




# Creating the sql create table files.
create_gene()
create_expression()
create_project()
create_GeneOntolgy()
create_DescribedBy()
create_KEGGPathway()
create_FunctionsIn()
create_project()

# Creating the sql insert files
format_insert_project("Data/project_info_data.csv",
                      "DDL_and_DML/insert_project.sql")

format_insert_gene("Data/expression_data_all.csv",
                   "DDL_and_DML/insert_gene_all.sql")
format_insert_KEGG("Data/kegg_pathway_all.csv",
                   "DDL_and_DML/insert_kegg_all.sql")
format_insert_GO("Data/go_enrichmentall.csv",
                 "DDL_and_DML/insert_GO_all.sql")

format_insert_expression("Data/expression_data_GSE156544.csv",
                         "DDL_and_DML/insert_expression_GSE156544.sql",
                         "GSE156544")
format_insert_FunctionsIn("Data/kegg_pathway_GSE156544.csv",
                          "DDL_and_DML/insert_functionsin_GSE156544.sql")
format_insert_DescribedBy("Data/go_enrichmentGSE156544.csv",
                          "DDL_and_DML/insert_describes_GSE156544.sql",
                          "GSE156544")

format_insert_expression("Data/expression_data_BioProjectPRJNA634489.csv",
                         "DDL_and_DML/insert_expression_BioProjectPRJNA634489.sql",
                         "BioProjectPRJNA634489")
format_insert_FunctionsIn("Data/kegg_pathway_BioProjectPRJNA634489.csv",
                          "DDL_and_DML/insert_functionsin_BioProjectPRJNA634489.sql")
format_insert_DescribedBy("Data/go_enrichmentBioProjectPRJNA634489.csv",
                          "DDL_and_DML/insert_describes_BioProjectPRJNA634489.sql",
                          "BioProjectPRJNA634489")