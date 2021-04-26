## Name: Grace Maline
## Email: gmaline@unomaha.edu
## Class: BIOI 4870/CSCI 8876, Spring 2021
## Assignment: Term Project
##
## Honor Pledge: On my honor as a student of the University of Nebraska at
## Omaha, I have neither given nor recieved unauthorized help on 
## this programming assignment. 
##
## Partners: NONE
##
## Sources: for making a bar plot: 
##          https://datatofish.com/bar-char-ython-,atplotlib/


import csv
import os
import matplotlib.pyplot as plot

os.system("mysql gmaline < pathway_query.sql > pathway_result.csv")

pathway_name = []
pathway_count = []

with open("pathway_result.csv", 'r') as inFile:
    readResult = csv.reader(inFile, delimiter='\t')
    line_num = 0
    for line in readResult:
        line_num += 1
        if line_num > 1 and line_num < 50:
            pathway_name.append(line[1])
            pathway_count.append(line[2])

    pathway_name.reverse()
    pathway_count.reverse()
    print(str(line_num))
    print(pathway_name)
    print(pathway_count)

    plot.bar(pathway_name, pathway_count, width=.5)
    plot.title("Representation of Kegg Pathways")
    plot.xlabel("Pathway Name")
    plot.xticks(rotation='vertical')
    plot.ylabel("Count")
    plot.savefig('pathway.png', dpi=300, bbox_inches='tight')

