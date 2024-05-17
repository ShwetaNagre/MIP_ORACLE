# -*- coding: utf-8 -*-
"""
@author: Sakshi
"""
import pandas as pd
from Bio.Seq import Seq

df = pd.read_excel (r"Passable MIPs.xlsx")
ligarm = df["Ligation Arm"].tolist()
extarm = df["Extension Arm"].tolist()
target = df["Target region"].tolist()
accid = df["Def Line"].tolist()
org = df["Organism"].tolist()
fname="whole_region"
tag2=[]
cnt2=0
#number the sequences and add the organisms to the definition line
for k in accid:
    k=k.rstrip("\n")
    tag2.append(k+" whole region"+"_"+str(cnt2)+"|"+org[cnt2])
    cnt2+=1
ofile = open(fname+".txt", "w")
cnt=0
#create a FASTA file with new definition lines and the arm1+target+arm2 sequence
for i in range(len(accid)):
    arm1put=Seq(target[i])
    larm=Seq(ligarm[i]).complement()
    earm=Seq(extarm[i]).reverse_complement()
    cnt+=1
    ofile.write(str(tag2[i]) + "\n"+str(larm)+str(arm1put)+str(earm)+"\n")

ofile.close()
