"""
read all vcf_paper_PRS.txt,
then get the vcf list and their each score to a csv file.
"""
import pandas
import os
import glob

inputDir = './'
outputDir = './'
paperName = 'PGS000028'

with open("score_"+paperName+"_list.csv",'w') as c:
    file = glob.glob(os.path.join(inputDir, "*_PRS.txt"))
    for i in file:
        name = i.split("_")[0][2:]
        with open(i,'r') as f:
            for line in f.readlines():
                if line[0]=="S":
                    c.write(name+'\t'+str(line[7:]))
            f.close()
