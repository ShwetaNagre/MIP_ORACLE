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
def_list = []

for i in defline:
	val = ' '.join(i.split(' ')[0:2])
	if val:
		def_list.append(val)

#check organism against the alignment definition line
for i in range(len(defline)):
    aldef=def_list[i]
    org=organisms[i]
    if org in aldef:
        new.append('yes')
    else:
        new.append('no')
for h in range(len(new)):
	if new[h]=='no':
		presentorg.append("Different Organism Found")
	else:
		presentorg.append("Perfect Match Found")

#Output files generated for both perfect matches found and all matches found(BLAST Organism Check)
        
if len(presentorg) != len(df):
    print(f"Warning: Length of 'presentorg' ({len(presentorg)}) does not match length of DataFrame ({len(df)})")
else:
	df["Organism Check"]=presentorg
	df.to_excel('BLAST Organism Check.xlsx', index=False)
	df = df[~df['Organism Check'].isin(['Different Organism Found'])]
	df.to_excel('BLAST Organism Check(Only perfect).xlsx', index=False)
