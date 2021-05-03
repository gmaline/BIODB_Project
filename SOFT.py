import csv

# Name: id2gene
# Summary: This iterates through the SOFT file table and stores the tables id corresponding to
#          a gene name.
# Parameters: inFileName - the name of the SOFT file to iterate through
# Returns: conversion - a dictionary in the format {id: gene_symbol}
def id2gene(inFileName):
    conversion = {}
    with open (inFileName, "r") as inFile:
        reader = csv.reader(inFile, delimiter='\t')
        startTable = False
        for line in reader:
            if line[0][0:19] == '!platform_table_end':
                break
            elif startTable:
                conversion[line[0]] = []
                if len(line) >= 10:
                    conversion[line[0]].append(line[9])
                if len(line) >= 11:
                    conversion[line[0]].append(line[10])
            elif line[0][0:21] == '!platform_table_begin':
                startTable = True
    return conversion

# Name: expression_data
# Summary: Grab the data from the SOFT File and store gene symbol, gene name,
#          expression direction. Writes all of the info out to a csv.
# Parameters: conversion - a dictionary in the format {id: gene_symbol}
#             inFileName - the name of the SOFT file to iterate through
#             sample_list - the samples from this project relevant to this db
#             projectID - the project id to assign to each of the records in the
#                         data dump.
def expression_data(conversion, inFileName, sample_list, projectID):
    with open("Data/expression_data" + projectID + ".csv", "w", newline='') as outFile:
        writer = csv.writer(outFile)
        with open (inFileName, "r") as inFile:
            reader = csv.reader(inFile, delimiter='\t')
            collect_Sample = False
            startTable = False
            sample = ""
            for line in reader:
                if line[0][0:17] == '!sample_table_end':
                    collect_Sample = False
                    startTable = False
                elif startTable and collect_Sample:
                    direction = "up"
                    if line[0] != "ID_REF":
                        if line[1][0] == '-':
                            direction = "down"
                        elif line[1][0] == '0':
                            direction = "neither"
                        writer.writerow([str(conversion[line[0]][0]),
                                         str(conversion[line[0]][1]), direction,
                                         sample, projectID])
                elif in_sample_list(line[0], sample_list):
                    collect_Sample = True
                    sample = line[0][0:20].split('=')[1][1:]
                elif line[0][0:19] == '!sample_table_begin':
                    startTable = True
        inFile.close()
    outFile.close()


# Name: in_sample_list
# Summary: This is a help method to make sure that the sample being ocnsidered is
#          in the list of samples that should be kept.
# Parameters: check - the sampleID being checked
#             slist - the list of sample ids to keep data from
# Returns: boolean - True if check is in the list, False if it is not
def in_sample_list(check, slist):
    for x in slist:
        if check.startswith(x):
            return True
    return False

# Name: project_info
# Summary: This iterates through the SOFT file table and stores information
#          about the project. Writes results to a csv file.
# Parameters: inFileName - the name of the SOFT file to iterate through
#             proj_name - the name of the project for the output file.
def project_info(inFileName, projectID):
    with open("Data/project_info_" + projectID + ".csv", "a", newline='') as outFile:
        writer = csv.writer(outFile)
        with open (inFileName, "r") as inFile:
            reader = csv.reader(inFile, delimiter='\t')
            projID = ""
            authors = []
            date = ""
            taxid = ""
            organism = ""
            #header = ["geo_accession", "authors", "date", "taxid", "organism"]
            #writer.writerow(header)
            for line in reader:
                if line[0][0:23] == '!Series_submission_date':
                    date = line[0].split('=')[1][1:]
                if line[0][0:19] == '!Series_contributor':
                    authors.append(line[0].split("=")[1][1:])
                if line[0][0:21] == '!Series_geo_accession':
                    projectID = line[0].split("=")[1][1:]
                if line[0][0:18] == '!Platform_organism':
                    organism = line[0].split("=")[1][1:]
                if line[0][0:15] == '!Platform_taxid':
                    taxid = line[0].split("=")[1][1:]
            str_authors = ""
            for author in authors:
                str_authors += author + "; "
            writer.writerow([projID, str_authors, date, taxid, organism])

        inFile.close()
    outFile.close()

# Parsing the first project.
samples1 = ["^SAMPLE = GSM4733279", "^SAMPLE = GSM4733280", "^SAMPLE = GSM4733281", "^SAMPLE = GSM4733282"]
dict1 = id2gene("Data/GSE156544_family.soft")
expression_data(dict1, "Data/GSE156544_family.soft", samples1, "GSE156544")
project_info("Data/GSE156544_family.soft", "GSE156544")