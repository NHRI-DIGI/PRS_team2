import pandas as pd
import os
"""
adjust paper to particular format of .txt file.
for each paper,you have to change "paperChr、Pos、Ref、Alt、EffectWeight" these varients to their own column's name below
"""
refName = "PGS000028"
paperChr = "chr_name"
paperPos = "chr_position"
paperRef = "effect_allele"
paperAlt = "other_allele"
paperEffectWeight = "effect_weight"
outputDir = "./paperAdjusted"
hg38 = pd.read_csv(refName+"_hmPOS_GRCh38.csv",skiprows=19) # read SNPs csv file, skiprows=the line of the HEADERS

df = pd.DataFrame(hg38)
df = df.sort_values(by=[paperChr]) # sort by chr number
# print(df)
if not os.path.isdir(outputDir):
    os.mkdir(outputDir)
with open(outputDir+"/HBOC_"+refName+"_adjusted.txt",'w') as f:
    f.write("\"Chr\"\t\"POS\"\t\"REF\"\t\"ALT\"\t\"OR\"\n")
    for idx,row in df.iterrows():
        f.write("\"chr"+str(row[paperChr])+"\"\t")
        f.write(str(row[paperPos])+"\t")
        f.write("\""+str(row[paperRef])+"\"\t")
        f.write("\""+str(row[paperAlt])+"\"\t")
        f.write(str(row[paperEffectWeight])+"\n")
    f.close()