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

def expression_data(conversion, inFileName, sample_list):
    with open("data_dump.csv", "w", newline='') as outFile:
        writer = csv.writer(outFile)
        with open (inFileName, "r") as inFile:
            reader = csv.reader(inFile, delimiter='\t')
            collect_Sample = False
            startTable = False
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
                        writer.writerow([str(conversion[line[0]][0]), str(conversion[line[0]][1]), direction])
                elif in_sample_list(line[0][0:20], sample_list):
                    collect_Sample = True
                elif line[0][0:19] == '!sample_table_begin':
                    startTable = True
        inFile.close()
    outFile.close()



def in_sample_list(check, slist):
    for x in slist:
        if x == check:
            return True
    return False