import csv

# There is something wrong with this because you get a lot of repeats in here
# not the best.
def format_insert_gene(inFileName):
    outFile = open("create_gene_table.sql", "w")

    outFile.write("CREATE TABLE gene (\n")
    outFile.write("\tgene_id int NOT NULL AUTO_INCREMENT,\n")
    outFile.write("\tgene_symbol varchar(100) NOT NULL,\n")
    outFile.write("\tgene_name varchar(500),\n")
    outFile.write("\tPRIMARY KEY (gene_id)\n")
    outFile.write(");")

    with open(inFileName, "r") as inFile:
        reader = csv.reader(inFile)
        for line in reader:
            if len(line[0]) > 0:
                symbol = line[1]
                if len(symbol) == 0:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\"" + line[0] + "\", " + "null" + ");")
                else:
                    outFile.write("\nINSERT INTO gene (gene_symbol, gene_name) VALUES (\"" + line[0] + "\", \"" + line[1] + "\");")