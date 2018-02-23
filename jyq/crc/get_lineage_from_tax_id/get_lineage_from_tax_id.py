#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/9 21:56
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : get_lineage_from_tax_id.py
# @Software: PyCharm


"""

This script will generate lineage from tax_id
Before to run , make sure NCBITaxa has alreadly been installed. 
"""
import csv
from ete3 import NCBITaxa

ncbi = NCBITaxa()

def get_desired_ranks(taxid, desired_ranks):
    lineage = ncbi.get_lineage(taxid)
    names = ncbi.get_taxid_translator(lineage)
    lineage2ranks = ncbi.get_rank(names)
    ranks2lineage = dict((rank,taxid) for (taxid, rank) in lineage2ranks.items())
    return{'{}_id'.format(rank): ranks2lineage.get(rank, '<not present>') for rank in desired_ranks}

def search(taxids):
    desired_ranks = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    result=dict()
    for taxid in taxids:
        #print(list(ncbi.get_taxid_translator([taxid]).values())[0])
        ranks = get_desired_ranks(taxid, desired_ranks)
        re=["","","","","",""]
        for key, rank in ranks.items():
            if(key=="phylum_id"):
                if rank != '<not present>':
                    re[0]=list(ncbi.get_taxid_translator([rank]).values())[0]
            elif(key=='class_id'):
                if rank != '<not present>':
                    re[1]=list(ncbi.get_taxid_translator([rank]).values())[0]
            elif(key=='order_id'):
                if rank != '<not present>':
                    re[2]=list(ncbi.get_taxid_translator([rank]).values())[0]
            elif(key=='family_id'):
                if rank != '<not present>':
                    re[3]=list(ncbi.get_taxid_translator([rank]).values())[0]
            elif(key=='genus_id'):
                if rank != '<not present>':
                    re[4]=list(ncbi.get_taxid_translator([rank]).values())[0]
            elif(key=='species_id'):
                if rank != '<not present>':
                    re[5]=list(ncbi.get_taxid_translator([rank]).values())[0]
        # return re
        result[str(taxid)]=re
    return result


gi_tax=dict()
with open("nt_gi_tax") as gt:
    lines=gt.readlines()
    for line in lines:
        gi_tax[line.split(' ')[0]]=line.split(' ')[1][:-1]
tax_lin=dict()
print(type(list(gi_tax.values())[0]))
# exit(0)
result=search([int(x) for x in list(gi_tax.values())])
with open("result.tsv") as f:
    lines=f.readlines()
    contigs_gi=dict()
    contigs_gi_lines=[]
    for i in range(1,len(lines)):
        #print(gi_tax[lines[i].split('\t')[3].split('|')[1]])
        contigs_gi[lines[i].split('\t')[0]]=lines[i].split('\t')[3].split('|')[1]
        contigs_gi_lines.append(lines[i].split('\t')[0]+"\t"+lines[i].split('\t')[3].split('|')[1]+'\t'+gi_tax[lines[i].split('\t')[3].split('|')[1]]+'\t'+'\t'.join(result[lines[i].split('\t')[0]])+'\n')
    with open("contigs_gi",'w') as outfile:
        outfile.writelines(contigs_gi_lines)
