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
## Sources: For making a pie chart:
##           https://matplotlib.org/stable/gallery/pie_and_polar_charts
##          /pie_features.html


import csv
import os
import matplotlib.pyplot as plot

os.system("mysql gmaline < go_query.sql > go_result.csv")

pathway_name = []
pathway_count = []

with open("go_result.csv", 'r') as inFile:
    readResult = csv.reader(inFile, delimiter='\t')
    with open("go_overlapping.csv", 'w', newline='') as outFile:
        writeOverlap = csv.writer(outFile)
        line_num = 0
        for line in readResult:
            line_num += 1
            if line_num > 1 and int(line[2]) == 2:
                writeOverlap.writerow([line[0], line[1]])
    outFile.close()
inFile.close()

# Manual processing of terms between these steps to annotate
# into categories (subjective).

terms = {}
# Initialize all terms as 0
with open("go_overlapping_annotated.csv", 'r') as inFile:
    readAnnotated = csv.reader(inFile)

    for line in readAnnotated:
        terms[line[2]] = 0
inFile.close()

# Coutning each term
with open("go_overlapping_annotated.csv", 'r') as inFile:
    readAnnotated2 = csv.reader(inFile)
    for line in readAnnotated2:
        terms[line[2]] = terms[line[2]] + 1

# Organizing for chart.
labels = terms.keys()
sizes = []
for key in labels:
    sizes.append(terms[key])

# Create pi chart.

plot.pie(sizes, labels=labels, rotatelabels=True)
plot.axis('equal')
plot.savefig("go.png")

