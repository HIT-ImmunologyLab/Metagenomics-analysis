#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/10/9 21:44
# @Author  : qiusuo
# @Email    : qiusuo2456@gmail.com
# @File    : statics_crc.py.py
# @Software: PyCharm


"""

This script generate a table from concoct, virsorter and taxassign.
For different num of samples, edit line 15 accordingly
"""
header = ["contig_ID", "length", "Nb genes", "Category", "location", "Nb phage hallmark genes",
          "Phage gene enrichment sig", "Non-Caudovirales phage gene enrichment sig", "Pfam depletion sig",
          "Uncharacterized enrichment sig", "Strand switch depletion sig", "Short genes enrichment sig", "PHYLUM",
          "CLASS", "ORDER", "FAMILY", "GENUS", "SPECIES", "cov_mean_sample_0", "cov_mean_sample_1", "cov_mean_sample_2",
          "cov_mean_sample_3", "cov_mean_sample_4", "cov_mean_sample_5", "cov_mean_sample_6", "cov_mean_sample_7",
          "cov_mean_sample_8", "cov_mean_sample_9", "cov_mean_sample_10", "cov_mean_sample_11", "cov_mean_sample_12",
          "cov_mean_sample_13", "cov_mean_sample_14", "cov_mean_sample_15", "cov_mean_sample_16", "cov_mean_sample_17",
          "cov_mean_sample_18", "cov_mean_sample_19", "cov_mean_sample_20", "cov_mean_sample_21", "cov_mean_sample_22",
          "cov_mean_sample_23", "cov_mean_sample_24", "cov_mean_sample_25", "cov_mean_sample_26", "cov_mean_sample_27",
          "cov_mean_sample_28", "cov_mean_sample_29", "cov_mean_sample_30", "cov_mean_sample_31", "cov_mean_sample_32",
          "cov_mean_sample_33", "cov_mean_sample_34", "cov_mean_sample_35", "cov_mean_sample_36", "cov_mean_sample_37",
          "cov_mean_sample_38", "cov_mean_sample_39", "cov_mean_sample_40", "cov_mean_sample_41", "cov_mean_sample_42",
          "cov_mean_sample_43", "cov_mean_sample_44", "cov_mean_sample_45", "cov_mean_sample_46", "cov_mean_sample_47",
          "cov_mean_sample_48", "cov_mean_sample_49"]
table = []
category_4 = open("../virsort_wd/Predicted_viral_sequences/VIRSorter_prophages_cat-4.gb")
category_5 = open("../virsort_wd/Predicted_viral_sequences/VIRSorter_prophages_cat-5.gb")
category_6 = open("../virsort_wd/Predicted_viral_sequences/VIRSorter_prophages_cat-6.gb")
category_4_lines = category_4.readlines()
category_5_lines = category_5.readlines()
category_6_lines = category_6.readlines()
with open("cov_inputtableR.tsv") as cov:
    lines_cov = cov.readlines()
    with open("../virsort_wd/VIRSorter_global-phage-signal.csv") as vir:
        lines_vir = vir.readlines()
        with open("../tax/Contigs_ASSIGNMENTS.csv") as tax:
            lines_tax = tax.readlines()
            with open("../contigs_gi") as nt_virus:
                lines_nt_virus = nt_virus.readlines()

                for i in range(1, len(lines_cov)):
                    row = []
                    for j in range(len(header)):
                        row.append("not filled")
                    table.append(row)

                for i in range(1, len(lines_cov)):
                    line = lines_cov[i]
                    if line[-1] == '\n':
                        line = line[:-1]
                    table[i - 1][0] = line.split('\t')[0]
                    table[i - 1][1] = line.split('\t')[1]
                    table[i - 1][18:] = line.split('\t')[2:]

                tax_data = []
                for line in lines_tax:
                    if line[-1] == '\n':
                        line = line[:-1]
                    if (line[-1] == ','):
                        line = line + "NA"
                    tax_data.append((line.split(',')[0], line.split(',')[1:]))
                tax_data = dict(tax_data)

                for i in range(len(lines_cov) - 1):
                    if (table[i][0] in tax_data.keys()):
                        table[i][12:18] = tax_data[table[i][0]]
                    else:
                        table[i][12:18] = ["NA", "NA", "NA", "NA", "NA", "NA"]

                tax_data = []
                for line in lines_nt_virus:
                    if line[-1] == '\n':
                        line = line[:-1]
                    if (line[-1] == '\t'):
                        line = line + "NA"
                    tax_data.append((line.split('\t')[0], line.split('\t')[-6:]))
                tax_data = dict(tax_data)

                for i in range(len(lines_cov) - 1):
                    if (table[i][0] in tax_data.keys()):
                        table[i][12:18] = tax_data[table[i][0]]

                vir_data = []
                for line in lines_vir:
                    if (line[0] != '#'):
                        if line[-1] == '\n':
                            line = line[:-1]
                        if (line[-1] == ','):
                            line = line + "NA"
                        li = line.split(',')
                        del li[2]
                        vir_data.append(('k119_' + li[0].split('_')[2], li[2:]))
                vir_data = dict(vir_data)

                for i in range(len(lines_cov) - 1):
                    if (table[i][0] in vir_data.keys()):
                        table[i][2:4] = vir_data[table[i][0]][0:2]
                        table[i][4] = "NA"
                        table[i][5:12] = vir_data[table[i][0]][2:]
                    else:
                        table[i][2:12] = ["NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA", "NA"]

                category_4_data = []
                for line in category_4_lines:
                    if (line[:5] == "LOCUS"):
                        category_4_data.append((line.split('_')[1], '-'.join(line.split('_')[7].split('-')[1:-1])))
                category_4_data = dict(category_4_data)

                category_5_data = []
                for line in category_5_lines:
                    if (line[:5] == "LOCUS"):
                        category_5_data.append((line.split('_')[1], '-'.join(line.split('_')[7].split('-')[1:-1])))
                category_5_data = dict(category_5_data)

                category_6_data = []
                for line in category_6_lines:
                    if (line[:5] == "LOCUS"):
                        category_6_data.append((line.split('_')[1], '-'.join(line.split('_')[7].split('-')[1:-1])))
                category_6_data = dict(category_6_data)

                for key in category_6_data.keys():
                    print(key)
                for i in range(len(lines_cov) - 1):
                    if (table[i][0] in category_4_data.keys()):
                        table[i][3] = '4'
                        table[i][4] = category_4_data[table[i][0]]
                    elif (table[i][0] in category_5_data.keys()):
                        table[i][3] = '5'
                        table[i][4] = category_5_data[table[i][0]]
                    elif (table[i][0] in category_6_data.keys()):
                        table[i][3] = '6'
                        table[i][4] = category_6_data[table[i][0]]

with open("table.csv", 'w') as out_file:
    out_file.write(','.join(header) + '\n')
    for i in range(len(table)):
        if (len(table[i]) != len(header)):
            print("err")
        for j in range(len(table[i])):
            if (table[i][j] == ''):
                table[i][j] = "NA"
        out_file.write(','.join(table[i]) + '\n')

