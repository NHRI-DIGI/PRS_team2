#this code can calculate a vcf file's PRS from $refName.
# $inputPath is the place where you store your vcf files.
# #refName   is the paper you use to compare each SNPs.
import pandas as pd
import math
import argparse

refName="PGS000050"
inputPath = "/NovaSeq_128/team2/HBOC/Data/convert_vcf/"

parser = argparse.ArgumentParser()
parser.add_argument("--vcf",type=str,default=None) #eg. "python3 calculatePRS.py --vcf HWGS10060"
args = parser.parse_args()
fileName = args.vcf.replace("\r","") #eg. "HWGS10060"

VCF = open(inputPath+fileName+".vcf", 'r+') # read vcf file
#print(fileName)
hg38 = pd.read_csv(refName+"_hmPOS_GRCh38.csv",skiprows=19) # read SNPs csv file, skiprows=the line of the HEADERS

df= pd.DataFrame(hg38)
# df = df.dropna(subset=['effect_weight'], how='all') # clean the SNP if it doesn't have OR score
chr = [str(i) for i in range(1,23)]

with open(fileName+"_"+refName+"_PRS.txt",'w+') as f:
    with open(fileName+"_"+refName+".txt",'a+') as g:
        PRS=0
        cnt=0
        for line in VCF.readlines():
            if line.startswith('#'): # ignore all header
                continue
            info = line.split("\t")
            if info[0][3:] in chr:
                CHROM = eval(info[0][3:]) # make "chr.1" to "1"
            else:
                continue
            POS   = int(info[1])          # get POS
            REF   = info[3]               # get REF
            ALT   = info[4].split(',')    # get ALT
            WGS   = info[-1][0:3]         # get WGS eg."0/1" or "1/1"
            filter = (df["hm_chr"]==CHROM)            #filter will let vcf only find it's chromosome number in reference.
            for index ,row in df[filter].iterrows():    #eg. if chr=1 in vcf , it will only find chr=1 in reference,nor other chr.
                if row["hm_pos"]==POS and row["effect_allele"] ==REF and row["other_allele"] in ALT:# check whether position、allele are the same
                    for i in df.loc[index].tolist(): # write .txt
                        g.write(str(i)+"\t")
                    g.write("\n")
                    # print("find one!")
                    Or = df.loc[index]["effect_weight"]  #natural log of OR
                    if WGS[0]!='0' and WGS[2]!='0': #calculate PRS score
                        PRS+= 2*Or
                    else:
                        PRS+= Or
                    cnt+=1
                    # print("Score:",PRS)
                    break
        # print("found ",cnt," .")
        # print("PRS score =",PRS)
        f.write("total: "+str(cnt)+"\n")
        f.write("Score: "+str(PRS)+"\n")
    g.close()
f.close()

