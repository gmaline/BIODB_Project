import csv

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

def expression_data(conversion, inFile):
    with open (inFileName, "r") as inFile:
        reader = csv.reader(inFile, delimiter='\t')