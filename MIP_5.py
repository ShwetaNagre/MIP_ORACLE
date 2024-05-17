# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""

# Filter for organisms
import pandas as pd
import os
name1="Resultswr.xml"
path=os.getcwd()
files = os.listdir(path)
trial_3=pd.DataFrame()

accid=[]
organisms=[]


df=pd.read_excel('MIP parsed(NEW).xlsx', index_col=None) 
defline=df['Alignment Definition'].tolist()
accid=df['Def Line'].tolist()

#Parsing the organism from the definition line
for s in accid:
    s=s.strip()
    val = s.rpartition("|")
    organisms.append(val[2])


presentorg=[]
cnt=1
new=[]
#check organism against the alignment definition line
for i in range(len(defline)):
    aldef=defline[i]
    org=organisms[i]
    if org in aldef:
        new.append('yes')
    else:
        new.append('no')
    if len(new) == 10:
        if 'no' in new:
            for h in range(len(new)):
                presentorg.append("Different Organism Found")
                #print("no here")
            
        else:
            for h in range(len(new)):
                presentorg.append("Perfect Match Found") 
                #print("else here")
    
    cnt+=1
    if len(new)==10:
        new=[]
        cnt=0
#Output files generated for both perfect matches found and all matches found(BLAST Organism Check)
df["Organism Check"]=presentorg
df.to_excel('BLAST Organism Check.xlsx', index=False)
df = df[~df['Organism Check'].isin(['Different Organism Found'])]
df.to_excel('BLAST Organism Check(Only perfect).xlsx', index=False)
