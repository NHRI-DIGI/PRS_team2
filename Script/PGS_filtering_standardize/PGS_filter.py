
import pandas as pd
import numpy as np
import os 
files = os.listdir("--your file location--")


for filename in files:
    # picking PGS files
    if(filename[0]=='P'):
        name=filename[0:filename.find('.')]
        searchdb= pd.read_csv(f'./process/{filename}', encoding="big5hkscs", low_memory=False)
       
        
    
#%% This section is to select data

        chorm_list= list(searchdb.iloc[:,1].astype(str))
        pos_list=   list(searchdb.iloc[:,2].astype(str))
        alle_list=list(searchdb.iloc[:,3].astype(str))
        ref_list=list(searchdb.iloc[:,4].astype(str))
        

        
            
        def VCFCheck(chorm, pos,ref,alle):
        
            for i in range(len(searchdb)):
                c_flag=False
                p_flag=False
                if(chrom == chorm_list[i]):
                    ptr=i
                    c_flag=True
                if(pos == pos_list[i]):
                    p_flag=True
                if(c_flag and p_flag):
                    ref_flag=False
                    alle_flag=False
                    if(ref == ref_list[i]):
                        ref_flag=True
                    if(alle == alle_list[i]):
                        alle_flag=True
                    if(alle_flag and ref_flag):
                        #if all info are matched, lebeling as 1
                        searchdb['label'][i]=1
                        break

        with open(' your vcf file', mode='r') as vcf:
            print("===== file in =====")
            for line in vcf: 
                if(line[0:3]=='chr' and line[3].isdigit() ): 
                    test=line.split("	")
                    if(test[1] in pos_list):
                        print("-----found pos-----")
                        chrom=test[0][3:]
                        pos=test[1]
                        alle=test[4]
                        ref=test[3]
                        # checking whether it matches or not
                        VCFCheck(chrom,pos,ref,alle)
                    
        print("===== check finishing =====")
        #%%
        # dropping useless
        searchdb_new=searchdb[searchdb['label'].notna()]
        #%%
        print("===== Outputting refresh data =====")
        searchdb_new=searchdb_new.to_csv(f'New_{name}.csv', index=False)
