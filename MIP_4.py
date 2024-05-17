from Bio.Blast import NCBIXML

import pandas as pd
import os

path=os.getcwd()
files = os.listdir(path)
trial_3=pd.DataFrame()

alignments=[]
start=[]
end=[]
linker=[]
matched_indexes=[]
qid=[]           
allq=[]
defn=[]
accid=[]
seqlist=[]
s=[]
f=open("whole_region.txt","r")
ksj=1
for line in f.readlines():
        if ksj % 2 == 0 :
            seqlist.append(line.rstrip())
        ksj += 1
with open("whole_region.txt") as fh:
    for line in fh:
        if line.startswith(">"):
            accid.append(line)

ks=0
trialdf=pd.DataFrame()
trial_2=pd.DataFrame()
trialdfh=pd.DataFrame()
trial_2h=pd.DataFrame()
count=0
toff=0
numdds=0
human_match=[]

#Parse the BLAST results
for i in files:
    #For non-human results
    if "Resultswr.xml" in i:
        result=open(i,"r")
        records= NCBIXML.parse(result)
        item=records
        a=0
        for record in records:
            toff+=1
            k=0
            if a==0:
                ks=0
            else:
                ks+=1
            allq.append(record.query)

            for alignment in record.alignments:

                numdds+=1
                start=[]
                if alignment.hit_def:
                    start.append(accid[ks])
                for hsp in alignment.hsps:
                    #only first hsp is taken for each hit, this is the hsp with the best score
                    #this is rough way to calculate query coverage and not completely accurate
                    #ex. qend=132 qstart=1 qlength=132 then 131+1/qlength=132/132
                    qcov=((hsp.query_end - hsp.query_start)+1)/(record.query_length)
                    
                    start.append(hsp.query_start)
                    start.append(hsp.query_end)
                    start.append(alignment.hit_def)
                    ident=(hsp.identities/ hsp.align_length)*100
                    evalue=hsp.expect

                    start.append(ident)
                    start.append(evalue)
                    start.append(qcov)
                    accidfin=alignment.accession
                    start.append(accidfin)

                    allq.append('')
                    trialdf=pd.DataFrame({"Def Line":pd.Series(start[0]),"Start":pd.Series(start[1]),"End":pd.Series(start[2]),"Alignment Definition":pd.Series(start[3]),"Ident":pd.Series(start[4]), "Eval":pd.Series(start[5]), "Query coverage":pd.Series(start[6]), "Alignment Accession":pd.Series(start[7])})
                trial_2=pd.concat([trial_2,trialdf], axis=0)
                a+=1
    #For human BLAST results
    elif "Resultshuman.xml" in i:
        result=open(i,"r")
        records= NCBIXML.parse(result)
        item=records
        a=0
        for record in records:
            #print(str(vars(record)))
            if "'num_hits': None" in str(vars(record)):
                human_match.append("None")
                continue
            toff+=1
            k=0
            if a==0:
                ks=0
            else:
                ks+=1
            allq.append(record.query)
            
            for alignment in record.alignments:
                print(alignment)
                numdds+=1
                #print(numdds)
                start=[]
                if alignment.hit_def:
                    start.append(accid[ks])
                for hsp in alignment.hsps:
                    #only first hsp is taken for each hit, this is the hsp with the best score
                    #this is rough way to calculate query coverage and not completely accurate
                    #ex. qend=132 qstart=1 qlength=132 then 131+1/qlength=132/132
                    qcov=((hsp.query_end - hsp.query_start)+1)/(record.query_length)
                    
                    start.append(hsp.query_start)
                    start.append(hsp.query_end)
                    start.append(alignment.hit_def)
                    ident=(hsp.identities/ hsp.align_length)*100
                    evalue=hsp.expect
                    start.append(ident)
                    start.append(evalue)
                    start.append(qcov)
                    accidfin=alignment.accession
                    start.append(accidfin)

                    allq.append('')
                    trialdfh=pd.DataFrame({"Def Line":pd.Series(start[0]),"Start":pd.Series(start[1]),"End":pd.Series(start[2]),"Alignment Definition":pd.Series(start[3]),"Ident":pd.Series(start[4]), "Eval":pd.Series(start[5]), "Query coverage":pd.Series(start[6]), "Alignment Accession":pd.Series(start[7])})
                trial_2h=pd.concat([trial_2h,trialdfh], axis=0)
                a+=1
            

            #break

ks=ks+1
allq.pop()
#Create parsed BLAST output file
if trial_2h.empty:
    tdf_line=trial_2["Def Line"].to_list()
    if len(human_match)<len(tdf_line):
        human_match=[]
        for i in tdf_line:
            human_match.append("None")
    trial_2['Human matches']=human_match
else:
    trial_2h.to_excel('MIP human parsed')
trial_2.to_excel('MIP parsed(NEW).xlsx', index=False)
