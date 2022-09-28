

import pandas as pd
import numpy as np
import os 
from sklearn import preprocessing
files = os.listdir("-- your file location--")
for filename in files:
    if(filename[0]=='N'):
       
        searchdb= pd.read_csv(f'{filename}', encoding="big5hkscs", low_memory=False)
       
       searchdb['standardize']=preprocessing.scale(searchdb['effect_weight'])
       
        searchdb.to_csv(f'{filename}', index=False)
        
    


