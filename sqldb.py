import csv

# There is something wrong with this because you get a lot of repeats in here
# not the best.
def format_insert_gene(inFileName):
    outFile = open("create_gene_table.sql", "w")

    outFile.write("CREATE TABLE gene (\n")
    outFile.write("\tgene_id int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL UNIQUE,\n")
    outFile.write("\tgene_name varchar(500),\n")
    outFile.write("\tPRIMARY KEY (gene_id)\n")
    outFile.write(");")



    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        gene_symbols = {}
        # Save each gene symbol as a key and gene name as item.
        # To avoid duplicate entries in the gene db.
        for line in reader:
            gene_symbols[line[0]] = line[1]

        for key in gene_symbols:
            if len(key) > 0:

                # Assign null if longer gene name is absent
                if len(gene_symbols[key]) == 0:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\"" + key + "\", " + "null" + ");")
                else:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\"" + key + "\", \"" + gene_symbols[key] + "\");")

def format_insert_project(inFileName):
    outFile = open("create_project_table.sql", "w")

    outFile.write("CREATE TABLE project (\n")
    outFile.write("\tproject_id varchar(30) NOT NULL,\n")
    outFile.write("\tauthors varchar(300) NOT NULL,\n")
    outFile.write("\tproj_date varchar(30),\n")
    outFile.write("\ttaxid varchar(10),\n")
    outFile.write("\torganism varchar(30),\n")
    outFile.write("\tPRIMARY KEY (project_id)\n")
    outFile.write(");")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            outFile.write("\nINSERT INTO project (project_id, authors, proj_date, taxid, organism) VALUES (\""
                          + line[0] + "\", \"" + line[1] + "\", \"" + line[2] + "\", \"" + line[3] + "\", \""
                          + line[4] + "\");")
