# MIP_ORACLE: Identifies unique target regions with diagnostic significance in pathogens.

---

# Table of contents
  1. Overview
  2. Requirements
  3. Execution
  4. Workflow

---

# Overview
MIP_ORACLE is a software to filter and identify Molecular Inversion Probes with diagnostic significance in antimicrobial resistance genes, and various other pathogen genomes. MIPs are single-stranded DNA molecules containing two complementary regions that flank the target DNA.  
These molecules often have a Fluorophore, DNA barcode, or Molecular tag for unique identification.

![MIP_example](https://github.com/SakshiPandey97/MIP_ORACLE/assets/59496870/9d92d545-ffe3-42c6-9125-0c3271ccd35f)

Rough Design Outline- 
1. Start with all possible MIPs by moving along the strand one base pair at a time. 
2. Design MIPs for both the forward and reverse strands so that we have the highest probability of binding and then proceed to filter them according to three user-specified criteria:  
   a) Temperature  
   b) GC Content  
   c) Nucleotide Repeats  
3. Following this, further filter the MIPs by BLASTing them against the host genome(human).
4. To further increase the probability of the MIP binding to the correct target region BLAST them against the non-redundant nucleotides database as well. Filter out any MIPs that match other organisms.

---

# Requirements
Nucleotide BLAST 2.12.0 + with the nt database.
  
Python 3.6 and the following Python packages:
1. pandas=1.1.5
2. biopython=1.70
3. configparser
4. regex
5. xlsxwriter
6. openpyxl

Users can install the required packages through conda using the following command

```bash
conda create -n mip_oracle --file mip_oracle_env.txt
```

For creating a database specific to the host (human), the following commands can be used

```bash
### Extract human sequences from NT DB
blastdbcmd -db $parameterJ/nt -taxids 9606 -out human_sequences.fasta

### Create a new BLAST database specific to humans
makeblastdb -in human_sequences.fasta -dbtype nucl -parse_seqids -out nt_human
```

---

# Execution -
1. Obtain sequences of interest in a FASTA format, make sure the organism name is present in the definition line of each sequence. 
2. Following this download all the program files and store them in the same directory as the FASTA file.
3. Fill out the requirements to filter MIPs in the config file provided. The MIPs within the ranges given will be accepted. ex. all MIPs with 45<temp<70 will be taken.

![image](https://user-images.githubusercontent.com/59496870/133621729-c870017d-8ed5-4c49-afe8-32ca1b00bf01.png)

4.  Run the shell script provided as so:
```bash
bash MIP_ORACLE.sh -i AAC-nucleotide -o AAC-nucleotide_results -l mip_oracle -j /DATA/databases/blast/nt/ -n /DATA/databases/blast/Nt_Human/
```
5.  nohup can also be used:
```bash
nohup bash MIP_ORACLE.sh -i AAC-nucleotide -o AAC-nucleotide_results -l mip_oracle -j /DATA/databases/blast/nt -n /DATA/databases/blast/Nt_Human/ > AAC-nucleotide_log.out &
```
where,  
-i = Name of the input FASTA file(There's no need to add the file extension)  
-o = Name of the ouptut file(There's no need to add the file extension)  
-l = The name of the conda environment containing all the packages  
-j = The location of the nt BLAST database  
-n = The location of the human-specific BLAST database  

6.  The following files will be generated(These files will be stored in a folder called LOG_FILES):
      1. The first file will contain all possible MIPs for the sequences provided.
      2. The second and third files will contain Passable MIPs(The MIPs that met user requirements as per the config file) and Eliminated MIPs(MIPs that were filtered out).
      3. The fourth file is the BLAST input containing arm1+target+arm2 sequences.
      4. The fifth and sixth files are the .xml result files from BLAST.
      5. The seventh file will contain the parsed BLAST results about each MIP, and the eighth file will have the filtered results.
      6. Lastly the final result file will be generated in an Excel format.
![image](https://github.com/ShwetaNagre/MIP_ORACLE2/blob/main/Result_files.png)    

---

# Workflow
![flowchart](https://github.com/ShwetaNagre/MIP_ORACLE2/blob/main/WORKFLOW.png)
