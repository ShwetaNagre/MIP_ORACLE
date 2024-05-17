# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""

import pandas as pd
import os
name1="Resultswr.xml"

import sys
output = sys.argv[1]
path=os.getcwd()
files = os.listdir(path)


df=pd.read_excel('BLAST Organism Check(Only perfect).xlsx', index_col=None) 
df2=pd.read_excel('Passable MIPs.xlsx', index_col=None) 
defline=df['Def Line'].tolist()
finallist=[]
firstname=""
cnt=0
act_def=[]
#taking definition from BLAST output perfect matches, then takes first defline from 10 alignment results
for a in defline:
    val = a.rpartition("|")
    act_def.append(val[0])
for i in act_def:
    ind=act_def.index(i)
    nlist=act_def[ind:ind+10]
    if all(x==nlist[0] for x in nlist):
        cnt+=1
        if cnt==1:
            finallist.append(i)
        elif cnt==10:
            cnt=0
        else:
            continue

#get the index with succesful results
elemnum=[]
for i in finallist:
    nstring=str(i).strip('\n')
    split_string = nstring.split("whole region_")
    elemnum.append(int(split_string[1]))

column_names=["Def Line","Main Sequence","Target region","Ligation Arm","TM 1","GC content 1","Continuous stretch","Extension Arm","TM 2","GC content 2","Continuous stretch 2","Reverse Strand Target region","Ligation Arm(Rev)","TM Rev","GC content Rev","Continuous stretch Rev","Extension Arm Rev","TM 2 Rev","GC content 2 Rev","Continuous stretch 2 Rev"]
df3=pd.DataFrame(columns = column_names)
entries=[]

#get lines from passable MIPs according to the index of MIPs who got good BLAST results
for ind in elemnum:
    if ind==len(df2):
        break
    df3 = df3.append(df2.iloc[ind])

#Output the final MIPs with good BLAST results
df3.to_excel(output+".xlsx", index=False)
